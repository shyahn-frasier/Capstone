from random import shuffle

player_money = 100
player_bet = player_money
ranks = range(1,13)
deck = ranks * 4
suits = ['SPADES', 'DIAMONDS', 'HEARTS', 'CLUBS']
player_points = 0
dealer_points = 0

def get_deck():
    return [[rank, suit] for rank in ranks for suit in suits]

deck = get_deck()
shuffle(deck)

print("How much would you like to bet?")
bet = input("> ")
print(f"Player has bet {bet} dollars")

player_in = True
player_hand = [deck.pop(), deck.pop()]
dealer_hand = [deck.pop(), deck.pop()]
player_points += ranks
dealer_points += ranks

print(player_hand)

print("What would you like to do?")
action = input("> ")


def stand():
    pass

def hit():
    if action == "hit":
        deck.pop()
        player_points += ranks

def double():
    if action == "double":
        player_bet *= 2
        deck.pop()
        player_point += ranks

def split():
    pass

def surrender():
    player_money -= player_bet / 2
    player_in = False


def push():
    if player_points == dealer_points:
        restart()

def player_bust():
    if player_points >= 22:
        print("House wins!")
        player_money -= player_bet

def dealer_bust():
    if dealer_points >= 22:
        print("Player wins!")
        player_money += player_bet

#def player_blackjack():

def insurance_wager():
    if dealer_hand == 'BLACKJACK':
        player_insurance_bet *= 2
        player_money += player_insurance_bet
    else:
        player_money -= player_insurance_bet

def restart():
    player_hand.clear()
    player_points = 0
    dealer_hand.clear()
    dealer_points = 0

# Go through card-dealing process
# Create point system matching each card, keeping in mind that aces can be 1 or 11
# Make additional functions (split, stand, hit, double, surrender, push)
# Make dealer rules (hit when at 17 points or below)
# Make bust and blackjack function, using those for win conditions
# Detail insurance_wager()