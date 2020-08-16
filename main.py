from deck import Deck, Card
from cribbage import Cribbage

def dealHand(deck):
    deck.shuffleDeck()
    return [deck.dealCard() for i in range(6)]

def bestChoice(deck, hand):
    # in cribbage you discard two cards, and then some other card is cut from
    # the deck. You use these 5 cards to make up your hand

    # check for point value if not using card1, index i, and card2, index j
    # a total of 30 options for 5 cards
    for i, card1 in enumerate(hand):
        for j, card2 in enumerate(hand):
            if i != j:
                
                discarding = [card1, card2]
                remaining_cards = [card for card in hand if card not in discarding]
                for card in deck.getDeck():
                    remaining_cards.append(card)
                    print(Cribbage.findPoints(remaining_cards))
                    remaining_cards.pop()

def main():
    deck = Deck()
    deck.shuffleDeck()
    print(deck)
    hand = dealHand(deck)
    for card in hand:
        print(card)
    bestChoice(deck, hand)
    # print(Cribbage.findPoints(hand))

if __name__ == '__main__':
    main()
