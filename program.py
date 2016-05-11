FACES = "234567890JQKA"
SUITS = "SCHD"
FULL_DECK = []
for face in FACES:
    for suit in SUITS:
        FULL_DECK.append(face + suit)


class game_data():
    def __init__(self):
        self.remaining_deck = FULL_DECK
        self.discard_pile = []


    def __init__(self, other, current_discard):
        self.remaining_deck = other.remaining_deck
        self.discard_pile = other.discard_pile
        for card in current_discard:
            self.remaining_deck.remove(card)
            self.discard_pile.append(card)


    def process(cards):
        for card in cards:
            self.remaining_deck.remove(card)
            self.discard_pile.append(card)
    

    def reshuffle():
        self.remaining_deck += discard_pile
        self.discard_pile.clear()


def greater_face(face1, face2):
    """
    Purpose:
    between two cards, find the one with higher face value.
    Parameters:
    face1 and face2: two 1-digit strings, representing the face value.
    Return value:
    True, if <face1> is greater than <face2> in the name;
    otherwise False.
    """

    pos1 = FACES.index(face1)
    pos2 = FACES.index(face2)
    return bool(pos1 > pos2)


def winning_player(tricks, deck_top):
    """
    Purpose:
    find the winner for a round based on the tricks played and the trump card.
    Parameters:
    tricks: a 4-tuple containing strings, representing the tricks played.
    deck_top: a 2-digit string, representing the trump card.
    Return value:
    An integer representing the player number of the winner.
    """

    trump = deck_top[1]
    winning_suit = ""
    if trump in [card[0] for card in tricks]:
        winning_suit = trump
    else:
        winning_suit = tricks[0][1]
    
    winning_card = ""
    for card in tricks:
        if card[1] == winning_suit:
            if not winning_card or \
                greater_face(card[1], winning_card[1]):
                winning_card = card
    return tricks.index(card)


def is_winner(tricks, deck_top, player_no):
    """
    Purpose:
    check whether a player is the winner for this round 
    based on the tricks played and the trump card.
    Parameters:
    tricks: a 4-tuple containing strings, representing the tricks played.
    deck_top: a 2-digit string, representing the trump card.
    player_no: an integer from 0 to 3, representing the target player number.
    Return value:
    True, if the target player is the winner;
    otherwise False.
    """

    return winning_player(tricks, deck_top) == player_no


def winning_probability(possible_cards, play, deck_top, player_no):
    """
    Purpose:
    Calculate the probability of winning for a given play.
    Parameters:
    possible_cards: a list of strings representing all possible 
                    cards in other players' hands.
    play: a 2-digit string, representing a potential play.
    deck_top: a 2-digit string, representing the trump card.
    player_no: an integer from 0 to 3, representing the target player number.
    Return value:
    A floating point number from 0.0 to 1.0, representing the probability.
    """

    total_tests = 0
    total_wins = 0

    for other1 in possible_cards:
        for other2 in possible_cards:
            if other1 == other2:
                continue
            
            for other3 in possible_cards:
                if other3 in (other1, other2):
                    continue

                tricks = [other1, other2, other3].insert(play, player_no)
                if is_winner(tricks, deck_top, player_no):
                    total_wins += 1
                total_tests += 1
    
    return total_wins / total_tests


def special_bid(forehaead, deck_top, player_no, 
                player_data, suppress_player_data):
    """
    Purpose:
    Make an optimum bid only based on the trump card and the cards 
    from other players in phase 1 and 19.
    Parameters:
    forehead: a 3-tuple containing strings, representing the cards 
              from other players.
    deck_top: a 2-digit string, representing the trump card.
    player_no: an integer from 0 to 3, representing the target player number.
    player_data: a self-defined data structure containing custon game info.
    suppress_player_data: if it is True, player_data should not be used.
    Return value:
    an integer 0 or 1 based on calculations, 
    and the new game data if suppress_game_data is False.
    """

    possible_cards = FULL_DECK.copy()
    impossible_cards = list(forehead) + [deck_top]

    if suppress_player_data:
        for card in impossible_cards:
            possible_cards.remove(card)
    else:
        player_data.process(impossible_cards)
        for card in player_data.remaining_deck:
            possible_cards.remove(card)

    total_tests = 0
    total_wins = 0
    for card in possible_cards:
        forehead_list = list(forehaead)
        forehead_list.insert(player_no, card)
        if is_winner(tuple(forehead_list), deck_top, player_no):
            total_wins += 1
        total_tests += 1

    if total_wins / total_tests < 0.5:
        return 0
    else:
        return 1


def simple_normal_bid(hand, deck_top, player_no):
    """
    Purpose:
    Make an optimum bid only based on the trump card and plyers hand 
    from phase 2 to 18.
    Parameters:
    hand: a n-tuple containing strings, representing the hand.
    dect_top: a 2-digit string, representing the trump card.
    player_no: an integer from 0 to 3, representing the target player number.
    Return value:
    an integer from 0 to 9, based on calculations.
    """

    possible_cards = FULL_DECK.copy()
    for card in hand:
        possible_cards.remove(card)
    possible_cards.remove(deck_top)
    
    winning_probabilities = []
    for play in hand:
        winning_probabilities.append(winning_probability\
            (possible_cards, play, deck_top, player_no))

    possible_wins = sum(winning_probabilities) / len(winning_probabilities)
    return int(possible_wins + 0.5)


def is_valid_play(play, curr_trick, hand):
    """
    is_valid_play takes a string <play>, which is a single card 
    representing a potential play; a tuple <curr_tricks>, which 
    indicates the card(s) have been played in the current round; 
    and a tuple <hand>, which is the tuple of cards that the 
    player is holding in his/her hand.
    """

    leading_suit = ""
    if curr_trick:
        leading_suit = curr_trick[0][1]
    else:
        return True

    my_suit = play[1]
    if my_suit == leading_suit:
        return True

    for card in hand:
        if card[1] == leading_suit:
            return False
    return True