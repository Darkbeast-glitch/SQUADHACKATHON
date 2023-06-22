from django.shortcuts import render
from django.http import HttpResponse
from africastalking import SMS
import json
from django.conf import settings
from MainApp.models import SMSMessage
from django.views.decorators.csrf import csrf_exempt
import africastalking


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