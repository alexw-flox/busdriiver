from enum import Enum
from random import shuffle


class Suit(Enum):
    CLUB = 0
    DIAMOND = 1
    HEART = 2
    SPADE = 3
    
    def __gt__(self, other):
        return self.value > other.value

class Card:
    def __init__(self, suit, rank):
        if not isinstance(rank, int):
            raise TypeError
        self.suit = suit
        self.rank = rank
    def __repr__(self):
        return '({}, {})'.format(str(self.suit.name), str(self.rank))
    def __gt__(self, other):
        return (self.suit, self.rank) > (other.suit, other.rank)

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

def main():
    d = Deck()
    for i in range(52):
        card = d.draw_card()
        print(card)

if __name__=='__main__':
    main()
