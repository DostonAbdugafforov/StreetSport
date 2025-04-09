from django.db import models
from accounts.models import User


class SportType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Amenity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Stadium(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_stadiums')
    sport_types = models.ManyToManyField(SportType, related_name='stadiums')
    amenities = models.ManyToManyField(Amenity, related_name='stadiums')
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class StadiumImage(models.Model):
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='stadium_images/')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.stadium.name}"


class StadiumManager(models.Model):
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, related_name='managers')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_stadiums')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('stadium', 'manager')

    def __str__(self):
        return f"{self.manager.name} manages {self.stadium.name}"
