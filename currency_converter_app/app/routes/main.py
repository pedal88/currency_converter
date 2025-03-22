from flask import Blueprint, render_template, request, jsonify
from currency_converter_app.app.services.converter import convert_currency, get_top_rates
from currency_converter_app.app.services.rate_service import get_latest_rates

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    rates = get_latest_rates()
    top_rates = get_top_rates()
    return render_template('index.html', rates=rates, top_rates=top_rates)

@bp.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    amount = float(data.get('amount', 0))
    from_currency = data.get('from_currency')
    to_currency = data.get('to_currency')
    
    result = convert_currency(amount, from_currency, to_currency)
    if result is None:
        return jsonify({'error': 'Invalid conversion'}), 400
    
    return jsonify({
        'result': round(result, 2),
        'from': from_currency,
        'to': to_currency,
        'amount': amount
    }) 