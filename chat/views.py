from django.shortcuts import render, redirect
from .models import ChatSession, Message
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
import uuid


def chat_home(request):
    return render(request, "chat/home.html")
    

def start_chat(request):
    if request.method == "POST":
        name = request.POST.get("name").strip()

        if not name:
            return render(request, "chat/name.html", {"error": "Name is required"})

        # create new session
        session_key = str(uuid.uuid4())
        request.session["chat_session_id"] = session_key

        chat = ChatSession.objects.create(
            name=name,
            session_id=session_key
        )

        return redirect("chat_room")

    return render(request, "chat/name.html")    

def search_chat(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()

        if not name:
            return render(request, "chat/home.html", {
                "error": "Please enter a name."
            })

        try:
            chat = ChatSession.objects.get(name=name)
            request.session["chat_session_id"] = chat.session_id
            return redirect("chat_room")
        except ChatSession.DoesNotExist:
            # Only show error on failed POST
            return render(request, "chat/home.html", {
                "error": "No chat found with that name."
            })

    # GET request (page load or refresh): no error shown
    return render(request, "chat/home.html")
    

def chat_room(request):
    session_id = request.session.get("chat_session_id")
    
    if not session_id:
        return redirect("chat_home")

    try:
        chat = ChatSession.objects.get(session_id=session_id)
    except ChatSession.DoesNotExist:
        return redirect("chat_home")

    messages = chat.messages.order_by("timestamp")

    return render(request, "chat/chat.html", {"messages": messages, "chat": chat})            
        
def send_message(request):
    if request.method == "POST":
        session_id = request.session.get("chat_session_id")

        chat = ChatSession.objects.get(session_id=session_id)
        text = request.POST["text"]

        Message.objects.create(chat=chat, sender="user", text=text)
        return redirect("chat_room")
        
def fetch_messages(request):
    session_id = request.session.get("chat_session_id")

    if not session_id:
        return JsonResponse({"messages": []})  # user has no chat session

    try:
        chat = ChatSession.objects.get(session_id=session_id)
    except ChatSession.DoesNotExist:
        return JsonResponse({"messages": []})

    msgs = chat.messages.order_by("timestamp")

    data = [
        {
            "sender": m.sender,
            "text": m.text,
            "timestamp": m.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for m in msgs
    ]

    return JsonResponse({"messages": data})