"""
URL configuration for ngo_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    # Admin URLs
    path('admin/', admin.site.urls),

    # App URL includes
    path('accounts/', include('accounts.urls')),       # accounts app
    path('donations/', include('donations.urls')),       # donations app
    path('events/', include('events.urls', namespace='events')),  # events app with namespace
    path('messaging/', include('messaging.urls')),       # messaging app
    path('volunteer/', include('volunteer.urls')),       # volunteer app
    path('reports/', include('reports.urls', namespace='reports')),

    # General pages using TemplateView
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('contact/', TemplateView.as_view(template_name='contact/contact.html'), name='contact'),
    path('faq/', TemplateView.as_view(template_name='faq/faq.html'), name='faq'),
]
