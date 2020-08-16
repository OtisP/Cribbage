from random import shuffle

suits = ["C", "S", "D", "H"]
values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

def valueToNum(val):
    if val in ["J", "Q", "K"]:
        return 10
    else:
        return int(val)

def valueToRunNum(val):
    if val == "J":
        return 11
    elif val == "Q":
        return 12
    elif val == "K":
        return 13
    else:
        return int(val)

class Card(object):
    def __init__(self, val, suit):
        # all face cards will have value 10
        if suit not in suits:
            raise ValueError("Suit of " + suit + " not valid")
        if val not in values:
            raise ValueError("Value of " + val + " not valid")

        self.suit = suit
        self.val = val
        self.num = valueToNum(val)
        self.run_num = valueToRunNum(val)

    def getSuit(self):
        return self.suit

    def getVal(self):
        return self.val

    def getNum(self):
        return self.num

    def getRunNum(self):
        return self.run_num

    def __repr__(self):
        # TODO: make prettier
        return str(self.val) + str(self.suit)

    def __str__(self):
        # TODO: make prettier
        return str(self.val) + str(self.suit)

class Deck(object):
    def __init__(self):
        self.deck = []
        self.dealt = []
        # make all cards
        for value in values:
            # of all suits
            for suit in suits:
                self.deck.append(Card(value, suit))

    def shuffleDeck(self):
        shuffle(self.deck)

    def dealCard(self):
        dealt_card = self.deck.pop()
        self.dealt.append(dealt_card)
        return dealt_card

    def shuffleBackIn(self):
        # could make shuffleDeck only call if they say so, but it's fine for now
        self.deck.extend(self.dealt)
        self.dealt = []
        self.shuffleDeck()

    def getDeck(self):
        return self.deck

    def getDealt(self):
        return self.dealt

    def __str__(self):
        # TODO: Make prettier
        to_return = ""
        for card in self.deck:
            to_return += card.getSuit() + card.getVal() + ","
        return to_return
