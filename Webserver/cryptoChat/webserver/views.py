import imp
from django.shortcuts import render
#from webserver.models import Post
from django.utils import timezone
from django.http import HttpResponse
from pymongo import MongoClient
from django import forms
from django.views.decorators.csrf import csrf_protect

from kiwi import get_sentiment,evaluate_features

client = MongoClient('localhost', 27017)
db = client['Kiwichat']
send = True

# Create your views here.
CSRF_COOKIE_SECURE = False
def index(request):
    return render(request,'HTML/index.html',{})

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
        print "message: ",message
        bar =evaluate_features(message)
        result = db.chats.insert_one(
        {
            "message":message,
            "polarity":bar
        }
        )
        if(send == True):
                print "forward"

        return HttpResponse(bar)
