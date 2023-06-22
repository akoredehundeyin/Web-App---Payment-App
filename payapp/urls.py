from django.urls import path
from . import views

urlpatterns = [
    path("webapps2023/", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("help/", views.help_page, name="help"),
]