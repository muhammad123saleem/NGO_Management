# volunteers/admin.py
from django.contrib import admin
from django.apps import apps
from .models import Volunteer, VolunteerAssignment

# Dynamically get the Event model from the events app
Event = apps.get_model('events', 'Event')

class VolunteerAssignmentInline(admin.TabularInline):
    model = VolunteerAssignment
    extra = 1
    fields = ('event', 'task_description', 'due_date', 'completed')

class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'joined_at')
    search_fields = ('name', 'email')
    list_filter = ('joined_at',)
    inlines = [VolunteerAssignmentInline]

admin.site.register(Volunteer, VolunteerAdmin)

@admin.register(VolunteerAssignment)
class VolunteerAssignmentAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'event', 'task_description', 'due_date', 'completed')
    list_filter = ('completed', 'event')
    search_fields = ('volunteer__name', 'event__name')
