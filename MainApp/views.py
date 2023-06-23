from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseBadRequest,JsonResponse,HttpRequest
from africastalking import SMS
import json
from django.conf import settings
from MainApp.models import SMSMessage,User
from django.views.decorators.csrf import csrf_exempt
import africastalking
from django.views import View
from paystackapi.transaction import Transaction as PaystackTransaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from MainApp.forms import *
import requests
import logging
from django.contrib import messages

# Create your views here.

AUN = settings.AFRICAS_TALKING_USERNAME
AAPI = settings.AFRICAS_TALKING_API_KEY


    

# Initialize SDK
# username = "Darkbeast"    # use 'sandbox' for development in the test environment
# api_key = "7fdf120e58abadb850c055b76388b58ed5433f30b13c262019707cbee64b2b8b"      # use your sandbox app API key for development in the test environment
africastalking.initialize(AUN, AAPI)

# Initialize a service  SMS
sms = africastalking.SMS

# SMS FUNCTION 
@csrf_exempt
def send_sms(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')
        recipients = [phone_number]
        # sender  = "SQUAD"

        try:
            # Send the SMS
            response = sms.send(message, recipients, )
            
            
            # Save the sent message to the database
            sent_message = SMSMessage(phone_number=phone_number, message=message)
            sent_message.save()

            # Process the response or handle any errors here
            print(response)

            return HttpResponse('SMS sent successfully')
        except Exception as e:
            return HttpResponse(f'Ouch! Something went wrong: {e}')
    else:
        return render(request, 'send_sms.html')



# SMS WEBHOOK

def webhook(request):
    try:
        data = json.loads(request.body)
        
        if data['event'] == 'sms.sent':
            print('SMS sent')
        elif data['event'] == 'sms.received':
            print('SMS received')
        else:
            print('Unknown event')

        return HttpResponse('Webhook received')
    except json.JSONDecodeError as e:
        return HttpResponse(f'Error decoding JSON data: {e}', status=400)
    except KeyError as e:
        return HttpResponse(f'Missing required key in JSON data: {e}', status=400)
    except Exception as e:
        return HttpResponse(f'Error processing webhook: {e}', status=500)
    
    
    


#USSD FUNCTON 
ussd = africastalking.USSD

@csrf_exempt
def ussd_callback(request):
    session_id   = request.POST.get("sessionId", None)
    serviceCode  = request.POST.get("serviceCode", None)
    phone_number = request.POST.get("phoneNumber", None)
    text         = request.POST.get("text", "default")

    if text == '':
        # This is the first request. Note how we start the response with CON
        response  = "CON What would you want to check \n"
        response += "1. My Account \n"
        response += "2. My phone number"

    elif text == '1':
        # Business logic for first level response
        response  = "CON Choose account information you want to view \n"
        response += "1. Account number\n"
        response += "2. Check Account Balance\n"
        response += "3. Account Statement\n"  # Additional option
        response += "4. Account Settings" 

    elif text == '2':
        # This is a terminal request. Note how we start the response with END
        response = "END Your phone number is " + phone_number

    elif text == '1*1':
        # This is a second level response where the user selected 1 in the first instance
        accountNumber = "ACC1001"
        # This is a terminal request. Note how we start the response with END
        response = "END Your account number is " + accountNumber
        
    elif text  == "1*2":
        response  = "CON Please choose the type of Account Balance you want to check  \n"
        response += "1. Checkings Account\n"
        response += "2. Savings Account\n"
    

        
    elif text  == "1*2*1":
        response  = "CON Please enter your PIN to check your account \n"
        
    elif text.startswith('1*2*1'):
        pin = "1234"  # Replace with your actual PIN
        if text == '1*2*1*{}'.format(pin):
            
            balance = "Ghc 20,323"
            response = "END Please you Checking account balance is " + balance
            
    elif text == '1*2*2':
        response  = "CON Please enter your PIN to check your account \n"

    elif text.startswith('1*2*2'):
        pin = "1234"  # Replace with your actual PIN
        if text == '1*2*2*{}'.format(pin):
            
            balance = "Ghc 1,234"
            response = "END Please you Savings account balance is " + balance
            
    elif text == '1*3':
        # Business logic for account statement
        statement = "Account Statement:\n"
        transactions = [
            {
                "date": "2023-06-20",
                "description": "Grocery Shopping",
                "amount": "$50.00",
            },
            {
                "date": "2023-06-19",
                "description": "ATM Withdrawal",
                "amount": "$100.00",
            },
            {
                "date": "2023-06-18",
                "description": "Online Purchase",
                "amount": "$25.00",
            },
        ]
        for transaction in transactions:
            statement += "Date: {}\n".format(transaction["date"])
            statement += "Description: {}\n".format(transaction["description"])
            statement += "Amount: {}\n\n".format(transaction["amount"])
        response = "END " + statement
        
    elif text == '1*4':
        # Business logic for account settings
        response = "CON Choose an option from Account Settings:\n"
        response += "1. Change PIN"

    elif text == '1*4*1':
        # Business logic for changing PIN
        response = "CON Enter your new PIN:"

    elif text.startswith('1*4*1*'):
        # Business logic for validating and updating PIN
        new_pin = text.split('*')[-1]
        if len(new_pin) == 4:
            # Update PIN logic here (e.g., save new_pin to the user's account)
            response = "END PIN updated successfully!"
        else:
            response = "END Invalid PIN. Please try again."

          
    else :
        response = "END Invalid choice"

    # Send the response back to the API

    return HttpResponse(response)







# initialize payment
@csrf_exempt


def pay_bill(request):
    if request.method == 'POST':
        form = BillPaymentForm(request.POST)
        if form.is_valid():
            bill_payment = form.save(commit=False)
            bill_payment.user = request.user
            bill_payment.status = 'PENDING'
            bill_payment.save()

            # Create Paystack transaction
            
            email = request.POST.get('email')
            if not email:
                # Handle the case when the user does not have an email
                error_message = 'User email is required.'
                return render(request, 'payment_failed.html', {'error_message': error_message})

            amount_in_kobo = int(bill_payment.bill_amount * 100)
            currency = 'GHS'

            url = 'https://api.paystack.co/transaction/initialize'
            headers = {
                'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
                'Content-Type': 'application/json',
            }
            data = {
                'amount': amount_in_kobo,
                'email': email,
                'currency': currency,
                # Add other necessary parameters
            }
            response = requests.post(url, headers=headers, json=data)
            paystack_transaction = response.json()

            if paystack_transaction['status']:
                authorization_url = paystack_transaction['data']['authorization_url']
                return redirect(authorization_url)
            else:
                error_message = paystack_transaction['message']
                return render(request, 'payment_failed.html', {'error_message': error_message})
    else:
        form = BillPaymentForm()
    
    return render(request, 'pay_bill.html', {'form': form})


logger = logging.getLogger(__name__)

@csrf_exempt
def payment_callback(request):
    ref = request.GET.get('reference')

    if ref:
        try:
            bill_payment = BillPayment.objects.get(ref=ref)
        except BillPayment.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'Bill payment not found.'})
    else:
        return JsonResponse({'success': False, 'error_message': 'Transaction reference not found.'})

    # Verify the transaction status with Paystack using the retrieved reference
    verification = PaystackTransaction.verify(ref)

    if verification['status']:
        bill_payment.status = 'SUCCESS'
        bill_payment.save()
        logger.info("Payment succeeded. Bill payment ID: %s", bill_payment.id)
        return JsonResponse({'success': True})
    else:
        error_message = verification['message']
        logger.error("Payment failed. Error message: %s", error_message)
        return JsonResponse({'success': False, 'error_message': error_message})

def payment_success(request):
    return render(request, 'payment_success.html')

def payment_failed(request):
    return render(request, 'payment_failed.html')




def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User(username=username, password=password, email=email)
        user.save()
        return redirect('login')
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username, password=password)
            # Perform login logic here
            return redirect('pay_bill')
        except User.DoesNotExist:
            error_message = 'Invalid username or password.'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')