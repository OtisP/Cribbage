from deck import Deck, Card
from collections import Counter

class Cribbage(object):
    # TODO: NOBS

    @staticmethod
    def _findFifteensRec(dp, hand, i, target, path, total):
        # If we reached end and sum is non-zero. We print
        # p[] only if arr[0] is equal to sun OR dp[0][sum]
        # is true.
        if (i == 0 and target != 0 and dp[1][target]):
            path.append(hand[i])
            # print(path)
            return total + 2

        # If target becomes 0
        if i == 0 and target == 0:
            # print(path)
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
        run_hand = [card.getRunNum() for card in hand]
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
    def findPoints(hand):
        return (Cribbage.findFifteens(hand)
                + Cribbage.findPairs(hand)
                + Cribbage.findRuns(hand)
                + Cribbage.findFlush(hand))

def main():
    deck = Deck()

    deck.shuffleDeck()


    hand = [Card("6", "S"),Card("9", "S"),Card("6", "C"),Card("4", "D"),Card("5", "H")]


    # print(findFifteens(hand))
    # print(findPairs(hand))
    # print(findRuns(hand))
    # print(findFlush(hand))

    print(Cribbage.findPoints(hand))


if __name__ == '__main__':
    main()
