from django.contrib import admin
from .models import SportType, Amenity, Stadium, StadiumImage, StadiumManager


@admin.register(SportType)
class SportTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Stadium)
class StadiumAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'owner', 'price_per_hour', 'opening_time', 'closing_time', 'is_active')
    list_filter = ('sport_types', 'owner', 'is_active')
    search_fields = ('name', 'address', 'owner__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(StadiumImage)
class StadiumImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'stadium', 'image', 'is_primary')
    list_filter = ('stadium', 'is_primary')
    search_fields = ('stadium__name',)
    readonly_fields = ('stadium',)


@admin.register(StadiumManager)
class StadiumManagerAdmin(admin.ModelAdmin):
    list_display = ('id', 'stadium', 'manager', 'is_active')
    list_filter = ('stadium', 'manager', 'is_active')
    search_fields = ('stadium__name', 'manager__email')
