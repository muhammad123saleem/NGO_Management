import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .forms import DonationForm
from .models import Donation

# Set up Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY


def donation_page(request):
    """Loads the main donation page."""
    return render(request, 'donations/donation.html')


def donation_form(request):
    """Loads the donation form page and handles form submission."""
    form = DonationForm()

    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.save()

            # Redirect to Stripe Checkout
            return redirect('donations:process_payment', donation_id=donation.id)

    return render(request, 'donations/donation_form.html', {'form': form, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})


def create_checkout_session(request):
    """Handles Stripe payment processing for one-time and recurring donations."""
    if request.method == "POST":
        amount = int(request.POST.get("amount")) * 100  # Convert to cents
        frequency = request.POST.get("frequency")  # One-time or recurring

        # Define Stripe line items
        line_items = [{
            'price_data': {
                'currency': 'usd',
                'unit_amount': amount,
                'product_data': {'name': "NGO Donation"},
            },
            'quantity': 1,
        }]

        # Payment mode: one-time or subscription
        mode = "payment"

        # ✅ FIX: Use a Stripe price ID for recurring payments
        if frequency == "recurring":
            price_id = settings.STRIPE_RECURRING_PRICE_ID  # Fetch from settings
            if not price_id:
                return JsonResponse({'error': 'No Stripe recurring price ID configured'}, status=400)

            line_items = [{
                'price': price_id,  # Use pre-configured Stripe recurring price ID
                'quantity': 1,
            }]
            mode = "subscription"

        # Create Stripe session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode=mode,
            success_url=request.build_absolute_uri('/donations/success/') + f"?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=request.build_absolute_uri('/donations/cancel/'),
        )

        # Store transaction ID in database
        donation = Donation.objects.create(
            amount=amount / 100,  # Convert from cents
            frequency=frequency,
            payment_method='stripe',
            transaction_id=session.id,
        )

        return JsonResponse({'sessionId': session.id})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def donation_success(request):
    """Loads a success message after donation submission."""
    messages.success(request, "Your donation was successful! Thank you for your support.")
    return render(request, 'donations/donation_success.html')


def donation_cancel(request):
    """Handles canceled donation transactions."""
    messages.warning(request, "Your donation was canceled. Please try again.")
    return render(request, 'donations/donation_cancel.html')

def fetch_stripe_transaction(request, donation_id):
    """Fetch payment details from Stripe API for a specific donation."""
    try:
        donation = Donation.objects.get(id=donation_id)
        if not donation.transaction_id:
            return JsonResponse({"error": "No transaction ID found for this donation."}, status=404)

        # Retrieve Stripe session and payment intent
        session = stripe.checkout.Session.retrieve(donation.transaction_id)
        payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)

        # Extract payment details
        transaction_data = {
            "id": payment_intent.id,
            "amount_received": payment_intent.amount_received / 100,  # Convert from cents
            "currency": payment_intent.currency.upper(),
            "status": payment_intent.status.upper(),
            "payment_method": payment_intent.payment_method_types[0].upper(),
            "created_at": payment_intent.created,
        }

        return JsonResponse(transaction_data)

    except stripe.error.StripeError as e:
        return JsonResponse({"error": str(e)}, status=400)

