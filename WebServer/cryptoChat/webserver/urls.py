from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^blog$', views.post_list, name='post_list'),
    url(r'^message$', views.process_message, name='process_message'),
]
