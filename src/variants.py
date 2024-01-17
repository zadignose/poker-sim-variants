from setup import Card

#CONSTANTS IDENTIFYING VARIANT RULES
#COMMUNITY CARD GAMES
HOLDEM = "Texas Hold'em"
OMAHA = "Omaha"
OMAHA_8 = "Omaha-Eight (Hi-Lo)"
CRAZY_PINEAPPLE = "Crazy Pineapple"
BIG_O = "Big O (Hi-Lo)"
#DRAW GAMES
DRAW = "Five Card Draw"
LOW_2_7 = "Deuce to Seven Lowball"
TRIPLE_DRAW = "Triple Draw Deuce to Seven"
BADUGI = "Badugi"
#STUD GAMES
STUD = "Seven Card Stud"
FIVE_STUD = "Five Card Stud"
RAZZ = "Razz"
EIGHT = "Seven Stud, Hi-Lo, 8 or Better"

#CONSTANTS FOR BETTING STRUCTURE
LIMIT = 101
POT_LIMIT = 102
NO_LIMIT = 103
SPREAD_LIMIT = 104

ANTE = "ante"
SMALl_BLIND = "small blind"
BIG_BLIND = "big blind"
BB_ANTE = "ante on the big blind"
BRING_IN = "bring in"

#MORE CONSTANTS
FIRST_RULE = 1  # Flagging which rule to evaluate if there are more than one, as in hi-lo split
SECOND_RULE = 2

#CONSTANTS FOR ACTIONS -- Dealer game-flow can be defined as a list of actions
#                         such as alternating rounds of dealing and betting.
#                         E.g. Holdem = [POST, DEAL_DOWN, DEAL_DOWN, BET,
#                                       DEAL_COMMUNITY, DEAL_COMMUNITY, DEAL_COMMUNITY,
#                                       BET, DEAL_COMMUNITY, BET, DEAL_COMMUNITY, BET,
#                                       SHOW_DOWN, PAY_OUT]
POST = 201  # This means the dealer calls for players to post antes and blinds before deal
BET = 202   # When all betting rounds have same limits (or no limit)
SMALL_BET = 203     # For games that have structured betting limits
BIG_BET = 204
DEAL_DOWN = 205
DEAL_UP = 206
DEAL_COMMUNITY = 207
EXCHANGE = 208   # For games like Draw where players discard and draw replacements
DISCARD = 209    # For games like Pineapple where players discard but don't draw
SHOW_DOWN = 210
PAY_OUT = 211

class variant:
    def __init__(self, vr = ""):
        self.var_name = vr
        self.action_list = []
        self.hi_only = False
        self.lo_only = False
        self.hi_lo = False
        self.other_split = False
        self.evals = eval_rule_set()
        self.split_evals = eval_rule_set() # It might be best to have two eval_rule_sets to use
                                           # in split games, and let this variant class apply
                                           # them when it comes to the SHOW_DOWN and PAY_OUT
    def SetName(self, vn):
        self.var_name = vn
    def GetName(self):
        return self.var_name
    def SetActionList(self, act_list):
        self.action_list = act_list
    def GetAction(self, i):
        return self.action_list[i]
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
        pass