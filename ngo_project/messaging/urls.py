from django.urls import path
from . import views

urlpatterns = [
    path('faq/', views.faq_view, name='faq'),
    path('get-messages/', views.get_messages, name='get_messages'),
    path('send-message/', views.send_message, name='send_message'),
    path('admin/chat/', views.admin_chat_view, name='admin_chat'),
    path('admin/get-messages/<int:user_id>/', views.get_messages_admin, name='get_messages_admin'),
    path('admin/send-message/', views.send_admin_message, name='send_admin_message'),
]
