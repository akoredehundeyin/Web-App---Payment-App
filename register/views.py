from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegistrationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import AuthenticationForm
from decimal import Decimal
from transfer.models import Balance
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone


@csrf_protect
def user_registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.date_joined = timezone.now()
            user.save()
            #creating user's initial balance
            currency = form.cleaned_data.get("currency")
            if currency == "GBP":
                initial_balance = Decimal("100.00")
            elif currency == "USD":
                initial_balance = Balance.convert_currency(Decimal("100.00"), "GBP", "USD")
            else:
                initial_balance = Balance.convert_currency(Decimal("100.00"), "GBP", "EUR")
            balance = Balance.objects.create(user=user, currency=currency, amount=initial_balance)
            balance.save()

            messages.success(request, "Registration Successful")
            return redirect("login")
        else:
            messages.error(request, "Registration Unsuccessful: Invalid Input")
            form = RegistrationForm()
            return render(request, "register/register.html", {"user_registration": form})
    form = RegistrationForm()
    return render(request, "register/register.html", {"user_registration": form})


@csrf_protect
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {username}.")
                if user.is_staff:
                    return redirect("admin:index")
                else:
                    return render(request, "payapp/dashboard.html")
            else:
                messages.error(request, "User not found, kindly register")
                form = AuthenticationForm()
                return render(request, "register/login.html", {"user_login": form})
        else:
            messages.error(request, "Invalid Username or Password")
            form = AuthenticationForm()
            return render(request, "register/login.html", {"user_login": form})
    form = AuthenticationForm()
    return render(request, "register/login.html", {"user_login": form})


@csrf_protect
@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "Logout Successful")
    return redirect("login")


@login_required
def user_profile(request):
    return render(request, "register/user_profile.html")



