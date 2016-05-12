import imp
from django.shortcuts import render
#from webserver.models import Post
from django.utils import timezone
from django.http import HttpResponse
from pymongo import MongoClient
from django import forms
from django.views.decorators.csrf import csrf_protect

from kiwi import get_sentiment,evaluate_features
from gcm import *
import urllib3
#urllib3.disable_warnings()

client = MongoClient('localhost', 27017)
db = client['Kiwichat']
send = True
threshold_limit = 5

# Create your views here.
CSRF_COOKIE_SECURE = False
def index(request):
    return render(request,'HTML/index.html',{})

def register_device(request):
    return render(request,'HTML/register_device.html',{})

def process_message(request):
    cursor = db.chats.find()
    for document in cursor:
        print(document['polarity'])
    return HttpResponse(document['polarity'])

@csrf_protect
def send_message(request):
    global send
    if request.method == 'POST':
        message = request.POST.get("message")
        deviceId = request.POST.get("deviceId")
        print "message: ",message
        bar =evaluate_features(message)
        result = db.chats.insert_one(
        {
            "message":message,
            "polarity":bar
        }
        )
        cursor = db.threshold.find_one({'deviceId':deviceId })
        threshold_value = cursor['threshold_value']
        print "bar",bar
        if(bar[0] == 'neg'):
            threshold_value = threshold_value + 1
            result = db.threshold.update_one(
            {"deviceId": deviceId},
            {
                "$set": {
                    "threshold_value": threshold_value
                },
            }
            )
        print "Threshold: ",threshold_value
        if(threshold_value <= threshold_limit):
                gcm = GCM("AIzaSyDL4b5qf3_iUGuqi__BGiQ2HKud5iA14rg")
                data = {'the_message': message}
                reg_id = 'APA91bFxz8_U87jN2fO1zRo-rXX2AjO8NBNqoLKunSyNYI2mZhdMkoXS9JWekDlrQk5cvi6T00QaFuhRHig8QFbhV49Kwk5GXu-MEtCFaj2ECq60D8hksJOc83pp99GwHdW3CGD$'
                gcm.plaintext_request(registration_id=reg_id, data=data)
                print "forward"

        return HttpResponse(bar)

@csrf_protect
def process_registeration(request):
    if request.method == 'POST':
        deviceId = request.POST.get("deviceId")
        print "deviceId: ",deviceId
        result = db.threshold.insert_one(
        {
            "deviceId":deviceId,
            "threshold_value":0
        }
        )
        return HttpResponse("Success")
