from django.db import models
from django.contrib.auth import get_user_model
from stadiums.models import Stadium

User = get_user_model()


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.stadium.name} - {self.date}"

