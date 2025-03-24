from django.db import models
from donations.models import Donation
from events.models import Event, EventRegistration
from volunteer.models import Volunteer, VolunteerAssignment
from django.db.models import Sum

class Reports(models.Model):
    """ Stores summarized reports for tracking NGO activities """

    report_name = models.CharField(max_length=255, unique=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    total_donations = models.PositiveIntegerField(default=0)
    total_donated_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_events = models.PositiveIntegerField(default=0)
    total_event_registrations = models.PositiveIntegerField(default=0)
    total_volunteers = models.PositiveIntegerField(default=0)
    total_volunteer_assignments = models.PositiveIntegerField(default=0)

    def update_report(self):
        """ Fetches live data and updates report fields """
        self.total_donations = Donation.objects.count()
        self.total_donated_amount = Donation.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        self.total_events = Event.objects.count()
        self.total_event_registrations = EventRegistration.objects.count()
        self.total_volunteers = Volunteer.objects.count()
        self.total_volunteer_assignments = VolunteerAssignment.objects.count()
        self.save()

    def __str__(self):
        return f"Report: {self.report_name} ({self.generated_at.strftime('%Y-%m-%d')})"
