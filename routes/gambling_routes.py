from flask import Blueprint, render_template, session, jsonify, request, url_for
import random
from game_logic.blackjack import initialize_blackjack, start_blackjack_game, draw_for_player, draw_for_dealer, get_winner as blackjack_winner, reset_blackjack
from game_logic.poker import deal_poker_hand, poker_winner, reset_poker

# Blueprint for gambling-related routes
gambling_blueprint = Blueprint('gambling_blueprint', __name__)

# Initialize user's Bitcoin balance if not already present
def initialize_balance():
    if 'bitcoin_balance' not in session:
        session['bitcoin_balance'] = 0.01  # Starting balance (for testing)
    if 'clicker_level' not in session:
        session['clicker_level'] = 1  # Start at clicker level 1

# Main Gambling Page (Home)
@gambling_blueprint.route('/gamble')
def gamble_home():
    initialize_balance()
    balance = f'{session["bitcoin_balance"]:.8f}'  # Display balance with 8 decimal places
    clicker_level = session['clicker_level']
    
    # Image URLs
    btc_icon_url = url_for('static', filename='img/btc_icon.avif')
    eth_icon_url = url_for('static', filename='img/eth_icon.jpg')
    doge_icon_url = url_for('static', filename='img/doge_icon.webp')
    background_url = url_for('static', filename='img/gambling_home_bg.avif')
    
    return render_template('gamble_home.html', balance=balance, clicker_level=clicker_level,
                           btc_icon=btc_icon_url, eth_icon=eth_icon_url,
                           doge_icon=doge_icon_url, background=background_url)

# Poker Game
@gambling_blueprint.route('/poker')
def poker():
    initialize_balance()
    balance = f'{session["bitcoin_balance"]:.8f}'  # Display balance with 8 decimal places

    # Deal both player and dealer hands
    player_hand, dealer_hand = deal_poker_hand(), deal_poker_hand()

    # Get the winner by comparing both hands
    result = poker_winner(player_hand, dealer_hand)
    
    return render_template('poker.html', balance=balance, player_hand=player_hand, dealer_hand=dealer_hand, result=result)

# Reset balance, games, etc.
@gambling_blueprint.route('/reset')
def reset():
    reset_blackjack()
    reset_poker()
    session.pop('bitcoin_balance', None)
    return jsonify(message="All balances and game data reset")

# Blackjack Game
@gambling_blueprint.route('/blackjack')
def blackjack():
    initialize_balance()
    balance = f'{session["bitcoin_balance"]:.8f}'  # Display balance with 8 decimal places
    start_blackjack_game()

    player_hand = session['player']
    dealer_hand = session['dealer']
    winner = blackjack_winner()

    return render_template('blackjack.html', balance=balance, player_hand=player_hand, dealer_hand=dealer_hand, result=winner)

# Clicker Game: Earn Bitcoin by clicking, with upgrades
@gambling_blueprint.route('/click_btc', methods=['POST'])
def click_btc():
    initialize_balance()
    clicker_level = session['clicker_level']
    earned_btc = 0.0001 * clicker_level  # Amount earned per click, multiplied by level
    session['bitcoin_balance'] += earned_btc
    return jsonify(new_balance=f'{session["bitcoin_balance"]:.8f}', clicker_level=clicker_level)

# Clicker Upgrade: Upgrade the clicker level to earn more BTC per click
@gambling_blueprint.route('/upgrade_clicker', methods=['POST'])
def upgrade_clicker():
    initialize_balance()
    upgrade_cost = 0.005  # Cost to upgrade clicker
    if session['bitcoin_balance'] >= upgrade_cost:
        session['bitcoin_balance'] -= upgrade_cost
        session['clicker_level'] += 1  # Increase the clicker level
        return jsonify(success=True, new_balance=f'{session["bitcoin_balance"]:.8f}', new_level=session['clicker_level'])
    else:
        return jsonify(success=False, message="Insufficient balance to upgrade!")

