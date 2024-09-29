import random

# Simple deck initialization for Poker
def initialize_deck():
    suits = ['♠', '♥', '♣', '♦']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [f'{rank}{suit}' for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck

# Deal poker hand
def deal_poker_hand():
    deck = initialize_deck()
    return [deck.pop() for _ in range(5)]

# Calculate hand winner (simplified logic based on sum of card values)
def poker_winner(player_hand, dealer_hand):
    player_total = sum(get_card_value(card) for card in player_hand)
    dealer_total = sum(get_card_value(card) for card in dealer_hand)

    if player_total > dealer_total:
        return 'Player Wins'
    elif dealer_total > player_total:
        return 'Dealer Wins'
    else:
        return "It's a Tie"

# Get card value based on rank
def get_card_value(card):
    rank = card[:-1]  # Exclude suit
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11  # This can be adjusted based on hand logic
    return int(rank)

# Reset poker game
def reset_poker():
    # Implement poker reset logic here if needed
    pass
