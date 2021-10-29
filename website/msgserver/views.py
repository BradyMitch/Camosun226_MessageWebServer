from django.shortcuts import render
from msgserver.models import Message
from django.http import HttpResponse

# Create your views here.
def get_message(request, key):
    message = Message.objects.filter(key=key)
    if (len(message) == 1):
        msg = str(message[0].msg)
        return HttpResponse(f"Message: {msg}")
    else:
        return HttpResponse("No message found.")
