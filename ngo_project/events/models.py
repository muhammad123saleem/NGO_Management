import random
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

def generate_ticket_number():
    """Generate a unique 6-digit ticket number."""
    while True:
        ticket = str(random.randint(100000, 999999))
        if not EventRegistration.objects.filter(ticket_number=ticket).exists():
            return ticket

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    ticket_number = models.CharField(max_length=6, unique=True, blank=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    member_count = models.PositiveIntegerField(default=1, help_text="Number of attendees")

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = generate_ticket_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.event.name} - Ticket: {self.ticket_number}"
