def make_payment(request):
    if request.method == 'POST':
        currency = request.POST.get('currency')
        amount = request.POST.get('amount')
        # mode = "Test"
        mobile_network = request.POST.get('mobile_network')
        mobile_number = request.POST.get('mobile_number')
        bank_code = request.POST.get('bank_code')
        bank_account = request.POST.get('bank_account')
        # callback_url = request.POST.get('callback_url', '')

        payload = {
            'currency': currency,
            'amount': amount,
            # 'mode': "Test",
            'mobile_network': mobile_network,
            'mobile_number': mobile_number,
            'bank_code': bank_code,
            'bank_account': bank_account,
            # 'callback_url': callback_url,
        }

        # Create a PayboxTransaction instance and save it to the database
        transaction = PayboxTransaction(**payload)
        transaction.save()

        # Make the Paybox API request using the payload
        url = "https://paybox.com.co/transfer"
        response = requests.post(url, data=payload)

        if response.status_code == 200:
            # Handle the API response and return the appropriate response to the user
            # ...

            return render(request, 'paybox/payment_success.html')

    else:
        # Handle GET request and render the payment form
        context = {
            'currency_choices': PayboxTransaction.CURRENCY_CHOICES,
            'mobile_network_choices': PayboxTransaction.MOBILE_NETWORK_CHOICES,
            'bank_choices': PayboxTransaction.BANK_CHOICES,
            'transaction_type_choices': PayboxTransaction.TRANSACTION_TYPE_CHOICES,
            'callback_url': "https://paybox.com.co/transfer",
        }
        return render(request, 'paybox/payment_form.html', context)