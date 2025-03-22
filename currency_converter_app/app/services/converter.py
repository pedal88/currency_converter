from currency_converter_app.app.services.rate_service import get_latest_rates

def convert_currency(amount, from_currency, to_currency):
    """
    Convert amount from one currency to another using latest rates.
    """
    rates = get_latest_rates()
    if not rates:
        return None
    
    # Convert to USD first (as base currency)
    usd_amount = amount / rates.get(from_currency, 1)
    # Convert from USD to target currency
    return usd_amount * rates.get(to_currency, 1)

def get_top_rates(limit=5):
    """
    Get top N exchange rates relative to USD.
    """
    rates = get_latest_rates()
    if not rates:
        return []
    
    # Sort rates by value (excluding USD)
    sorted_rates = sorted(
        [(currency, rate) for currency, rate in rates.items() if currency != 'USD'],
        key=lambda x: x[1],
        reverse=True
    )
    
    return sorted_rates[:limit] 