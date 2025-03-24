from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Event, EventRegistration
from .forms import EventRegistrationForm

def events_view(request):
    # Show upcoming events
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'events/events.html', {'events': events})

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    # See if the current user is already registered
    registration = EventRegistration.objects.filter(event=event, user=request.user).first()
    return render(request, 'events/event_detail.html', {
        'event': event,
        'registration': registration,
    })

def event_register(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.user = request.user
            registration.save()
            messages.success(request, f"Registration successful! Your Ticket Number: {registration.ticket_number}")
            return redirect('events:event_detail', event_id=event.id)
    else:
        form = EventRegistrationForm()

    return render(request, 'events/event_register.html', {'event': event, 'form': form})  # ✅ Ensure the correct path

