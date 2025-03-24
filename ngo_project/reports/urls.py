from django.urls import path
from . import views

app_name = "reports"  # Ensure app_name is set

urlpatterns = [
    path('dashboard/', views.reports_dashboard, name='reports_dashboard'),
    path('export/csv/', views.export_reports_csv, name='export_reports_csv'),  # Ensure this line is included
]
