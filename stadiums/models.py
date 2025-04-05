from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Stadium(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stadiums')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

