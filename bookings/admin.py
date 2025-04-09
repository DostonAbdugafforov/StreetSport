from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'stadium', 'created_at']
    search_fields = ['user__username', 'stadium__name']
    list_filter = ['stadium', 'user']


