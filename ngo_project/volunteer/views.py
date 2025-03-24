# volunteer/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .forms import VolunteerForm
from .models import Volunteer
from events.models import Event
from volunteer.models import VolunteerAssignment
from django.utils.timezone import now

def volunteer_signup(request):
    volunteer = None
    if request.user.is_authenticated:
        volunteer = Volunteer.objects.filter(email=request.user.email).first()

    if request.method == 'POST':
        if volunteer:
            messages.info(request, "You are already registered as a volunteer!")
            return redirect('volunteer')
        else:
            form = VolunteerForm(request.POST)
            if form.is_valid():
                volunteer = form.save()
                messages.success(request, "Thank you for becoming a volunteer!")
                return redirect('volunteer')
    else:
        form = VolunteerForm() if not volunteer else None

    upcoming_events = Event.objects.filter(date__gte=timezone.now())
    assignments = VolunteerAssignment.objects.filter(volunteer=volunteer) if volunteer else None

    context = {
        'form': form,
        'volunteer': volunteer,
        'upcoming_events': upcoming_events,
        'assignments': assignments,
    }
    return render(request, 'volunteer/volunteer.html', context)

def volunteer_view(request):
    return render(request, "volunteer.html", {"timestamp": now().timestamp()})

