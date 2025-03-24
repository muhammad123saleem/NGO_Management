from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.db.models import Sum
from donations.models import Donation
from events.models import Event
from volunteer.models import Volunteer, VolunteerAssignment
import csv
import json

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_superuser, login_url='index')
def reports_dashboard(request):
    total_donations = Donation.objects.count()
    total_donated = Donation.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_events = Event.objects.count()
    total_volunteers = Volunteer.objects.count()

    donations = Donation.objects.all().order_by('-date_donated')[:5]  # Changed from 'date' to 'date_donated'
    events = Event.objects.all()
    volunteer_tasks = VolunteerAssignment.objects.all()

    # Prepare chart data
    donation_labels = [donation.date_donated.strftime("%Y-%m-%d") for donation in donations]

    # Convert Decimal to float (Fix the JSON issue!)
    donation_values = [float(donation.amount) for donation in donations]

    # Debugging prints (check your terminal after restarting server)
    print("Donation Labels:", donation_labels)
    print("Donation Values:", donation_values)

    event_labels = [event.date.strftime("%Y-%m-%d") for event in events]
    event_values = [Event.objects.filter(date=event.date).count() for event in events]

    context = {
        "total_donations": total_donations,
        "total_donated": total_donated,
        "total_events": total_events,
        "total_volunteers": total_volunteers,
        "donations": donations,
        "events": events,
        "volunteer_tasks": volunteer_tasks,
        "donation_labels": json.dumps(donation_labels),
        "donation_values": json.dumps(donation_values),
        "event_labels": event_labels,
        "event_values": event_values,
    }

    return render(request, "reports_dashboard.html", context)


@user_passes_test(is_superuser, login_url='index')
def export_reports_csv(request):
    """Exports reports data as CSV file."""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="reports.csv"'
    writer = csv.writer(response)
    writer.writerow(["Category", "Details"])

    # Total Donations
    total_donations = Donation.objects.count()
    total_donated = sum(donation.amount for donation in Donation.objects.all())
    writer.writerow(["Total Donations", total_donations])
    writer.writerow(["Total Amount Donated ($)", total_donated])

    # Events
    writer.writerow(["Total Events", Event.objects.count()])
    for event in Event.objects.all():
        writer.writerow(["Event", f"{event.name} - {event.date}"])

    # Volunteers
    writer.writerow(["Total Volunteers", Volunteer.objects.count()])
    for task in VolunteerAssignment.objects.all():
        writer.writerow(["Volunteer Task", f"{task.volunteer.name} - {task.task_description}"])

    return response

