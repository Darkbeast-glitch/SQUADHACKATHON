from django.shortcuts import render
from django.http import HttpResponse
from africastalking import SMS
import json
from django.conf import settings
from .sms import SMS

from MainApp.models import SMSMessage
from django.views.decorators.csrf import csrf_exempt
import africastalking


# Create your views here.

# AUN = settings.AFRICAS_TALKING_USERNAME
# AAPI = settings.AFRICAS_TALKING_API_KEY

# def send_sms(request):
#     if request.method == 'POST':
#         phone_number = request.POST.get('phone_number')
#         message = request.POST.get('message')
#         sender_id = 'Darkbeast'  # Replace with your desired sender ID


#         try:
#             sms = SMS()
#             response = sms.send(message, [phone_number], sender_id)

#             # Process the response or handle any errors here
#             print(response)

#             return HttpResponse('SMS sent successfully')
#         except Exception as e:
#             return HttpResponse(f'Ouch! Something went wrong: {e}')
#     else:
#         return render(request, 'send_sms.html')
    
    
    
    

# Initialize SDK
username = "Darkbeast"    # use 'sandbox' for development in the test environment
api_key = "7fdf120e58abadb850c055b76388b58ed5433f30b13c262019707cbee64b2b8b"      # use your sandbox app API key for development in the test environment
africastalking.initialize(username, api_key)

# Initialize a service e.g. SMS
sms = africastalking.SMS
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

            # Process the response or handle any errors here
            print(response)

            return HttpResponse('SMS sent successfully')
        except Exception as e:
            return HttpResponse(f'Ouch! Something went wrong: {e}')
    else:
        return render(request, 'send_sms.html')



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
    
    
    
    