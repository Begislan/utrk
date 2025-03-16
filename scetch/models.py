from django.db import models
from django.contrib.auth.models import User

class QueueSlot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)  # Флаг занятости

    def __str__(self):
        status = "Занято" if self.is_booked else "Свободно"
        return f"{self.date} {self.start_time}-{self.end_time} ({status})"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.OneToOneField(QueueSlot, on_delete=models.CASCADE)  # Один слот - одна бронь
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.slot}"
