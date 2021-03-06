import random

player_money = 1000
chips = 0
max_players = 4
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'JACK', 'QUEEN', 'KING', 'ACE']
suits = ['SPADES', 'DIAMONDS', 'HEARTS', 'CLUBS']


class Card(object):
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

        if rank == 'ACE':
            self.point = 11
        elif rank in ['JACK', 'QUEEN', 'KING']:
            self.point = 10
        else:
            self.point = int(rank)

        self.hidden = False

    def __str__(self):
        if self.hidden:
            return '[?]'
        else:
            return '[' + self.rank + ' of ' + self.suit + ']'

    def hide_card(self):
        self.hidden = True

    def reveal_card(self):
        self.hidden = False

    def is_ace(self):
        return self.rank == 'ACE'

class Deck(object):
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        self.shuffle()

    def __str__(self):
        cards_in_deck = ''
        for card in self.cards:
            cards_in_deck = cards_in_deck + str(card) + ' '
        return cards_in_deck

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        card = self.cards.pop(0)
        return card

class Hand(object):
    def __init__(self):
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)
        return self.hand

    def get_value(self):
        aces = 0
        value = 0
        for card in self.hand:
            if card.is_ace():
                aces += 1
            value += card.point
        while (value > 21) and aces:
            value -= 10
            aces -= 1
        return value

class Dealer(Hand):
    def __init__(self, name, deck):
        Hand.__init__(self)
        self.name = name
        self.deck = deck
        self.isBust = False

    def show_hand(self):
        for card in self.hand:
            print(card)
        print

    def hit(self):
        print("Hitting...")
        self.add_card(self.deck.deal_card())
        return self.hand

    def stand(self):
        print("%s gets %d. Done." % (self.name, self.get_value()))

    def check_bust(self):
        if self.get_value() > 21:
            self.isBust = True
            print("%s goes bust!" % self.name)
        else:
            self.stand()


class Player(Dealer):
    def __init__(self, name, deck, bet):
        Dealer.__init__(self, name, deck)
        self.bet = bet
        self.isBust = False
        self.isSurrender = False
        self.isSplit = False
        self.split = []

def play(player, deck):
    print(player.name + ':',)
    player.show_hand()
    if player.name == 'Dealer':
        while player.get_value() < 17:
            player.hit()
            player.show_hand()
        player.check_bust()
    else:
        global chips
        if chips > player.bet and not player.isSplit:
            if player.hand[0].point == player.hand[1].point:
                choice = input_func("Hit, Stand, Double, Split, or Surrender? ", str.lower,
                                    range_ =('hit', 'stand', 'double', 'split', 'surrender'))
            else:
                choice = input_func("Hit, Stand, Double, or Surrender? ", str.lower,
                                    range_ =('hit', 'stand', 'double', 'surrender'))
        else:
            choice = input_func("Hit, Stand or Surrender? ", str.lower, range_ =('hit', 'stand', 'surrender'))
        while choice == 'hit':
            player.hit()
            player.show_hand()
            if player.get_value() > 21:
                player.isBust = True
                print("%s goes bust!" % player.name)
                break
            elif player.get_value() == 21:
                player.stand()
                break
            elif player.get_value() == 21 and len(player.hand) == 2 and not player.isSplit:
                player.stand()
                break
            choice = input_func("Hit or Stand? ", str.lower, range_=('hit', 'stand'))

        if choice == 'stand':
            player.stand()

        if choice == 'double':
            chips -= player.bet
            player.bet *= 2
            print("New balance = %d" % chips)
            player.hit()
            player.show_hand()
            player.check_bust()

        if choice == 'surrender':
            player.isSurrender = True
            chips += (player.bet - player.bet / 2)
            print("New balance = %d" % chips)

        if choice == 'split':
            chips -= player.bet
            print("New balance = %d" % chips)
            player.split.append(Player(' Split_1', deck, player.bet))
            player.split.append(Player(' Split_2', deck, player.bet))
            for p in player.split:
                p.add_card(player.hand.pop(0))
                p.add_card(deck.deal_card())
                p.isSplit = True
                play(p, deck)

def input_func(prompt, type_ = None, min_ = None, max_ = None, range_ = None):
    value = ''
    while True:
        value = input(prompt)
        if type_ is not None:
            try:
                value = type_(value)
            except ValueError:
                print("Sorry I don't understand.")
                continue
        if min_ is not None and value < min_:
            print("Sorry your input can not be less than %d!" % min_)
        elif max_ is not None and value > max_:
            print("Sorry your input can not be more than %d!" % max_)
        elif range_ is not None and value not in range_:
            print("You must select from", range_)
        else:
            break
    return value


def report(player, dealer):
    global chips
    if player.isSurrender:
        tag = 'Surrender'
    elif player.isBust:
        tag = 'Lose'
    elif len(player.hand) == 2 and player.get_value() == 21 and not player.isSplit:
        tag = 'Blackjack'
        chips += player.bet * 1.5
    elif dealer.isBust or (player.get_value() > dealer.get_value()):
        tag = 'Win'
        chips += player.bet * 2
    elif player.get_value() == dealer.get_value():
        tag = 'Push'
        chips += player.bet
    else:
        tag = 'Lose'
    print("%s: %-*s Balance = %d" % (player.name, 10, tag, chips))


def game():
    players = []
    global chips
    deck = Deck()

    player_num = input_func("\nPlease enter the number of players: (1-4) ", int, 1, max_players)

    print("\nLet's get started...\n")

    for i in range(player_num):
        if chips > 0:
            player_name = 'Player_' + str(i + 1)
            print("%s:" % player_name)
            player_bet = input_func("Please bet. The minimal bet is 1 chip. ", int, 1, chips)
            chips -= player_bet
            print("Balance updated. New balance is %d." % chips)
            player = Player(player_name, deck, player_bet)
            players.append(player)
        else:
            print("\nThe actual number of players is %d. There's no balance to support more players." % (len(players)))
            break

    dealer = Dealer('Dealer', deck)

    for i in range(2):
        for player in (players + [dealer]):
            player.add_card(deck.deal_card())

    dealer.hand[1].hide_card()
    print("\nDealer:")
    dealer.show_hand()
    print
    dealer.hand[1].reveal_card()

    for player in (players + [dealer]):
        play(player, deck)
        print

    print("...Final result...\n")

    for player in players:
        if not player.split:
            report(player, dealer)
        else:
            print("%s: split" % player.name)
            for p in player.split:
                report(p, dealer)

    print("\nFinal chip balance is %d.\n" % chips)


if __name__ == '__main__':

    chips= input_func("\nWelcome to Shyahn's Blackjack! Please enter the amount of chips you would like to use this round: (1-1000) ", int, 1, player_money)
    while True:
        game()
        if chips < 1:
            print("You don't have enough chips to proceed. Game over.")
            break
        proceed = input_func("Do you want to continue? (yes/no) ", str.lower, range_ = ('yes', 'no'))
        if proceed == 'no':
            print("\nThank you for playing! See you next time.")
            break

# Detail insurance_wager()