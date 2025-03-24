from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    path('', views.donation_page, name='donation'),
    path('form/', views.donation_form, name='donation_form'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.donation_success, name='donation_success'),
    path('cancel/', views.donation_cancel, name='donation_cancel'),
    path('fetch-stripe/<int:donation_id>/', views.fetch_stripe_transaction, name='fetch_stripe_transaction'),
]