# Dice Game: Bet and roll the dice with adjustable bets
@gambling_blueprint.route('/roll_dice', methods=['POST'])
def roll_dice():
    initialize_balance()
    bet_amount = float(request.json.get('bet_amount', 0.001))  # Get the bet amount from the form
    if session['bitcoin_balance'] < bet_amount:
        return jsonify(success=False, message="Insufficient balance!")
    
    session['bitcoin_balance'] -= bet_amount  # Deduct the bet amount
    dice_result = random.randint(1, 6)
    
    if dice_result >= 4:  # Win if dice roll is 4 or higher
        winnings = bet_amount * 2
        session['bitcoin_balance'] += winnings
        return jsonify(success=True, result=dice_result, winnings=winnings, new_balance=f'{session["bitcoin_balance"]:.8f}')
    else:
        return jsonify(success=False, result=dice_result, new_balance=f'{session["bitcoin_balance"]:.8f}')

# Mini Slot Machine Game: Play slots with multiple paylines and jackpots
@gambling_blueprint.route('/play_slot', methods=['POST'])
def play_slot():
    initialize_balance()
    cost_per_spin = 0.001  # Cost of one spin in BTC
    if session['bitcoin_balance'] < cost_per_spin:
        return jsonify(success=False, message="Insufficient balance!")
    
    # Deduct the cost of playing
    session['bitcoin_balance'] -= cost_per_spin

    # Slot machine reels (3 reels with crypto coin symbols)
    reel_symbols = ['₿', 'Ξ', 'Ð']  # Using BTC, ETH, and DOGE as the symbols
    reel_1 = random.choice(reel_symbols)
    reel_2 = random.choice(reel_symbols)
    reel_3 = random.choice(reel_symbols)

    result = [reel_1, reel_2, reel_3]

    # Determine if the user wins (Jackpot if all match, double payout if two match)
    if reel_1 == reel_2 == reel_3:
        winnings = cost_per_spin * 10
        session['bitcoin_balance'] += winnings
        return jsonify(success=True, result=result, winnings=winnings, new_balance=f'{session["bitcoin_balance"]:.8f}')
    elif reel_1 == reel_2 or reel_2 == reel_3 or reel_1 == reel_3:
        winnings = cost_per_spin * 2
        session['bitcoin_balance'] += winnings
        return jsonify(success=True, result=result, winnings=winnings, new_balance=f'{session["bitcoin_balance"]:.8f}')
    else:
        return jsonify(success=False, result=result, new_balance=f'{session["bitcoin_balance"]:.8f}')

# Coin Flip Game
@gambling_blueprint.route('/coin_flip', methods=['POST'])
def coin_flip():
    initialize_balance()
    bet_amount = float(request.json.get('bet_amount', 0.001))  # Betting amount for the coin flip
    if session['bitcoin_balance'] < bet_amount:
        return jsonify(success=False, message="Insufficient balance!")

    session['bitcoin_balance'] -= bet_amount
    flip_result = random.choice(['heads', 'tails'])
    
    if flip_result == request.json.get('choice'):
        winnings = bet_amount * 2
        session['bitcoin_balance'] += winnings
        return jsonify(success=True, result=flip_result, winnings=winnings, new_balance=f'{session["bitcoin_balance"]:.8f}')
    else:
        return jsonify(success=False, result=flip_result, new_balance=f'{session["bitcoin_balance"]:.8f}')

# Roulette Game
@gambling_blueprint.route('/roulette', methods=['POST'])
def roulette():
    initialize_balance()
    bet_amount = float(request.json.get('bet_amount', 0.001))  # Betting amount for roulette
    if session['bitcoin_balance'] < bet_amount:
        return jsonify(success=False, message="Insufficient balance!")

    session['bitcoin_balance'] -= bet_amount
    outcome = random.choice(['red', 'black', 'green'])  # Simplified to red, black, and green
    player_choice = request.json.get('choice')

    if player_choice == outcome:
        if outcome == 'green':
            winnings = bet_amount * 14  # Green pays more
        else:
            winnings = bet_amount * 2  # Red/black payout
        session['bitcoin_balance'] += winnings
        return jsonify(success=True, result=outcome, winnings=winnings, new_balance=f'{session["bitcoin_balance"]:.8f}')
    else:
        return jsonify(success=False, result=outcome, new_balance=f'{session["bitcoin_balance"]:.8f}')
