from django.contrib import admin
from .models import Event, EventRegistration

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location')
    search_fields = ('name', 'location')

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'ticket_number', 'name', 'phone_number', 'member_count', 'date_registered')
    list_filter = ('event', 'date_registered')
    search_fields = ('event__name', 'ticket_number', 'name', 'phone_number')


admin.site.register(Event, EventAdmin)
