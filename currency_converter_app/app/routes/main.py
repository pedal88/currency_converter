from flask import Blueprint, render_template, request, jsonify
from currency_converter_app.app.services.converter import convert_currency
from currency_converter_app.app.services.rate_service import get_latest_rates, get_top_rates
import json

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    rates, metadata = get_latest_rates()
    top_rates = get_top_rates()
    return render_template('index.html', 
                         rates=rates, 
                         top_rates=top_rates,
                         metadata=metadata)

@bp.route('/exchange-rates-explained')
def exchange_rates_explained():
    return render_template('exchange-rates-for-dummies.html')

@bp.route('/convert-currency', methods=['GET', 'POST'])
def convert_page():
    # Get all available currencies from the rates
    rates, metadata = get_latest_rates()
    available_currencies = ['USD'] + list(rates.keys())  # Add USD as it's our base currency
    available_currencies.sort()  # Sort alphabetically

    # Initialize variables for the template
    result = None
    error = None
    amount = None
    from_currency = None
    to_currency = None

    if request.method == 'POST':
        try:
            # Get form data
            amount = float(request.form.get('amount', 0))
            from_currency = request.form.get('from_currency')
            to_currency = request.form.get('to_currency')

            # Validate inputs
            if not all([amount, from_currency, to_currency]):
                error = 'Please fill in all fields'
            else:
                # Perform conversion
                result = convert_currency(amount, from_currency, to_currency)
                if result is None:
                    error = 'Invalid conversion'
                else:
                    result = round(result, 2)

        except ValueError:
            error = 'Invalid amount'
        except Exception as e:
            error = str(e)

    # Render template with all necessary data
    return render_template('convert-exchange-rate.html',
                         available_currencies=available_currencies,
                         result=result,
                         error=error,
                         amount=amount,
                         from_currency=from_currency,
                         to_currency=to_currency)

