import random
from flask import session

class DeckController:
    colors = ['PI', 'KA', 'TR', 'KO']
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    @staticmethod
    def shuffle_deck():
        deck = []
        for color in DeckController.colors:
            for card in DeckController.cards:
                deck.append(f'{color}-{card}')
        random.shuffle(deck)
        return deck

    @staticmethod
    def draw(deck):
        return deck.pop()

class GameController:
    @staticmethod
    def calculate_result(cards):
        total = 0
        aces = 0

        for card in cards:
            value = card.split('-')[1]

            if value.isdigit():
                total += int(value)
            elif value in ['J', 'Q', 'K']:
                total += 10
            elif value == 'A':
                total += 11
                aces += 1

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    @staticmethod
    def draw_card(deck):
        card = DeckController.draw(deck)
        return card

def initialize_blackjack():
    if 'deck' not in session:
        session['deck'] = DeckController.shuffle_deck()
    if 'player' not in session:
        session['player'] = []
    if 'dealer' not in session:
        session['dealer'] = []

def start_blackjack_game():
    initialize_blackjack()
    session['player'] = [DeckController.draw(session['deck']), DeckController.draw(session['deck'])]
    session['dealer'] = [DeckController.draw(session['deck'])]
    session.modified = True

def draw_for_player():
    card = GameController.draw_card(session['deck'])
    session['player'].append(card)
    session.modified = True
    return card

def draw_for_dealer():
    while GameController.calculate_result(session['dealer']) < 18:
        card = GameController.draw_card(session['deck'])
        session['dealer'].append(card)
    session.modified = True

def get_winner():
    player_total = GameController.calculate_result(session['player'])
    dealer_total = GameController.calculate_result(session['dealer'])

    if player_total > 21:
        return 'Dealer'
    elif dealer_total > 21 or player_total > dealer_total:
        return 'Player'
    elif player_total == dealer_total:
        return 'None'
    else:
        return 'Dealer'

def reset_blackjack():
    session.pop('deck', None)
    session.pop('player', None)
    session.pop('dealer', None)
