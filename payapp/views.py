from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from transfer.models import RequestFund


def index(request):
    if request.method == "GET":
        return render(request, "payapp/index.html")

@login_required
def dashboard(request):
    return render(request, "payapp/dashboard.html")

@login_required
def help_page(request):
    return render(request, "payapp/help.html")