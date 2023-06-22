from decimal import Decimal
from django.http import JsonResponse


RATES = {
    "GBP": {"EUR": Decimal("1.13"), "USD": Decimal("1.25")},
    "USD": {"EUR": Decimal("0.91"), "GBP": Decimal("0.80")},
    "EUR": {"GBP": Decimal("0.89"), "USD": Decimal("1.10")},
}


def conversion(request):
    base_currency = request.GET.get("base_currency")
    quote_currency = request.GET.get("quote_currency")
    amount = Decimal(request.GET.get("amount"))

    if base_currency == quote_currency:
        quote_amount = amount
    elif base_currency in RATES and quote_currency in RATES[base_currency]:
        rate = RATES[base_currency][quote_currency]
        quote_amount = amount * rate
    else:
        return JsonResponse({
            "error": f"Unsupported currency pair: {base_currency}/{quote_currency}"
        }, status=400)

    return JsonResponse({
        "base_currency": base_currency,
        "quote_currency": quote_currency,
        "amount": amount,
        "quote_amount": quote_amount,
    })
