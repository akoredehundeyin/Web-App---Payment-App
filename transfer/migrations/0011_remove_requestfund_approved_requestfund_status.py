# Generated by Django 4.2 on 2023-04-22 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transfer", "0010_alter_requestfund_approved"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="requestfund",
            name="approved",
        ),
        migrations.AddField(
            model_name="requestfund",
            name="status",
            field=models.TextField(default="PENDING"),
        ),
    ]