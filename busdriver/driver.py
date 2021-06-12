from enum import Enum
from random import shuffle
import logging

LOGGER = logging.getLogger('bd')


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

    def __str__(self):
        return self.name


class Card:
    def __init__(self, suit, rank):
        if not isinstance(rank, int):
            raise TypeError
        self.suit = suit
        self.rank = rank
    def __repr__(self):
        return '({}, {})'.format(str(self.suit.name), str(self.rank + 1))

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
        LOGGER.debug(self.lanes)
        
        for lane in self.lanes:
            self.strat.log_seen(lane[0])
        self.curr_lane = 0

    def draw(self):
        drawn = self.deck.draw_card()
        LOGGER.debug('Got {}'.format(drawn))
        self.strat.log_seen(drawn)
        return drawn

    def cross_lane(self, direction):
        LOGGER.debug('Aim  {} !'.format(direction))
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

    def query_strat(self, lane_card):
        return self.strat.gen_action(lane_card)

    def attempt_oneshot_drive(self, verbose=False):
        res = True
        while res: 
            if self.curr_lane == 5:
                # full success
                return True
            selected_direction = self.query_strat(self.lanes[self.curr_lane][-1])
            res = self.cross_lane(selected_direction) 

        # catch all
        return False

class Strat:
    def __init__(self):
        self.seen = [0 for i in range(13)]
        self.total_drawn = 0
        
    def log_seen(self, drawn):
        self.seen[drawn.rank] += 1
        self.total_drawn += 1

    def gen_action(self, lane_card):
        # given a lane card, decide on an appropriate direction
        # this can be done by just checking the history of seen
        # cards and selecting the direction with fewer seen
        LOGGER.debug(str(self.seen))

        under_acc = 0
        for i in range(lane_card.rank):
            under_acc += self.seen[i]
        on_acc = self.seen[lane_card.rank]
        over_acc = self.total_drawn - (under_acc + on_acc)

        under_total = lane_card.rank * 4
        over_total = 48 - under_total

        if (under_total - under_acc) > (over_total - over_acc):
            return Direction.LOWER
        else:
            return Direction.HIGHER


def main():
    logging.basicConfig(level=logging.INFO)
    
    tot = 0
    wins = 0
    for i in range(1000000):
        strat = Strat()
        busgame = Busgame(strat)
        res = busgame.attempt_oneshot_drive()
        
        # bookkeeping
        tot += 1
        if res:
            wins += 1

        outcome = 'SUCCESS' if res else 'FAILURE'
            
        logging.info('Run resulted in {}. (Winrate: {}/{}, {})'.format(outcome, wins, tot, round(100 * wins/tot, 3)))

    

if __name__=='__main__':
    main()
