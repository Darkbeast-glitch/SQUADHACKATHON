from django.urls import path

from MainApp.views import *
# from MainApp.views import PayboxTransactionCreateView 


urlpatterns = [
    path('send-sms/', send_sms, name='send-sms'),
    path('webhook/', webhook, name='webhook'),
    path('ussd/', ussd_callback, name='ussd-callback'),
    path('pay_bill/', pay_bill, name='pay_bill'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),

    path('payment_callback/', payment_callback, name='payment_callback'),
    path('payment_success/', payment_success, name='payment_success'),
    path('payment_failed/', payment_failed, name='payment_failed'),
    # path('paybox/transaction/create/', PayboxTransactionCreateView.as_view(), name='paybox-transaction-create'),


]
