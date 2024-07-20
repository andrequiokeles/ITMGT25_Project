from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Room(models.Model):
    ROOM_TYPES = (
        ('studio', 'Studio'),
        ('1-bed', '1 Bedroom'),
        ('2-bed', '2 Bedrooms'),
    )
    
    unit = models.CharField(max_length=10)
    type = models.CharField(max_length=20, choices=ROOM_TYPES)
    floor = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_booked = models.BooleanField(default=False)
    images = models.JSONField(default=list)  # Storing images as JSON

    def __str__(self):
        return f'{self.get_type_display()} - Room {self.unit} on floor {self.floor} - ₱{self.price}'

    def is_available(self, start_date, end_date):
        bookings = self.booking_set.filter(
            models.Q(start_date__lte=end_date) & models.Q(end_date__gte=start_date)
        )
        return not bookings.exists()

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_canceled = models.BooleanField(default=False)
    proof_of_payment = models.ImageField(upload_to='proofs/', blank=True, null=True)  # Adjust as needed

    def save(self, *args, **kwargs):
        if self.start_date < date.today():
            raise ValueError("Start date cannot be in the past.")
        if self.end_date <= self.start_date:
            raise ValueError("End date must be after the start date.")
        if not self.is_canceled and not self.room.is_available(self.start_date, self.end_date):
            raise ValueError("The room is not available for the selected dates.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Booking by {self.user.username} for Room {self.room.unit}'

class Transaction(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transaction for Booking {self.booking.id} - Amount: ₱{self.amount} on {self.transaction_date}'

    class Meta:
        ordering = ['-transaction_date']

class ProofOfPayment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='proofs_of_payment/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Proof of Payment for Booking {self.booking.id}'
