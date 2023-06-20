import africastalking
from django.conf import settings

class SMS:
    def __init__(self):
        # Set your app credentials
        self.username = settings.AFRICAS_TALKING_USERNAME
        self.api_key = settings.AFRICAS_TALKING_API_KEY

        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)

        # Get the SMS service
        self.sms = africastalking.SMS

    def send(self, message, recipients, sender):
        try:
            # Thats it, hit send and we'll take care of the rest.
            response = self.sms.send(message, recipients, sender)
            return response
        except Exception as e:
            return str(e)

# Usage example
if __name__ == '__main__':
    # Set your message
    message = "I'm a lumberjack and it's ok, I sleep all night and I work all day"

    # Set the numbers you want to send to in international format
    recipients = ["+254713YYYZZZ", "+254733YYYZZZ"]

    # Set your shortCode or senderId
    sender = "shortCode or senderId"

    sms = SMS()
    response = sms.send(message, recipients, sender)
    print(response)
