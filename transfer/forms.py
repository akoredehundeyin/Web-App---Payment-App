from django import forms
from django.contrib.auth.models import User
from .models import Balance, SendFund, RequestFund
from django.contrib import messages


class SendFundForm(forms.ModelForm):
    class Meta:
        model = SendFund
        fields = ("sender", "receiver", "sender_currency", "receiver_currency", "amount", "quote_amount")
        widgets = {
            "receiver": forms.TextInput(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["sender"].initial = self.user.username
        self.fields["sender_currency"].initial = Balance.objects.get(user=self.user).currency
        self.fields["sender"].widget = forms.HiddenInput()
        self.fields["sender_currency"].widget = forms.HiddenInput()
        self.fields["receiver_currency"].widget = forms.HiddenInput()
        self.fields["quote_amount"].widget = forms.HiddenInput()
        self.form_error = None

    def clean(self):
        cleaned_data = super().clean()
        receiver = cleaned_data.get("receiver")
        receiver_currency = Balance.objects.get(user__username=receiver).currency
        amount = cleaned_data.get("amount")
        if receiver == self.user.username:
            self.form_error = "Sender and Receiver cannot be the same"
            raise forms.ValidationError(self.form_error)
        if amount <= 0:
            self.form_error = "Amount must be greater than 0.00"
            raise forms.ValidationError(self.form_error)
        cleaned_data["sender_currency"] = Balance.objects.get(user=self.user).currency
        if cleaned_data["sender_currency"] == receiver_currency:
            quote_amount = amount
        else:
            quote_amount = Balance.convert_currency(amount, cleaned_data["sender_currency"], receiver_currency)
        cleaned_data["quote_amount"] = quote_amount
        cleaned_data["receiver_currency"] = receiver_currency
        return cleaned_data


class RequestFundForm(forms.ModelForm):
    class Meta:
        model = RequestFund
        fields = ("requester", "funder", "amount", "currency", "status")
        widgets = {
            "funder": forms.TextInput(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["requester"].initial = self.user.username
        self.fields["requester"].widget = forms.HiddenInput()
        self.fields["currency"].initial = Balance.objects.get(user=self.user).currency
        self.fields["currency"].widget = forms.HiddenInput()
        self.fields["status"].widget = forms.HiddenInput()
        self.form_error = None

    def clean(self):
        cleaned_data = super().clean()
        funder = cleaned_data.get("funder")
        amount = cleaned_data.get("amount")
        if funder == self.user.username:
            self.form_error = "Requester and Funder cannot be the same"
            raise forms.ValidationError(self.form_error)
        if amount <= 0:
            self.form_error = "Amount must be greater than 0.00"
            raise forms.ValidationError(self.form_error)
        return cleaned_data
