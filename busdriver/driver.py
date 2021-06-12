from enum import Enum
from random import shuffle


class Suit(Enum):
    CLUB = 0
    DIAMOND = 1
    HEART = 2
    SPADE = 3
    
    def __gt__(self, other):
        return self.value > other.value


class Direction(Enum):
    LOWER = 0
    HIGHER = 1


class Card:
    def __init__(self, suit, rank):
        if not isinstance(rank, int):
            raise TypeError
        self.suit = suit
        self.rank = rank
    def __repr__(self):
        return '({}, {})'.format(str(self.suit.name), str(self.rank))

    # only compare on rank, as per busdriver game
    def __gt__(self, other):
        return self.rank > other.rank
    def __eq__(self, other):
        return self.rank == other.rank


class Deck:
    def __init__(self):
        self.total = 52

        cards = list(range(52))
        shuffle(cards)
        self.remnant = cards
        self.next_idx = 0

    def idx_to_card(self, idx):
        return Card(Suit(idx // 13), idx % 13)

    def draw_card(self):
        selected = self.idx_to_card(self.remnant[self.next_idx])
        self.next_idx += 1
        return selected


class Busgame:
    def __init__(self, strat):
        self.deck = Deck()
        self.strat = strat
        self.lanes = [[self.deck.draw_card()] for i in range(5)]
        self.curr_lane = 0

    def draw(self):
        drawn = self.deck.draw_card()

    def action(self, direction):
        drawn = self.draw()
        lane_card = self.lanes[self.curr_lane][-1]

        if direction == Direction.LOWER:
            if drawn < lane_card:
                # success
                self.lanes[self.curr_lane].append(drawn)
                self.curr_lane += 1
                return True
        elif direction == Direction.HIGHER:
            if drawn > lane_card:
                # success
                self.lanes[self.curr_lane].append(drawn)
                self.curr_lane += 1
                return True

        # catch all
        return False


class Strat:
    def __init__(self):
        self.seen = [0 for i in range(13)]

    def load_starting(self, starting):
        for lane in starting:
            r = lane[0].rank
            self.seen[r] += 1
        
    def log_seen(self, drawn):
        self.seen += [drawn]

    def action(self, lane_card):
        # given a lane card, decide on an appropriate direction
        # this can be done by just checking the history of seen
        # cards and selecting the direction with fewer seen
        return Direction.LOWER


def main():
    b = Busgame(None)
    s = Strat()
    print(b.lanes)
    s.load_starting(b.lanes)
    

if __name__=='__main__':
    main()
