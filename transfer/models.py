from django.db import models
from django.contrib.auth.models import User
import requests
from decimal import Decimal
from django.utils.timezone import now
from notification.models import Notification


class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="balance")
    currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.amount}{self.currency}"

    @staticmethod
    def convert_currency(amount, base_currency, quote_currency):
        url = f"http://127.0.0.1:8000/conversion/?base_currency={base_currency}&quote_currency={quote_currency}&amount={amount}"
        response = requests.get(url)
        if response.status_code == 200:
            raw_data = response.json()
            quote_amount = Decimal(raw_data["quote_amount"])
            return quote_amount
        else:
            raise ValueError(f"Conversion failed: {response.content}")


class SendFund(models.Model):
    sender = models.CharField(max_length=20)
    receiver = models.CharField(max_length=20)
    sender_currency = models.CharField(max_length=3, default="GBP")
    receiver_currency = models.CharField(max_length=3, default="GBP")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    quote_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sender_balance_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    receiver_balance_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        details = ""
        details += f"Sender: {self.sender}\n"
        details += f"Receiver: {self.receiver}\n"
        details += f"Amount: {self.amount}{self.sender_currency}|{self.quote_amount}{self.receiver_currency}\n"
        details += f"Date: {self.date}"
        return details


class RequestFund(models.Model):
    requester = models.CharField(max_length=20)
    funder = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="GBP")
    status = models.TextField(default="PENDING")
    date = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        details = ""
        details += f"Requester: {self.requester}\n"
        details += f"Funder: {self.funder}\n"
        details += f"Amount: {self.amount}{self.currency}\n"
        details += f"Status: {self.status}\n"
        details += f"Date: {self.date}"
        return details


