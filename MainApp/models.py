from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import secrets
from MainApp.paystack import PayStack

# Create your models here.



# SMS MODEL
class SMSMessage(models.Model):
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.phone_number}: {self.message}'


# ussd is just a request in the VIEW.PY


class BillPayment(models.Model):
    # Existing fields
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    biller_name = models.CharField(max_length=100)
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('SUCCESS', 'Success'), ('PENDING', 'Pending'), ('FAILED', 'Failed')])
    ref = models.CharField(max_length=100)  # New field for the transaction reference

    def __str__(self):
        return f'{self.biller_name} - {self.bill_amount}'
    
    
    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(6)
            object_with_similar_ref = BillPayment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
            super().save(*args, **kwargs)
            
            
    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['get_total']/100 == self.get:
                self.verified = True
            self.save()
            if self.verified:
                return True
            return False

    
    
    
class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.username