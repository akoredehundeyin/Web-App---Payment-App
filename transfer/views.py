from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .models import Balance, SendFund, RequestFund
from decimal import Decimal
from .forms import SendFundForm, RequestFundForm
from django.contrib import messages
from django.contrib.auth.models import User
from notification.models import Notification
from django.db.models import Q


def wallet(request):
    wallet_transfers = list(SendFund.objects.filter(Q(sender=request.user.username) | Q(receiver=request.user.username)).order_by("date"))
    return render(request, "transfer/wallet.html", {"wallet_transfers": wallet_transfers})


def transfer_fund(request):
    return render(request, "transfer/transfer_fund.html")


def request_fund_home(request):
    return render(request, "transfer/request_fund_home.html")


def send_fund(request):
    if request.method == "POST":
        form = SendFundForm(request.POST, user=request.user)
        if form.is_valid():
            sender = request.user
            receiver = User.objects.get(username=request.POST.get("receiver"))
            amount = Decimal(request.POST.get("amount"))

            sender_balance = Balance.objects.get(user=sender)
            receiver_balance = Balance.objects.get(user=receiver)

            sender_currency = sender_balance.currency
            receiver_currency = receiver_balance.currency

            if sender_balance.amount > amount:
                if sender_currency == receiver_currency:
                    with transaction.atomic():
                        sender_balance.amount -= amount
                        sender_balance.save()
                        receiver_balance.amount += amount
                        receiver_balance.save()
                        SendFund.objects.create(
                            sender=sender.username, receiver=receiver.username, sender_currency=sender_currency,
                            receiver_currency=receiver_currency, amount=amount, quote_amount=amount,
                            sender_balance_amount=sender_balance.amount, receiver_balance_amount=receiver_balance.amount
                        )
                else:
                    quote_amount = sender_balance.convert_currency(amount, sender_currency, receiver_currency)
                    with transaction.atomic():
                        sender_balance.amount -= amount
                        sender_balance.save()
                        receiver_balance.amount += quote_amount
                        receiver_balance.save()
                        SendFund.objects.create(
                            sender=sender.username, receiver=receiver.username, sender_currency=sender_currency,
                            receiver_currency=receiver_currency, amount=amount, quote_amount=quote_amount,
                            sender_balance_amount=sender_balance.amount, receiver_balance_amount=receiver_balance.amount
                        )

                messages.success(request, f"{amount}{sender_currency} successfully sent to {receiver}")
                notification = f"You received {amount if sender_currency==receiver_currency else quote_amount}{receiver_currency} from {sender.username}"
                Notification.send_notification(receiver, notification)
                return redirect("wallet")
            else:
                messages.info(request, "Insufficient Funds")
                form = SendFundForm(user=request.user)
                return render(request, "transfer/send_fund.html", {"send_fund": form})
        else:
            messages.warning(request, form.form_error)
            form = SendFundForm(user=request.user)
            return render(request, "transfer/send_fund.html", {"send_fund": form})
    form = SendFundForm(user=request.user)
    return render(request, "transfer/send_fund.html", {"send_fund": form})


def request_fund(request):
    if request.method == "POST":
        form = RequestFundForm(request.POST, user=request.user)
        if form.is_valid():
            funder = User.objects.get(username=request.POST.get("funder"))
            form.save()
            messages.success(request, f"Your fund request has been sent to {funder}")
            notification = f"You received a fund request of {form.cleaned_data.get('amount')}{form.cleaned_data.get('currency')} from {request.user.username}. Go to Send|Request to Approve or Decline"
            Notification.send_notification(recipient=funder, notification_text=notification)
            return redirect("fund_requests_list")
        else:
            messages.warning(request, form.form_error)
            form = RequestFundForm(user=request.user)
            return render(request, "transfer/request_fund.html", {"request_fund": form})
    form = RequestFundForm(user=request.user)
    return render(request, "transfer/request_fund.html", {"request_fund": form})


def fund_requests_list(request):
    fund_requests = list(RequestFund.objects.filter(Q(requester=request.user.username) | Q(funder=request.user.username)).order_by("date"))
    print(len(fund_requests))
    return render(request, "transfer/fund_requests_list.html", {"fund_requests": fund_requests})

