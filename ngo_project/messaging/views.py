from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import ChatMessage
from accounts.models import CustomUser  # Use the CustomUser model

@login_required
def faq_view(request):
    """Displays the FAQ page with user chat messages"""
    user_messages = ChatMessage.objects.filter(user=request.user).order_by("sent_at")
    return render(request, "faq/faq.html", {"chat_messages": user_messages})

@login_required
def get_messages(request):
    """Fetches chat messages for the logged-in user"""
    chat_messages = ChatMessage.objects.filter(user=request.user).order_by("sent_at")

    messages_data = [
        {"message": msg.message, "is_admin": msg.is_admin, "sent_at": msg.sent_at.strftime("%Y-%m-%d %H:%M")}
        for msg in chat_messages
    ]

    return JsonResponse({"messages": messages_data})

@login_required
@csrf_exempt
def send_message(request):
    """Allows users to send a message to admin"""
    if request.method == "POST":
        message_text = request.POST.get("message", "").strip()
        if not message_text:
            return JsonResponse({"status": "error", "message": "⚠️ Message cannot be empty."}, status=400)

        ChatMessage.objects.create(user=request.user, message=message_text, is_admin=False)
        return JsonResponse({"status": "success", "message": "Message sent!"})

    return JsonResponse({"status": "error", "message": "Invalid request."}, status=400)

@login_required
def admin_chat_view(request):
    """Displays the admin chat interface where they can select users"""
    if not request.user.is_superuser:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    users = CustomUser.objects.filter(chatmessage__isnull=False).distinct()
    return render(request, "faq/admin_chat.html", {"users": users})

@login_required
def get_messages_admin(request, user_id):
    """Fetches chat messages between admin and a specific user"""
    if not request.user.is_superuser:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    messages = ChatMessage.objects.filter(user_id=user_id).order_by("sent_at")
    message_data = [
        {"message": msg.message, "is_admin": msg.is_admin, "sent_at": msg.sent_at.strftime("%Y-%m-%d %H:%M")}
        for msg in messages
    ]

    return JsonResponse({"messages": message_data})

@login_required
@csrf_exempt
def send_admin_message(request):
    """Allows admin to send a message to a specific user"""
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        message_text = request.POST.get("message", "").strip()

        if not message_text:
            return JsonResponse({"status": "error", "message": "⚠️ Message cannot be empty."}, status=400)

        user = get_object_or_404(CustomUser, id=user_id)
        ChatMessage.objects.create(user=user, message=message_text, is_admin=True)

        return JsonResponse({"status": "success", "message": "Message sent!"})

    return JsonResponse({"status": "error", "message": "Invalid request."}, status=400)
