from django.urls import path
from . import views

urlpatterns = [
    path("wallet/", views.wallet, name="wallet"),
    path("transfer/", views.transfer_fund, name="transfer"),
    path("send/", views.send_fund, name="send"),
    path("request/", views.request_fund, name="request"),
    path("request_home/", views.request_fund_home, name="request_home"),
    path("fund_requests_list/", views.fund_requests_list, name="fund_requests_list"),
    path("pending_fund_requests_list/", views.pending_fund_requests_list, name="pending_fund_requests_list"),
    path("approve_fund_request/<int:request_id>/", views.approve_fund_request, name="approve_fund_request"),
    path("decline_fund_request/<int:request_id>/", views.decline_fund_request, name="decline_fund_request"),
]