from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("register/", views.user_registration, name="register"),
    path("logout/", views.user_logout, name="logout"),
    path("user_profile/", views.user_profile, name="user_profile"),
]