# volunteers/urls.py
from django.urls import path
from .views import volunteer_signup

urlpatterns = [
    path('', volunteer_signup, name='volunteer'),
]
