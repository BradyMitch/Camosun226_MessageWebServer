from django.shortcuts import render
from msgserver.models import Message
from msgserver.models import JSONEncode
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
import json

# PURPOSE:
# Create message form with all fields (key, msg)
# When submitted, link to get_all_messages url
#
# PARAMETERS:
# 'CreateView' allows us to use a form and create new key-value pairs in the database
#
# RETURN/SIDE EFFECTS/NOTES:
# Called by going to url '/msgserver/create'
#
class create_message(CreateView):
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('get_all_messages')

# PURPOSE:
# Update msg field of a given key
# When submitted, link to get_all_messages url
#
# PARAMETERS:
# 'UpdateView' allows us to use a form and update key-value pairs in the database
#
# RETURN/SIDE EFFECTS/NOTES:
# Called by going to url '/msgserver/update/<key>'
#
class update_message(UpdateView):
    model = Message
    fields = ['msg']
    success_url = reverse_lazy('get_all_messages')

# PURPOSE:
# Given a key, return the msg associated with given key
# Looks through key-msg pairs to find a msg associated with the given key
#
# PARAMETERS:
# 'request' is GET
# 'key' is the key from the url
#
# RETURN/SIDE EFFECTS/NOTES:
# Called by going to url '/msgserver/get/<key>'
# Returns HttpResponse of json encoded msg
#
def get_message(request, key):
    message = Message.objects.filter(key=key)
    if (len(message) == 1):
        jsonMsg = json.dumps(message[0], cls=JSONEncode)
        return HttpResponse(jsonMsg)
    else:
        return HttpResponse("No message found.")

# PURPOSE:
# Displays an array of all key-msg pairs in json format
#
# PARAMETERS:
# 'request' is GET
#
# RETURN/SIDE EFFECTS/NOTES:
# Called by going to url '/msgserver'
# Returns HttpResponse of json encoded data
#
def get_all_messages(request):
    messages = Message.objects.all()
    jsonArray = []
    for message in messages:
        jsonArray.append(json.dumps(message, cls=JSONEncode))
    return HttpResponse(json.dumps(jsonArray, cls=JSONEncode))