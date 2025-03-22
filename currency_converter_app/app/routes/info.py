from flask import Blueprint, render_template
from currency_converter_app.app.services.rate_service import get_latest_rates

bp = Blueprint('info', __name__, url_prefix='/info')

@bp.route('/currency101')
def currency101():
    rates = get_latest_rates()
    return render_template('currency101.html', rates=rates) 