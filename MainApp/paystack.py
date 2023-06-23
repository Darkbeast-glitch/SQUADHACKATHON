from email import header
from urllib import request, response
from wsgiref import headers
from django.conf import settings


class PayStack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url = "https://api.paystack.co"

    def verify_payment(self, ref, *arg, **kwargs):
        path = f'/transaction/verify/{ref}',

        headers = {

            "Authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
            'Content-Type': 'application/json',
        }

        url = self.base_url + path
        response = request.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['data']

        response_data = response.json()
        return response_data["status"], response_data['message']