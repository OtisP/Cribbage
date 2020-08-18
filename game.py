from deck import Deck, Card
from cribbage import Cribbage
from random import randrange

# simulate an entire game

def getHands(deck):
    """
    Params: hand1, hand2 = list of Cards
    Discard1
    """
    hand1 = [deck.dealCard() for i in range(6)]
    hand2 = [deck.dealCard() for i in range(6)]
    return [hand1, hand2]

def simulateGame(players, strat1="opt", strat2="rand"):

    """
    Purpose: simulate a game and return the winner
    Params:
        players: list of 2 strings of players names/tags
        strat1: optimal by default. Decides which strategy "player" uses
        strat1: rand by default. Decides which strategy "player" uses
        options for strats: "opt", "max", or "rand"
    Returns: string of winner's name/tag
    """
    # make sure argument formatted correctly
    if (strat1 not in ["opt", "max", "rand"]
    or strat2 not in ["opt", "max", "rand"]):
        raise ValueError("strat1, as '" + strat1 +"', or strat2, as '" + strat2 +"', not valid.\
        \nOptions are ['opt', 'max', 'rand']")

    strats = [strat1, strat2]
    pts = [0, 0]
    #pick a random number, 0 or 1, and set that person to be the dealer
    dealer = randrange(0,2)
    deck = Deck()

    while True:
        deck.shuffleDeck()
        hands = getHands(deck)
        hand1, hand2 = hands[0], hands[1]
        crib = []

        # simulate only giving players the information they would have
        deck_1_view = Deck()
        deck_1_view.dealCard(hand1)
        deck_2_view = Deck()
        deck_2_view.dealCard(hand2)
        deck_view = [deck_1_view, deck_2_view]

        # print(hand1)
        # print(hand2)
        players_discards = []
        for i in range(2):
            player_discards = tuple()
            if strats[i] == "opt":
                player_discards = Cribbage.bestChoice(deck_view[i], hands[i])
            elif strats[i] == "max":
                player_discards = Cribbage.bestChoice(deck_view[i], hands[i], True)
            elif strats[i] == "rand":
                player_discards = Cribbage.randomChoice(deck_view[i], hands[i])

            players_discards.append(player_discards)
            # print(player_discards)
            larger_num = max(player_discards[0], player_discards[1])
            smaller_num = min(player_discards[0], player_discards[1])
            crib.append(hands[i].pop(larger_num))
            crib.append(hands[i].pop(smaller_num))

        cut_card = deck.dealCard()
        # TODO: 2 POINTS TO DEALER IF JACK IS cut_card

        # TODO: PEGGING GOES HERE

        # the non dealer counts first
        pts[1 - dealer] += Cribbage.findPoints(hands[1 - dealer] + [cut_card])
        if pts[1 - dealer] >= 121:
            return players[1 - dealer]

        pts[dealer] += Cribbage.findPoints(hands[dealer] + [cut_card])
        if pts[dealer] >= 121:
            return players[dealer]

        # make the other person the dealer and reshuffle deck
        dealer = 1 - dealer
        deck.shuffleBackIn()


    return "opt"


def main():
    winners = []
    for i in range(100):
        print(i)
        winners.append(simulateGame(["smart", "rand"], strat1="opt", strat2="rand"))

    print(winners)
if __name__ == '__main__':
    main()
