from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum

from accounts.models import User
from .models import Stadium, StadiumManager
from .serializers import StadiumSerializer
from accounts.permissions import IsAdmin, IsStadiumOwner


class StadiumViewSet(viewsets.ModelViewSet):
    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'address', 'sport_types__name']
    ordering_fields = ['name', 'price_per_hour', 'created_at']

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return Stadium.objects.filter(is_active=True)

        if user.role == 'ADMIN':
            return Stadium.objects.all()

        if user.role == 'STADIUM_OWNER':
            return Stadium.objects.filter(owner=user)

        if user.role == 'STADIUM_MANAGER':
            managed_ids = StadiumManager.objects.filter(
                manager=user, is_active=True
            ).values_list('stadium_id', flat=True)
            return Stadium.objects.filter(id__in=managed_ids)

        return Stadium.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, (IsAdmin | IsStadiumOwner)]
        else:
            permission_classes = [permissions.IsAuthenticated, (IsAdmin | IsStadiumOwner)]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        if self.request.user.role == 'STADIUM_OWNER':
            serializer.save(owner=self.request.user)
        else:
            serializer.save()

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        stadium = self.get_object()

        if not (request.user.is_admin or
                (request.user.is_stadium_owner and stadium.owner == request.user) or
                StadiumManager.objects.filter(stadium=stadium, manager=request.user, is_active=True).exists()):
            return Response({"detail": "You do not have permission to view these statistics."},
                            status=status.HTTP_403_FORBIDDEN)

        total_bookings = stadium.bookings.count()
        completed = stadium.bookings.filter(status='COMPLETED').count()
        cancelled = stadium.bookings.filter(status='CANCELLED').count()
        revenue = stadium.bookings.filter(status='COMPLETED').aggregate(total=Sum('total_price'))['total'] or 0

        return Response({
            'total_bookings': total_bookings,
            'completed_bookings': completed,
            'cancelled_bookings': cancelled,
            'total_revenue': revenue
        })

    @action(detail=True, methods=['post'])
    def add_manager(self, request, pk=None):
        stadium = self.get_object()

        if not (request.user.is_admin or (request.user.is_stadium_owner and stadium.owner == request.user)):
            return Response({"detail": "Only stadium owners can assign managers."},
                            status=status.HTTP_403_FORBIDDEN)

        manager_id = request.data.get('manager_id')
        if not manager_id:
            return Response({"detail": "Manager ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            manager = User.objects.get(id=manager_id, role='STADIUM_MANAGER')
        except User.DoesNotExist:
            return Response({"detail": "User not found or is not a stadium manager."},
                            status=status.HTTP_404_NOT_FOUND)

        stadium_manager, created = StadiumManager.objects.get_or_create(
            stadium=stadium,
            manager=manager,
            defaults={'is_active': True}
        )

        if not created:
            stadium_manager.is_active = True
            stadium_manager.save()
            message = "Manager re-assigned to this stadium."
        else:
            message = "Manager assigned to this stadium."

        return Response({"detail": message}, status=status.HTTP_200_OK)
