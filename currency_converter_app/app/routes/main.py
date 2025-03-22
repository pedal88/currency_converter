from flask import Blueprint, render_template, request, jsonify
from currency_converter_app.app.services.converter import convert_currency
from currency_converter_app.app.services.rate_service import get_latest_rates, get_top_rates

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    rates = get_latest_rates()
    top_rates = get_top_rates()
    return render_template('index.html', rates=rates, top_rates=top_rates)

@bp.route('/exchange-rates-explained')
def exchange_rates_explained():
    return render_template('exchange-rates-for-dummies.html')

@bp.route('/convert-currency', methods=['GET', 'POST'])
def convert_page():
    # Get all available currencies from the rates
    rates = get_latest_rates()
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