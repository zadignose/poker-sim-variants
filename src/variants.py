# CONSTANTS IDENTIFYING VARIANT RULES
# COMMUNITY CARD GAMES
HOLDEM = "Texas Hold'em"
OMAHA = "Omaha"
OMAHA_8 = "Omaha-Eight (Hi-Lo)"
CRAZY_PINEAPPLE = "Crazy Pineapple"
BIG_O = "Big O (Hi-Lo)"
# DRAW GAMES
DRAW = "Five Card Draw"
LOW_2_7 = "Deuce to Seven Lowball"
TRIPLE_DRAW = "Triple Draw Deuce to Seven"
BADUGI = "Badugi"
# STUD GAMES
STUD = "Seven Card Stud"
FIVE_STUD = "Five Card Stud"
RAZZ = "Razz"
EIGHT = "Seven Stud, Hi-Lo, 8 or Better"

# CONSTANTS FOR BETTING STRUCTURE
LIMIT = "Limit"
POT_LIMIT = "Pot Limit"
NO_LIMIT = "No Limit"
SPREAD_LIMIT = "Spread Limit"

ANTE = "ante"
SMALl_BLIND = "small blind"
BIG_BLIND = "big blind"
BB_ANTE = "ante on the big blind"
BRING_IN = "bring in"

# MORE CONSTANTS
FIRST_RULE = 1  # Flagging which rule to evaluate if there are more than one, as in hi-lo split
SECOND_RULE = 2

HI_ONLY = "High Only"
LO_ONLY = "Lowball"
HI_LO = "High-Low Split"
OTHER_SPLIT = "Other Split"

DEUCE_TO_SEVEN = "Deuce to Seven"
ACE_TO_FIVE = "Ace to Five"
BADUGI_STYLE = "Badugi Style"

# CONSTANTS FOR ACTIONS -- Dealer game-flow can be defined as a list of actions
#                         such as alternating rounds of dealing and betting.
#                         E.g. Holdem = [POST, DEAL_DOWN, DEAL_DOWN, BET,
#                                       DEAL_COMMUNITY, DEAL_COMMUNITY, DEAL_COMMUNITY,
#                                       BET, DEAL_COMMUNITY, BET, DEAL_COMMUNITY, BET,
#                                       SHOW_DOWN, PAY_OUT]
POST = "Post"  # This means the dealer calls for players to post antes and blinds before deal
BET = "Bet"   # When all betting rounds have same limits (or no limit)
SMALL_BET = "S_Bet"     # For games that have structured betting limits
BIG_BET = "B_Bet"
BURN = "Burn"
DEAL_DOWN = "Down"
DEAL_UP = "Up"
DEAL_COMMUNITY = "Community"
EXCHANGE = "Exchange"   # For games like Draw where players discard and draw replacements
DISCARD = "Discard"    # For games like Pineapple where players discard but don't draw
SHOW_DOWN = "Show"
PAY_OUT = "Pay"

class variant:
    def __init__(self, vr = ""):
        self.var_name = vr
        self.action_list = []
        self.pay_type = HI_ONLY
        self.eval = eval_rule_set()
        self.split_eval = eval_rule_set() # It might be best to have two eval_rule_sets to use
                                          # in split games, and let this variant class apply
                                          # them when it comes to the SHOW_DOWN and PAY_OUT
        self.bet_structure = LIMIT
        # Note that the size of structured bets is a property of the table, not the variant
        # and must be handled there.

    def __repr__(self):     #This will be a big part of outputting a variant to a file
        rep_string = ""
        rep_string += f"::NAME={self.var_name}\n"
        rep_string += f"::ACTIONS="
        for i in range(0, len(self.action_list)):
            rep_string += str(self.action_list[i]) + ","
        if rep_string.find(","):
            rep_string = rep_string[:-1] + "\n"   # removing final comma at end of action list
        rep_string += f"::PAY={self.pay_type}\n"
        rep_string += f"::BET={self.bet_structure}\n"
        return rep_string
    def SetName(self, vn):
        self.var_name = vn
    def GetName(self):
        return self.var_name
    def SetActionList(self, act_list):
        self.action_list = act_list
    def AppendAction(self, act):
        self.action_list.append(act)
    def GetAction(self, i):
        return self.action_list[i]
    def NumActions(self):
        return len(self.action_list)
    def SetPayType(self, type = HI_ONLY):
        self.pay_type = type
    def GetPayType(self):
        return self.pay_type
    def SetStructure(self, st):
        self.bet_structure = st
    def GetStructure(self):
        return self.bet_structure
    def HandToHand(self, p1, p2, com = [], rl = FIRST_RULE):   # Pass two hands and any
        pass                                                   # community cards to evaluate

    def EvalHands(self, hnds, com = [], rl = FIRST_RULE): # Find winning hands from a list
        pass                                              # of hands according to selected rule

