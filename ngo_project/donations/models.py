from django.db import models
from accounts.models import CustomUser

class Donation(models.Model):
    DONATION_FREQUENCY = [
        ('one-time', 'One-Time'),
        ('recurring', 'Recurring'),
    ]

    PAYMENT_METHODS = [
        ('stripe', 'Stripe'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.CharField(max_length=10, choices=DONATION_FREQUENCY, default='one-time')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='stripe')
    transaction_id = models.CharField(max_length=255, unique=True, blank=True, null=True)  # Store Stripe Payment Intent ID
    date_donated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation - {self.amount} USD by {self.user.email if self.user else 'Guest'}"
