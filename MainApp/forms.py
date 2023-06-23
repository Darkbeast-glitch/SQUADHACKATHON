from django import forms
from .models import BillPayment




class BillPaymentForm(forms.ModelForm):
    class Meta:
        model = BillPayment
        fields = ['biller_name', 'bill_amount', 'email']