# EVAL_RULE_SET will be a tough class to define, but its purpose is to establish which hand
# beats which. A standard method for high-only games like HOLDEM and DRAW will be a starting
# point, but stay flexible until lowball rules and irregular games like Badugi (or Badeucey!)
# can eventually be accommodated.
class eval_rule_set:
    def __init__(self):
        basic_type = HI_ONLY
        lo_type = None
        lo_qualifier = 0

    def SortbyRank(self, crd):
        return crd.GetValue()

    def IsWheel(self, five_cards):              # This function assumes cards have
        if (five_cards[0].GetValue() == 14 and       # already been sorted, with Aces
                five_cards[1].GetValue() == 5 and    # valued at 14
                five_cards[2].GetValue() == 4 and
                five_cards[3].GetValue() == 3 and
                five_cards[4].GetValue() == 2):
#            print("I found a wheel!\n")
            return True
        else:
            return False

    def HandValue(self, five_cards):
        five_cards.sort(key = self.SortbyRank, reverse = True)
        summed = 0
        is_straight = True # Assume straight until one card breaks the pattern
        is_flush = True # Assume flush until one card breaks the pattern
        pair_rank = 0
        overpair_rank = 0
        trip_rank = 0
        # first card evaluated here
        suit_to_match = five_cards[0].GetSuit()
        rank_to_watch = five_cards[0].GetValue()
        summed += 2 ** (rank_to_watch - 2)
        # remaining cards evaluated in turn
        for i in range (1, 5):
            this_suit = five_cards[i].GetSuit()
            this_rank = five_cards[i].GetValue()
            summed += 2 ** (this_rank - 2)
            if this_suit != suit_to_match:
                is_flush = False
            if this_rank != (rank_to_watch - 1):
                is_straight = False
            if this_rank == rank_to_watch:
                if trip_rank == this_rank:
                    summed += 2 ** 28           # quads are represented by trip rank
                                                # plus a flag for quads
                elif pair_rank == this_rank:
                    trip_rank = this_rank      # we've made trips, and if there were
                    pair_rank = overpair_rank   # an overpair, it would drop to "pair"
                                                # and together these will make a full house
                elif pair_rank > this_rank:
                    overpair_rank = pair_rank   # we've made two pair
                    pair_rank = this_rank
                else:
                    pair_rank = this_rank       # this must be our first pair
            else:
                rank_to_watch = this_rank
        # special case: must check for a 5432A low straight, adjust value, and sort again
#        print(f"Value at index 0 is {str(five_cards[0].GetValue())}\n")
        if five_cards[0].GetValue() == 14: # would it be better to also check no pair on this?
#            print("Checking for wheel!\n")
            if self.IsWheel(five_cards):
                summed -= 2 ** 14
                is_straight = True
                card_holder = five_cards[0]
                five_cards = five_cards[1:]
                five_cards.append(card_holder)
        # pairs, two pairs, and trips to be valued
        summed += ((pair_rank * 2 ** 13) +
                   (overpair_rank * 2 ** 17) +
                   (trip_rank * 2 ** 21))
        # now flag all power-hands straight and above
        if is_straight and is_flush:
            summed += 2 ** 29
        elif is_straight:
            summed += 2 ** 25
        elif is_flush:
            summed += 2 ** 26
        # now flag full houses
        if trip_rank and pair_rank:
            summed += 2 ** 27
        # quads have already been handled above when trips found one more of same rank
        # if five of a kind is possible due to jokers or wild cards, flag it at 2 ** 28
        return summed


