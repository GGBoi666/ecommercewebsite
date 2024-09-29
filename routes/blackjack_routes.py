# blackjack_routes.py
from flask import Blueprint, render_template

blackjack_blueprint = Blueprint('blackjack_blueprint', __name__)

@blackjack_blueprint.route('/blackjack')
def blackjack_game():
    return render_template('blackjack.html')
