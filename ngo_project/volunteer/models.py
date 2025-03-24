from django.db import models

class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    message = models.TextField()
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class VolunteerAssignment(models.Model):
    volunteer = models.ForeignKey(
        Volunteer,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    # Use a string reference to the Event model from the events app
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    task_description = models.TextField(
        help_text="Describe the task assigned to this volunteer."
    )
    assigned_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.volunteer.name} - {self.event.name}"