@bp.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        amount = float(data.get('amount', 0))
        from_currency = data.get('from_currency')
        to_currency = data.get('to_currency')
        
        if not all([amount, from_currency, to_currency]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        result = convert_currency(amount, from_currency, to_currency)
        if result is None:
            return jsonify({'error': 'Invalid conversion'}), 400
        
        return jsonify({
            'result': round(result, 2),
            'from': from_currency,
            'to': to_currency,
            'amount': amount
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred during conversion'}), 500

@bp.route('/ai-bot')
def ai_bot():
    return render_template('ai-bot.html')

@bp.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower()
        
        # Get current rates for context
        rates, metadata = get_latest_rates()
        
        # Basic response logic based on user input
        response = process_chat_message(user_message, rates, metadata)
        
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def process_chat_message(message, rates, metadata):
    """Process the chat message and return an appropriate response."""
    message = message.lower().strip()
    
    # Greeting responses
    greetings = ['hi', 'hello', 'hey', 'can you hear me']
    if any(greeting in message for greeting in greetings):
        return "Hello! Yes, I can hear you clearly. How can I help you with currency information today?"

    # Exchange rate queries
    if any(word in message for word in ['rate', 'exchange', 'worth', 'value']):
        # Check for specific currency pairs
        currencies = list(rates.keys()) + ['USD']
        mentioned_currencies = [curr for curr in currencies if curr.lower() in message.upper()]
        
        if len(mentioned_currencies) == 2:
            curr1, curr2 = mentioned_currencies
            if curr1 == 'USD':
                rate = rates.get(curr2, 0)
                return f"The current exchange rate is: 1 USD = {rate} {curr2}"
            elif curr2 == 'USD':
                rate = rates.get(curr1, 0)
                return f"The current exchange rate is: 1 {curr1} = {rate} USD"
        elif len(mentioned_currencies) == 1:
            curr = mentioned_currencies[0]
            if curr != 'USD':
                rate = rates.get(curr, 0)
                return f"The current exchange rate is: 1 {curr} = {rate} USD"
        else:
            # General exchange rate status
            eur_rate = rates.get('EUR', 0)
            trend = "strengthening" if eur_rate < 0.92 else "weakening"
            return f"Currently, 1 USD is worth {eur_rate} EUR. The US dollar is {trend} against the euro compared to the historical average of 0.92 EUR."

    # Market impact and future rate queries
    if any(word in message for word in ['impact', 'future', 'affect', 'trend', 'forecast']):
        return """Several factors will impact future exchange rates:

1. Economic Indicators:
   - Interest rates set by central banks (Fed and ECB)
   - Inflation rates in respective regions
   - GDP growth rates
   - Employment figures

2. Political Factors:
   - Government policies
   - International trade agreements
   - Political stability

3. Market Sentiment:
   - Global economic outlook
   - Investment flows
   - Risk appetite in financial markets

4. Trade Balances:
   - Import/export ratios
   - Current account deficits/surpluses

Would you like to know more about any of these factors?"""

    # Conversion guidance
    if any(word in message for word in ['convert', 'change', 'calculator']):
        return """I can help you convert currencies! Here are two ways:

1. Use our conversion tool: Click the 'Convert' link in the navigation menu
2. Ask me directly: Try saying something like 'Convert 100 USD to EUR'

What would you like to try?"""

    # Update time queries
    if any(word in message for word in ['updated', 'latest', 'recent']):
        return f"The exchange rates were last updated {metadata['last_updated']} from {metadata['source']}. We update our rates regularly to ensure accuracy."

    # Default response with suggestion
    return """I can help you with:
1. Current exchange rates (e.g., "What's the EUR/USD rate?")
2. Currency conversion (e.g., "Convert 100 USD to EUR")
3. Market analysis (e.g., "What affects exchange rates?")
4. Latest updates (e.g., "When were rates last updated?")

What would you like to know?"""

@bp.route('/historical-rates')
def historical_rates():
    # Get all available currencies from the current rates
    rates, _ = get_latest_rates()
    available_currencies = ['USD'] + list(rates.keys())
    available_currencies.sort()
    
    return render_template('historical-exchange-rates.html',
                         available_currencies=available_currencies)

def get_economic_events():
    """Return major economic events that impacted currency exchange rates."""
    return [
        {
            "date": "2010-01-01",
            "event": "European Debt Crisis Begins",
            "impact": "EUR weakens against major currencies as Greece reveals severe budget problems"
        },
        {
            "date": "2011-01-01",
            "event": "European Sovereign Debt Crisis Intensifies",
            "impact": "EUR/USD falls to 0.747 as debt crisis spreads to other EU nations"
        },
        {
            "date": "2012-01-01",
            "event": "ECB's 'Whatever it Takes' Speech",
            "impact": "EUR strengthens to 0.772 vs USD after ECB pledges to preserve the euro"
        },
        {
            "date": "2013-01-01",
            "event": "Abenomics Launch in Japan",
            "impact": "JPY weakens to 86.75 vs USD due to aggressive monetary easing"
        },
        {
            "date": "2014-01-01",
            "event": "End of Fed's QE Program",
            "impact": "USD strengthens broadly, EUR falls to 0.726"
        },
        {
            "date": "2016-01-01",
            "event": "Brexit Referendum",
            "impact": "GBP drops significantly to 0.679 vs USD"
        },
        {
            "date": "2017-01-01",
            "event": "Trump Administration Takes Office",
            "impact": "USD volatility increases, EUR rises to 0.949"
        },
        {
            "date": "2018-01-01",
            "event": "US-China Trade War Begins",
            "impact": "CNY weakens to 6.506 vs USD"
        },
        {
            "date": "2019-01-01",
            "event": "Global Growth Slowdown",
            "impact": "Safe-haven currencies (JPY, CHF) strengthen"
        },
        {
            "date": "2021-01-01",
            "event": "Post-COVID Recovery",
            "impact": "USD weakens as global economy rebounds"
        },
        {
            "date": "2022-01-01",
            "event": "Russia-Ukraine Conflict",
            "impact": "RUB volatility increases dramatically"
        }
    ]

@bp.route('/api/historical-rates', methods=['POST'])
def get_historical_rates():
    try:
        data = request.get_json()
        selected_currencies = data.get('currencies', [])
        
        if not selected_currencies or len(selected_currencies) > 5:
            return jsonify({'error': 'Please select between 1 and 5 currencies'}), 400
        
        # Get historical data from archive
        historical_data = {
            'dates': [],
            'currencies': [],
            'events': get_economic_events()  # Add economic events
        }
        
        # Define all dates we want to include in chronological order
        dates = [
            '2010-01-01',
            '2011-01-01',
            '2012-01-01',
            '2013-01-01',
            '2014-01-01',
            '2015-01-01',
            '2016-01-01',
            '2017-01-01',
            '2018-01-01',
            '2019-01-01',
            '2020-01-01',
            '2021-01-01',
            '2022-01-01',
            '2023-01-01',
            '2024-01-01',
            '2025-01-01',
            '2025-02-01',
            '2025-03-01',
            '2025-03-22'
        ]
        historical_data['dates'] = dates
        
        # For each selected currency, get its historical rates
        for currency in selected_currencies:
            rates = []
            missing_dates = []
            
            for date in dates:
                try:
                    file_path = f'currency_converter_app/data/archive/rates_{date}.json'
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        rate = data['rates'].get(currency)
                        if rate is None:
                            missing_dates.append(date)
                            rates.append(None)  # Use None for missing rates
                        else:
                            rates.append(rate)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    # Log the error for debugging
                    print(f"Error reading file for date {date}: {str(e)}")
                    missing_dates.append(date)
                    rates.append(None)  # Use None for missing rates
            
            if len(missing_dates) == len(dates):
                return jsonify({
                    'error': f'No historical data available for currency {currency}. Please try another currency.'
                }), 404
            
            historical_data['currencies'].append({
                'currency': currency,
                'rates': rates,
                'missing_dates': missing_dates
            })
        
        if not historical_data['currencies']:
            return jsonify({'error': 'No data available for the selected currencies'}), 404
        
        return jsonify(historical_data)
    except Exception as e:
        print(f"Unexpected error in get_historical_rates: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred while fetching historical rates'}), 500