def pending_fund_requests_list(request):
    pending_fund_requests = list(RequestFund.objects.filter(status="PENDING", funder=request.user.username).order_by("date"))
    return render(request, "transfer/pending_fund_requests_list.html", {"pending_fund_requests": pending_fund_requests})


def approve_fund_request(request, request_id):
    request_obj = get_object_or_404(RequestFund, id=request_id)
    requester = get_object_or_404(User, username=request_obj.requester)
    funder = get_object_or_404(User, username=request_obj.funder)
    if request.user != funder:
        messages.error(request, "You cannot approve this fund request")
        return redirect("fund_requests_list")

    sender = funder
    receiver = requester
    sender_balance = Balance.objects.get(user=sender)
    receiver_balance = Balance.objects.get(user=receiver)
    sender_currency = sender_balance.currency
    receiver_currency = receiver_balance.currency

    if sender_currency == receiver_currency:
        amount = request_obj.amount
        if sender_balance.amount >= amount:
            with transaction.atomic():
                request_obj.status = "APPROVED"
                request_obj.save()
                sender_balance.amount -= amount
                sender_balance.save()
                receiver_balance.amount += amount
                receiver_balance.save()
                SendFund.objects.create(
                    sender=sender.username, receiver=receiver.username, sender_currency=sender_currency,
                    receiver_currency=receiver_currency, amount=amount, quote_amount=amount,
                    sender_balance_amount=sender_balance.amount, receiver_balance_amount=receiver_balance.amount
                )
                messages.success(request, f"You have approved the fund request from {request_obj.requester}.")
                messages.success(request, f"{amount}{sender_currency} successfully sent to {receiver}")
                notification = f"{funder.username} has approved your fund request for {request_obj.amount}{request_obj.currency}."
                Notification.send_notification(requester, notification)
                notification = f"You received {amount}{receiver_currency} from {sender.username}"
                Notification.send_notification(receiver, notification)
            return redirect("pending_fund_requests_list")
        else:
            messages.error(request, "Insufficient Funds, Fund Request PENDING")
            return redirect("pending_fund_requests_list")
    else:
        quote_amount = Balance.convert_currency(amount=request_obj.amount, base_currency=receiver_currency, quote_currency=sender_currency)
        if sender_balance.amount > quote_amount:
            with transaction.atomic():
                request_obj.status = "APPROVED"
                request_obj.save()
                sender_balance.amount -= quote_amount
                sender_balance.save()
                receiver_balance.amount += request_obj.amount
                receiver_balance.save()
                SendFund.objects.create(
                    sender=sender.username, receiver=receiver.username, sender_currency=sender_currency,
                    receiver_currency=receiver_currency, amount=quote_amount, quote_amount=request_obj.amount,
                    sender_balance_amount=sender_balance.amount, receiver_balance_amount=receiver_balance.amount
                )
                messages.success(request, f"You have approved the fund request from {request_obj.requester}.")
                messages.success(request, f"{quote_amount}{sender_currency} successfully sent to {receiver}")
                notification = f"{funder.username} has approved your fund request for {request_obj.amount}{request_obj.currency}."
                Notification.send_notification(requester, notification)
                notification = f"You received {request_obj.amount}{receiver_currency} from {sender.username}"
                Notification.send_notification(receiver, notification)
            return redirect("pending_fund_requests_list")
        else:
            messages.error(request, "Insufficient Funds, Fund Request PENDING")
            return redirect("pending_fund_requests_list")


def decline_fund_request(request, request_id):
    request_obj = get_object_or_404(RequestFund, id=request_id)
    requester = get_object_or_404(User, username=request_obj.requester)
    funder = get_object_or_404(User, username=request_obj.funder)
    if request.user != funder:
        messages.error(request, "You cannot decline this fund request")
        return redirect("fund_requests_list")
    request_obj.status = "DECLINED"
    request_obj.save()
    messages.success(request, f"You have declined the fund request from {request_obj.requester}.")
    notification = f"{funder.username} has declined your fund request for {request_obj.amount}{request_obj.currency}."
    Notification.send_notification(requester, notification)
    return redirect("pending_fund_requests_list")


