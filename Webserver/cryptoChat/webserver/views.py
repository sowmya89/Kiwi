import imp
from django.shortcuts import render
#from webserver.models import Post
from django.utils import timezone
from django.http import HttpResponse
from pymongo import MongoClient
from django import forms
from django.views.decorators.csrf import csrf_protect

from kiwi import get_sentiment

# Create your views here.
CSRF_COOKIE_SECURE = False
def index(request):
    return render(request,'HTML/index.html',{})

def process_message(request):
    client = MongoClient('localhost', 27017)
    db = client['cmpe280_ajax']
    cursor = db.user_data.find()
    for document in cursor:
        print(document)
    return HttpResponse(document)

@csrf_protect
def send_message(request):
    if request.method == 'POST':
        message = request.POST.get("message")
        print "message: ",message
        bar = get_sentiment(message)
        return HttpResponse(bar)
