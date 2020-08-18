from deck import Deck, Card
from cribbage import Cribbage
from random import randrange

class Compare(object):

    @staticmethod
    def compareOnce(deck):
        """
        Purpose: Run a single simulation of 3 strategies (opt, max, rand)
                 playing with the same cribbage hand
        Params: a deck of type Deck
        Return: list of points:
                [0] has num points optimal strategy got
                [1] has num points max strategy got
                [2] has num points random strategy got
        """

        deck.shuffleDeck()
        hand = [deck.dealCard() for i in range(6)]
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

def main():
    deck = Deck()
    print(Compare.compareOnce(deck))

if __name__ == '__main__':
    main()
