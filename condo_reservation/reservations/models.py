from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    ROOM_TYPES = (
        ('studio', 'Studio'),
        ('1-bed', '1 Bedroom'),
        ('2-bed', '2 Bedrooms'),
    )
    
    type = models.CharField(max_length=20, choices=ROOM_TYPES)
    floor = models.IntegerField()
    unit = models.CharField(max_length=3)  # New field for unit
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_booked = models.BooleanField(default=False)
    images = models.JSONField(default=list)  # Store image URLs

    def __str__(self):
        return f"{self.type} on floor {self.floor} - Unit {self.unit} - ${self.price}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
