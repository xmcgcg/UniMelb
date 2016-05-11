from random import shuffle


def get_new_deck():
    """
    get_new_deck takes nothing and returns a list of strings, 
    where the first character represents a face value and the 
    second character represents a suit; the list has 52 card.
    """

    deck = []
    for face in "234567890JQKA":
        for suit in "SCHD":
            deck.append(face + suit)
    shuffle(deck)
    return deck

def join_discard_pile(deck, discard_pile):
    """
    join_discard_pile takes a list os strings <deck>, which 
    represents the current deck, and a list of strings 
    <discard_pile>, which represents the current discard 
    pile; the function shuffles the discard pile and appends 
    it to the deck and returns None.
    """

    shuffle(discard_pile)
    deck += discard_pile
    return None

