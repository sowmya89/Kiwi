from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^send_message$', views.send_message, name='send_message'),
    url(r'^message$', views.process_message, name='process_message'),
]
