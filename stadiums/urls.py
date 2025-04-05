from django.urls import path, include
from rest_framework import routers

from .views import StadiumViewSet

router = routers.DefaultRouter()
router.register(r'stadiums', StadiumViewSet)


urlpatterns = [
    path('', include(router.urls)),
]