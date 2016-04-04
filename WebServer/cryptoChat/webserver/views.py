from django.shortcuts import render
from webserver.models import Post
from django.utils import timezone
from django.http import HttpResponse
from pymongo import MongoClient
# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'HTML/post_list.html', {'posts':posts})

def process_message(request):
    client = MongoClient('localhost', 27017)
    db = client['cmpe280_ajax']
    cursor = db.user_data.find()
    for document in cursor:
        print(document)
    return HttpResponse(document)
