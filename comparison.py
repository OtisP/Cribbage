from deck import Deck, Card
from cribbage import Cribbage
from random import randrange

class Compare(object):
    @staticmethod
    def dealHand(deck):
        deck.shuffleDeck()
        return [deck.dealCard() for i in range(6)]

    @staticmethod
    def compareOnce(deck):
        deck.shuffleDeck()
        hand = Compare.dealHand(deck)
        optimal_hand = hand[:]
        discards = Cribbage.bestChoice(deck, hand)
        larger_num = max(discards[0], discards[1])
        smaller_num = min(discards[0], discards[1])
        optimal_hand.pop(larger_num)
        optimal_hand.pop(smaller_num)

        max_hand = hand[:]
        discards = Cribbage.bestChoice(deck, hand, True)
        larger_num = max(discards[0], discards[1])
        smaller_num = min(discards[0], discards[1])
        max_hand.pop(larger_num)
        max_hand.pop(smaller_num)

        random_hand = hand[:]
        random_hand.pop(randrange(0, len(random_hand)))
        random_hand.pop(randrange(0, len(random_hand)))

        deck.shuffleDeck()
        cut_card = deck.dealCard()

        optimal_pt = Cribbage.findPoints(optimal_hand + [cut_card])
        max_pt = Cribbage.findPoints(max_hand + [cut_card])
        random_pt = Cribbage.findPoints(random_hand  + [cut_card])

        deck.shuffleBackIn()
        return [optimal_pt, max_pt, random_pt]
