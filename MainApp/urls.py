from django.urls import path

from MainApp.views import *

urlpatterns = [
    path('send-sms/', send_sms, name='send-sms'),
    path('webhook/', webhook, name='webhook'),
    path('ussd/', ussd_callback, name='ussd-callback'),


]
