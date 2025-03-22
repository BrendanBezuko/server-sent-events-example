from django.db import models

# Create your models here.


class Booking(models.Model):
    slot = models.DateTimeField(unique=True)
    user = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.slot}"
