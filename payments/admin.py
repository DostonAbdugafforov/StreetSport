from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount', 'payment_type', 'status', 'transaction_id', 'created_at', 'updated_at')
    list_filter = ('payment_type', 'status', 'created_at')
    search_fields = ('booking__id', 'transaction_id', 'amount')
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset
