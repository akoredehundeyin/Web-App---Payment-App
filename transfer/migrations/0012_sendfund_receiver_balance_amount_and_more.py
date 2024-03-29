# Generated by Django 4.2 on 2023-04-24 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transfer", "0011_remove_requestfund_approved_requestfund_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="sendfund",
            name="receiver_balance_amount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name="sendfund",
            name="sender_balance_amount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
