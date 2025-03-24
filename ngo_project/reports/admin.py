from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.http import HttpResponse
import csv
from django.db.models import Sum
from donations.models import Donation
from events.models import Event, EventRegistration
from volunteer.models import Volunteer, VolunteerAssignment
from .models import Reports

class ReportsAdmin(admin.ModelAdmin):
    """ Custom Admin Panel Reports Dashboard """
    change_list_template = "admin/reports_dashboard.html"

    def changelist_view(self, request, extra_context=None):
        """Redirects to the Reports Dashboard in Admin Panel"""
        return redirect(reverse("reports:reports_dashboard"))

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.report_dashboard), name="reports_dashboard"),
            path('export/csv/', self.admin_site.admin_view(self.export_csv), name="export_reports_csv"),
        ]
        return custom_urls + urls

    def report_dashboard(self, request):
        """ Render reports dashboard in Django Admin Panel """

        # Fetch Data
        total_donations = Donation.objects.count()
        total_events = Event.objects.count()
        total_volunteers = Volunteer.objects.count()
        total_event_registrations = EventRegistration.objects.count()
        total_donated_amount = Donation.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        total_assignments = VolunteerAssignment.objects.count()

        context = {
            'donations': total_donations,
            'events': total_events,
            'volunteers': total_volunteers,
            'event_registrations': total_event_registrations,
            'total_donated': total_donated_amount,
            'total_assignments': total_assignments,
        }
        return TemplateResponse(request, "reports_dashboard.html", context)  # Global Template Path

    def export_csv(self, request):
        """ Export all reports data as a CSV file """

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="ngo_reports.csv"'

        writer = csv.writer(response)
        writer.writerow(["Category", "Count", "Total Donations ($)"])

        # Fetch data dynamically
        total_donations = Donation.objects.count()
        total_donated_amount = Donation.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        total_events = Event.objects.count()
        total_volunteers = Volunteer.objects.count()
        total_event_registrations = EventRegistration.objects.count()
        total_assignments = VolunteerAssignment.objects.count()

        # Write data to CSV
        writer.writerow(["Total Donations", total_donations, total_donated_amount])
        writer.writerow(["Total Events", total_events, "N/A"])
        writer.writerow(["Total Volunteers", total_volunteers, "N/A"])
        writer.writerow(["Event Registrations", total_event_registrations, "N/A"])
        writer.writerow(["Volunteer Assignments", total_assignments, "N/A"])

        return response

# ✅ Register the Reports model in Django Admin Panel
admin.site.register(Reports, ReportsAdmin)
