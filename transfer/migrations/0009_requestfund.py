# Generated by Django 4.2 on 2023-04-22 14:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("transfer", "0008_sendfund_quote_amount_sendfund_receiver_currency_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="RequestFund",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("requester", models.CharField(max_length=20)),
                ("funder", models.CharField(max_length=20)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("currency", models.CharField(default="GBP", max_length=3)),
                ("approved", models.BooleanField(default=False)),
                (
                    "date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
            ],
        ),
    ]