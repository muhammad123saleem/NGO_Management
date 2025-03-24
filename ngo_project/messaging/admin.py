from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.contrib import admin
from django.http import JsonResponse
from .models import ChatMessage
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "sent_at", "is_admin")
    list_filter = ("is_admin",)
    search_fields = ("user__email", "message")

    def get_urls(self):
        """Override default Django Admin URLs with a custom chat interface."""
        urls = super().get_urls()
        custom_urls = [
            path("chat-interface/", self.admin_site.admin_view(self.chat_interface), name="admin_chat_interface"),
            path("get-messages/<int:user_id>/", self.admin_site.admin_view(self.get_messages), name="admin_get_messages"),
            path("send-message/", self.admin_site.admin_view(self.send_message), name="admin_send_message"),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        """Redirect Chat Messages menu in Django Admin to custom chat interface."""
        return redirect("admin_chat")  # Use 'admin_chat' instead of 'admin_chat_interface'

    def chat_interface(self, request):
        """Renders the chat interface for admin."""
        users = User.objects.all()
        return render(request, "faq/admin_chat.html", {"users": users})

    def get_messages(self, request, user_id):
        """Fetch chat messages for a specific user."""
        messages = ChatMessage.objects.filter(user_id=user_id).order_by("sent_at")
        messages_data = [
            {
                "message": msg.message,
                "is_admin": msg.is_admin,
                "sent_at": msg.sent_at.strftime("%Y-%m-%d %H:%M")
            }
            for msg in messages
        ]
        return JsonResponse({"messages": messages_data})

    @method_decorator(csrf_exempt)
    def send_message(self, request):
        """Admin sends a message to the user."""
        if request.method == "POST":
            user_id = request.POST.get("user_id")
            message_text = request.POST.get("message", "").strip()

            if not message_text:
                return JsonResponse({"status": "error", "message": "⚠️ Message cannot be empty."}, status=400)

            user = User.objects.get(id=user_id)
            ChatMessage.objects.create(user=user, message=message_text, is_admin=True)

            return JsonResponse({"status": "success", "message": "Message sent!"})

        return JsonResponse({"status": "error", "message": "Invalid request."}, status=400)

admin.site.register(ChatMessage, ChatMessageAdmin)
