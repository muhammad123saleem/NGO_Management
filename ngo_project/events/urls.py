from django.urls import path
from .views import events_view, event_detail, event_register

app_name = 'events'

urlpatterns = [
    path('', events_view, name='events'),
    path('<int:event_id>/', event_detail, name='event_detail'),
    path('<int:event_id>/register/', event_register, name='event_register'),
]
