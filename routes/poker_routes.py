from flask import Blueprint, render_template, session, jsonify, request
from game_logic.poker import deal_poker_hand, poker_winner, reset_poker

# Blueprint for poker-related routes
poker_blueprint = Blueprint('poker_blueprint', __name__)

# Poker Game
@poker_blueprint.route('/play')
def poker_game():
    if 'bitcoin_balance' not in session:
        session['bitcoin_balance'] = 0.01  # Initialize balance if not already present

    balance = f'{session["bitcoin_balance"]:.8f}'

    # Deal both player and dealer hands
    player_hand = deal_poker_hand()
    dealer_hand = deal_poker_hand()

    # Get the winner by comparing both hands
    result = poker_winner(player_hand, dealer_hand)

    return render_template('poker.html', balance=balance, player_hand=player_hand, dealer_hand=dealer_hand, result=result)

# Reset poker game
@poker_blueprint.route('/reset_poker')
def reset_poker_game():
    reset_poker()
    return jsonify(message="Poker game reset")
