from django.contrib import admin
from .models import Donation
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY  # Set Stripe API Key


class DonationAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'get_donor_email', 'amount', 'frequency', 'payment_method', 'transaction_id', 'get_stripe_status',
    'date_donated')
    list_filter = ('frequency', 'payment_method', 'date_donated')  # ✅ Replaced 'donation_type' with 'frequency'
    search_fields = ('user__email', 'transaction_id', 'amount')
    readonly_fields = ('date_donated', 'transaction_id')

    def get_donor_email(self, obj):
        """Fetch donor email from CustomUser"""
        return obj.user.email if obj.user else "Anonymous"

    get_donor_email.short_description = "Donor Email"

    def get_stripe_status(self, obj):
        """Fetch Stripe payment status for this donation."""
        if not obj.transaction_id:
            return "No Transaction ID"

        try:
            session = stripe.checkout.Session.retrieve(obj.transaction_id)
            payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)
            return payment_intent.status.upper()
        except stripe.error.StripeError:
            return "Error Fetching Data"

    get_stripe_status.short_description = "Stripe Payment Status"

    def has_delete_permission(self, request, obj=None):
        """Prevent accidental deletion of donation records"""
        return False


admin.site.register(Donation, DonationAdmin)
