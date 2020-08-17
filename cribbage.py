from deck import Deck, Card
from collections import Counter

class Cribbage(object):
    """ Find number of points in a cribbage hand """

    @staticmethod
    def _findFifteensRec(dp, hand, i, target, path, total):
        """
        Helper method just to take a 2D array filled by subset sum, and
        increment total for each possible 15 that can be made
        """
        # If we reached end and sum is non-zero. We print
        # p[] only if arr[0] is equal to sun OR dp[0][sum]
        # is true.
        if (i == 0 and target != 0 and dp[1][target]):
            path.append(hand[i])
            return total + 2

        # If target becomes 0
        if i == 0 and target == 0:
            return total + 2

        # if the element i IS in the 15
        if target >= hand[i] and dp[i][target-hand[i]]:
            path.append(hand[i])
            total = Cribbage._findFifteensRec(dp, hand, i-1, target-hand[i], path, total)
            path.pop()

        # if the element i is NOT in the 15
        if dp[i][target]:
            path_2 = path[:]
            total = Cribbage._findFifteensRec(dp, hand, i-1, target, path_2, total)

        return total

    @staticmethod
    def findFifteens(hand):
        # given a set of non-negative numbers, find all possible combinations
        # that sum to be a target (15)

        # essentially perfect subset sum.
        # Becuase I know that the length of the hand is five,
        # I could just brute force it, and that would probably be faster

        # but given that this is just a personal project, I'll take the time to
        # implement the subset sum with ~~*dynamic programming*~~


        #start by solving subset sum, building the array
        hand = [card.getNum() for card in hand]

        target = 15
        n = len(hand)
        # Index i, j means that from hand[0... i] contains a subsetsum of target j
        # initialize a 2d array of size [len(hand)+1][target+1]

        # idea from https:www.geeksforgeeks.org/subset-sum-problem-dp-25/
        # implementation is my own
        dp = []
        for i in range(n + 1):
            dp.append([])
            for j in range(target + 1):
                dp[i].append(0)

        for i in range(n+1):
            dp[i][0] = 1

        for j in range(1, target+1):
            # for i, line in enumerate(dp):
            #     print(str(hand[i-1]) + str(line))
            # print("__________________")
            for i in range(n+1):
                if i == 0:
                    dp[i][j] = 0
                elif hand[i-1] > j:
                    dp[i][j] = dp[i-1][j]
                else:
                    dp[i][j] = dp[i-1][j] or dp[i-1][j - hand[i-1]]

        # for line in dp:
        #     print(line)

        if not dp[n][target]:
            return 0

        total = 0
        path = []
        total = Cribbage._findFifteensRec(dp, hand, n-1, target, path, total)

        return total

    @staticmethod
    def findPairs(hand):
        num_hand = [card.getVal() for card in hand]
        count = Counter(num_hand)

        total = 0
        for num in count:
            total += (count[num]-1)*count[num]
        return total

    @staticmethod
    def findRuns(hand):
        # could implement a counting sort or something, but for 5 elems feels like overkill
        run_hand = sorted([card.getRunNum() for card in hand])
        seen = set()
        count = Counter(run_hand)
        total = 0
        for num in run_hand:
            length = 1
            next = True
            if num not in seen:
                run_points = 1
                while next:
                    seen.add(num)
                    if (num+1) not in count:
                        next = False
                    else:
                        length += 1
                        run_points *= count[num]
                        num += 1
            if length >= 3:
                run_points *= count[num]
                run_points *= length
                total += run_points
        return total

    @staticmethod
    def findFlush(hand):
        suit_hand = [card.getSuit() for card in hand]
        suit_count = Counter(suit_hand)
        total = sum([suit_count[suit] for suit in suit_count if suit_count[suit] >= 4])

        return total

    @staticmethod
    def findNobs(hand):
        # NOTE this assumes that the last card in the list was the cut card
        nobs_suit = hand[-1].getSuit()
        for i in range(len(hand)-1):
            card = hand[i]
            if card.getVal() == "J" and card.getSuit() == nobs_suit:
                return 1
        return 0

    @staticmethod
    def findPoints(hand):
        return (Cribbage.findFifteens(hand)
                + Cribbage.findPairs(hand)
                + Cribbage.findRuns(hand)
                + Cribbage.findFlush(hand)
                + Cribbage.findNobs(hand))

    @staticmethod
    def bestChoice(deck, hand, get_max=False):
        # in cribbage you discard two cards, and then some other card is cut from
        # the deck. You use these 5 cards to make up your hand

        # check for point value if not using card1, index i, and card2, index j
        # a total of 30 options for 5 cards
        discard_options_max = {}
        discard_options_avg = {}

        for i, card1 in enumerate(hand):
            for j, card2 in enumerate(hand):
                if i != j:
                    # for this one discard, the options
                    avg_hand_val = 0
                    num_checked = 0
                    max_hand_val = 0
                    discarding = [card1, card2]
                    remaining_cards = [card for card in hand if card not in discarding]
                    for card in deck.getDeck():
                        remaining_cards.append(card)
                        hand_val = Cribbage.findPoints(remaining_cards)
                        avg_hand_val += hand_val

                        if hand_val > max_hand_val:
                            max_hand_val = hand_val
                            discard_options_max[(i, j, card)] = max_hand_val
                        num_checked += 1
                        remaining_cards.pop()

                    avg_hand_val /= num_checked
                    discard_options_avg[(i, j)] = avg_hand_val

        highest_max_discard = max(discard_options_max, key=discard_options_max.get)
        highest_avg_discard = max(discard_options_avg, key=discard_options_avg.get)

        if get_max:
            # print("Max discard with", highest_max_discard, "yielding", discard_options_max[highest_max_discard])
            return highest_max_discard
        # print("Highest avg discard with", highest_avg_discard, "yielding", discard_options_avg[highest_avg_discard])
        return highest_avg_discard
