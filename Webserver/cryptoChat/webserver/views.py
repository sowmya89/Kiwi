import imp
from django.shortcuts import render
#from webserver.models import Post
from django.utils import timezone
from django.http import HttpResponse
from pymongo import MongoClient
from django import forms
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from kiwi import get_sentiment,evaluate_features,evaluate_small_features
from twilio.rest import TwilioRestClient
from gcm import *
import urllib3
import json
from django.http import JsonResponse
from bson import json_util
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

def process_emergency_message(number,name,receiver):
    # Find these values at https://twilio.com/user/account
    account_sid = "AC2a781fd7b2047a8d02bf4800fef9a244"
    auth_token = "c6518ef76c1301cc694db02e74ce6430"
    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(to=number, from_="+15555555555",
                                         body="Hi "+ receiver +", \n This is to notify that "+ name + " is receiving in appropriate messages. You are getting this message since you have been added as an emergency contact !" )

@csrf_exempt
def test_message(request):
    global send
    if request.method == 'POST':
        message = request.POST.get("message")

        print "message: ",message

        if len(message.split()) <= 3:
			bar = evaluate_small_features(message)
        else:
    		bar = evaluate_features(message)

        return HttpResponse(bar)

@csrf_exempt
def getuser(request):
    global send
    if request.method == 'POST':
        phoneNumber = request.POST.get("phoneNumber")
	all_records = []
	json_data = {}
        data =  db.threshold.find({ phoneNumber: { "$ne": phoneNumber }},{"phoneNumber" : 1, "firstName": 1, "_id" : 0})
	for record in data:
		json_data['phoneNumber'] = record.get("phoneNumber")
		json_data['firstName'] = record.get("firstName")
		all_records.append(json_data)
	json_data = json.dumps(all_records)

	print "data: ",json_data
        return JsonResponse(json_data,safe=False)

@csrf_exempt
def send_message(request):
    global send
    if request.method == 'POST':
        message = request.POST.get("message")
        senderPhoneNumber = request.POST.get("senderPhoneNumber")
        senderName = request.POST.get("senderName")
        receiverPhoneNumber = request.POST.get("receiverPhoneNumber")

        cursor = db.threshold.find_one({'phoneNumber':senderPhoneNumber })
        threshold_value = cursor['threshold_value']
        blocked = cursor['blocked']

        cursor = db.threshold.find_one({'phoneNumber':receiverPhoneNumber })
        deviceId = cursor['deviceId']

        print "message: ",message

        if len(message.split()) <= 3:
			bar = evaluate_small_features(message)
        else:
    		bar = evaluate_features(message)

        result = db.chats.insert_one(
        {
            "message":message,
            "polarity":bar,
            "senderPhoneNumber":senderPhoneNumber,
            "senderName":senderName,
            "receiverPhoneNumber":receiverPhoneNumber
        }
        )

        print "bar",bar
        if(bar[0] == 'neg'):
            threshold_value = threshold_value + 1
            result = db.threshold.update_one(
            {"phoneNumber": senderPhoneNumber},
            {
                "$set": {
                    "threshold_value": threshold_value
                },
            }
            )
        print "Threshold: ",threshold_value
        if(threshold_value <= threshold_limit and not blocked):
                gcm = GCM("AIzaSyDL4b5qf3_iUGuqi__BGiQ2HKud5iA14rg")
                data = {'message': message,'polarity':bar}
                reg_id = deviceId
                gcm.plaintext_request(registration_id=reg_id, data=data)
                print "forward"
                return HttpResponse("Successfully sent")
        else:
                result = db.threshold.update_one(
                {"phoneNumber": senderPhoneNumber},
                {
                    "$set": {
                        "blocked": True
                    },
                }
                )
                cursor = db.threshold.find_one({'phoneNumber':senderPhoneNumber })
                contactOnePhone = cursor['contactOnePhone']
                contactOneName = cursor['contactOneName']
                contactTwoPhone = cursor['contactTwoPhone']
                contactTwoName = cursor['contactOTwoName']
                send_emergency_message(senderName,contactOnePhone,contactOneName)
                send_emergency_message(senderName,contactTwoPhone,contactTwoName)

        return HttpResponse(bar)

@csrf_exempt
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


@csrf_exempt
def login(request):
    if request.method == 'POST':
        deviceId = request.POST.get("reg_id")
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        phoneNumber = request.POST.get("phoneNumber")
        emailId = request.POST.get("emailId")
        age = request.POST.get("age")
        contactOneName = request.POST.get("contactOneName")
        contactOnePhone = request.POST.get("contactOnePhone")
        contactTwoName = request.POST.get("contactTwoName")
        contactTwoPhone = request.POST.get("contactTwoPhone")

        print "deviceId: ",deviceId
	print "lastName: ",lastName
	print "phoneNumber: ",phoneNumber
	print "age: ",age
        result = db.threshold.insert_one(
        {
            "deviceId":deviceId,
            "threshold_value":0,
            "firstName":firstName,
            "lastName":lastName,
            "phoneNumber":phoneNumber,
            "emailId":emailId,
            "age":age,
            "contactOneName":contactOneName,
            "contactOnePhone":contactOnePhone,
            "contactTwoName":contactTwoName,
            "contactTwoPhone":contactTwoPhone,
            "blocked":False
        }
        )

	data = {}
	data['response'] = "Successfully Registered"
	json_data = json.dumps(data)
	print "json data: ",json_data
        return JsonResponse(data,safe=False)
    else:
	data = {}
        data['response'] = 'Registeration Failed'
        json_data = json.dumps(data)
        return JsonResponse(json_data,safe=False)
