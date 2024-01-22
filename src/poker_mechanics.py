import random
from variants import *

turn_order = [POST, DEAL_DOWN, DEAL_DOWN, BET, BURN, DEAL_COMMUNITY,
              DEAL_COMMUNITY, DEAL_COMMUNITY, BET, BURN, DEAL_COMMUNITY,
              BET, BURN, DEAL_COMMUNITY, BET, SHOW_DOWN, PAY_OUT]


class Card:
    # A Joker will have suit "Jkr" and value 0
    def __init__(self, suit = "Jkr", value = 0):
        self.suit = suit
        self.value = value
        self.face_up = False

    def __repr__(self):
        return self.show()

    def GetValue(self):
        return int(self.value)

    def SetValue(self, v):
        self.value = v

    def GetSuit(self):
        return self.suit

    def SetSuit(self, s):
        self.suit = s

    def SetFaceUp(self, up = True):
        self.face_up = up

    def IsFaceUp(self):
        return self.face_up

    def show_raw(self):
        print(f"{self.suit}{self.value}", end=" ")

    def show(self):
        show_suit = ""
        show_value = ""

        match self.suit:
            case "h":
                show_suit = "♥"
            case "d":
                show_suit = "♦"
            case "c":
                show_suit = "♣"
            case "s":
                show_suit = "♠"
            case _:
                show_suit = self.suit
        
        match self.value:
            case 0:
                pass
            case 1:
                show_value = "A"
            case 11:
                show_value = "J"
            case 12:
                show_value = "Q"
            case 13:
                show_value = "K"
            case 14:
                show_value = "A"
            case _:
                show_value = str(self.value)

        return f"{show_suit}{show_value}"

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def __repr__(self):
        holder = f"Number of Cards = {len(self.cards)}\n\n"
        j = 0
        while j < len(self.cards):
            for i in range (13):
                while j < len(self.cards):
                    holder += self.cards[j].show()
                    j +=1
            holder += "\n"
        return holder

    def build(self):
        for suit in ["h", "d", "c", "s"]:
            for value in range(2, 15):                  # Aces valued at 14, but will be
                self.cards.append(Card(suit, value))    # be evaluated as low end of A-5
                                                        # straight or set low for some lowball
                                                        # variants
    def add_joker(self):
        self.cards.append(Card("Jkr", 0))

class Dealer:
    def __init__(self):
        self.deck = Deck()
        self.shuffle()
    
    def reset_deck(self):
        # self.deck = Deck()
        self.deck.__init__()
        self.shuffle()
        #print("resetting deck!  Watch for the __repr__ function!!!!")
        #print(self.deck.__repr__())

    def shuffle(self):
        random.shuffle(self.deck.cards)

    def add_joker(self):
        self.deck.add_joker()
        self.shuffle()

    def deal(self, up = False):     # Pass argument True to deal face up
        crd = self.deck.cards.pop()
        crd.SetFaceUp(up)
        return crd
    
class Player:
    def __init__(self, name = ""):
        self.name = name
        self.hand = []
        self.own_chips = 0
        self.bet_chips = 0
        self.folded = False
        self.all_in = False
        self.pot_share = 0  # When hand is over, but payout has not yet occurred, this
                            # flags a player to receive a share of the pot. It is an inverse,
                            # i.e., "1" wins the whole pot, "4" is 1/4 pot, "6" is 1/6, etc.

        # List of actions
        # 0: Check
        # 1: Bet
        # 2: Call
        # 3: Raise
        # 4: Fold
        # 5: All-in
        self.actions_allowed = [False, False, False, False, False, False]

    def __repr__(self):
        holder = "["
        for i in range (len(self.hand)):
            holder += self.hand[i].__repr__() + " "
        holder = holder.strip(" ") + "]"
        return holder

    def set_name(self, n):
        self.name = n

    def get_name(self):
        return self.name
    def give_card(self, crd):
        self.hand.append(crd)
    def action_check(self):
        if self.actions_allowed[0]:
            return True
        else:
            return False
    
    def action_bet(self, bet_chips):
        if self.actions_allowed[1]:
            self.own_chips -= bet_chips
            self.bet_chips += bet_chips
            return True
        else:
            return False
        
    def action_call(self, call_chips):
        if self.actions_allowed[2]:
            self.own_chips -= call_chips
            self.bet_chips += call_chips
            return True
        else:
            return False
        
    def action_raise(self, raise_chips):
        if self.actions_allowed[3]:
            self.own_chips -= raise_chips
            self.bet_chips += raise_chips
            return True
        else:
            return False
        
    def action_fold(self):
        if self.actions_allowed[4]:
            self.hand = []
            self.folded = True
            return True
        else:
            return False
    
    def action_all_in(self):
        if self.actions_allowed[5]:
            self.own_chips = 0
            self.bet_chips += self.own_chips
            self.all_in = True
            return True
        else:
            return False
    
    def reset(self):
        self.hand = []
        self.bet_chips = 0
        self.folded = False
        self.all_in = False

class Table:
    def __init__(self, max = 8):
        self.players = []
        self.dealer = Dealer()
        self.pot = 0
        self.community_cards = []
        self.burns = []  # Keep burn cards in case needed when deck is exhausted
        self.max_players = max

    def __repr__(self):
        holder = ""
        for i in range (len(self.players)):
            holder += (f"Player ({i + 1}): {self.players[i].get_name()} "
                       + self.players[i].__repr__()
                       + "\n")
        holder += "Community Cards: ["
        for i in range (len(self.community_cards)):
            holder += self.community_cards[i].show() + " "
        holder = holder.strip(" ") + "]\n"
        return holder

    def set_max_players(self, max):
        self.max_players = max

    def get_max_players(self):
        return self.max_players
    def reset(self):
        #print("resetting table!!!!! WATCH OUT!!!!!!")
        self.dealer.reset_deck()
        self.pot = 0
        self.community_cards = []
        self.burns = []
        for player in self.players:
            player.reset()

    def deal_to(self, index, fu = False):   # By default, cards are dealt face down, but set
                                            # fu to True for face-up deals (e.g. stud games)
        p = self.players[index]
        p.give_card(self.dealer.deal(fu))

    def deal_around(self, fu = False):
        for i in range (len(self.players)):
            self.deal_to(i, fu)

    def deal_to_board(self):
        crd = self.dealer.deal()
        crd.SetFaceUp(True)         #This function can be simplified as in deal_to()
        self.community_cards.append(crd)

    def burn(self):
        self.burns.append(self.dealer.deal())

    def add_players(self, plrs):
        for i in range (len(plrs)):
            self.players.append(plrs[i])

    def remove_player(self, num = -1):
        self.players.pop(num)

    def PlayHand(self):
        self.reset()
        for i in range (len(turn_order)):
            match turn_order[i]:
                case "Post":
                    pass
                case "Down":
                    self.deal_around()
                case "Bet":
                    pass
                case "Burn":
                    self.burn()
                case "Community":
                    self.deal_to_board()
                case "Show":
                    pass
                case "Pay":
                    pass
                case _:
                    pass

