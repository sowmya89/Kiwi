from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^send$', views.send_message, name='send_message'),
    url(r'^message$', views.process_message, name='process_message'),
    url(r'^register_device$', views.register_device, name='register_device'),
    url(r'^login$', views.login, name='login'),
    url(r'^test_message$', views.test_message, name='test_message'),
    url(r'^getuser$', views.getuser, name='getuser'),
    url(r'^process_registeration$', views.process_registeration, name='process_registeration'),
]

