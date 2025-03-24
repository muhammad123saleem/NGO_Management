from django import forms
from .models import EventRegistration

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['name', 'phone_number', 'address', 'member_count']
        labels = {
            'name': 'Your Full Name',
            'phone_number': 'Phone Number',
            'address': 'Address',
            'member_count': 'Number of Attendees',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}),
            'member_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
