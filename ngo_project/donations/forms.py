from django import forms
from .models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount', 'frequency', 'payment_method']  # ✅ Changed 'donation_type' to 'frequency'
        labels = {
            'amount': 'Donation Amount ($)',
            'frequency': 'Donation Type',  # ✅ Updated label
            'payment_method': 'Payment Method',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'Enter donation amount'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),  # ✅ Updated field
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }
