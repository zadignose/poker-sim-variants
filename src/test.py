from variants import *
from poker_mechanics import *

def handpick():
    evaluator = eval_rule_set()
    card1 = Card("h", "5")
    card2 = Card("h", "4")
    card3 = Card("h", "3")
    card4 = Card("h", "7")
    card5 = Card("h", "6")
    hand1 = [card1, card2, card3, card4, card5]
    card6 = Card("s", "14")
    card7 = Card("s", "5")
    card8 = Card("s", "4")
    card9 = Card("s", "3")
    card10 = Card("s", "2")
    hand2 = [card6, card7, card8, card9, card10]
    print(str(evaluator.HandValue(hand1)))
    print(str(evaluator.HandValue(hand2)))



def main():
    tbl = Table()
    p1 = Player("Oliver")
    p2 = Player("Sally")
    p3 = Player("Wanda")
    vals = []
    tbl.add_players([p1, p2, p3])
    for _ in range (0, 5):
        tbl.deal_around()
    evaluator = eval_rule_set()
    vals.append(evaluator.HandValue(p1.hand))
    vals.append(evaluator.HandValue(p2.hand))
    vals.append(evaluator.HandValue(p3.hand))

    highest = max(vals)
    winner = vals.index(highest)
    print(tbl.__repr__())

    print(f"The winner is Player #{winner + 1}\n\n")

    # evaluator = eval_rule_set()
    # evaluator.HandValue(p1.hand)
    # print(tbl.__repr__())
def mainish():
    # myC = Card("h", 12)
    # print(myC.show())
    # dee = Dealer()
    #dee.add_joker()
    #myC = Card()

    tbl = Table(7)

    plr1 = Player("Sally")
    plr2 = Player("Wendy")
    plr3 = Player("Farrah")

    tbl.add_players([plr1, plr2, plr3])
    # tbl.deal_around()
    # tbl.deal_around()
    # tbl.burn()
    # tbl.deal_to_board()
    # tbl.deal_to_board()
    # tbl.deal_to_board()
    # tbl.deal_to_board()
    # tbl.deal_to_board()

    tbl.PlayHand()
    print(tbl.__repr__())

    plr4 = Player("Waldo")
    tbl.add_players([plr4])
    #
    tbl.PlayHand()
    print(tbl.__repr__())
    #
    tbl.remove_player(1)
    #
    tbl.PlayHand()
    #
    print(tbl.__repr__())
    # for i in range (7):
    #     plr1.give_card(dee.deal())

    # print(plr1.__repr__())

    # for i in range (53):
    #     myC = dee.deal()
    #     print(myC.show(), end = " ")

def SetAndShowVariantData():
    nlhe = variant()
    nlhe.SetName(HOLDEM)
    nlhe.SetStructure(NO_LIMIT)
    nlhe.SetActionList([POST, DEAL_DOWN, DEAL_DOWN, BET, BURN, DEAL_COMMUNITY,
                             DEAL_COMMUNITY, DEAL_COMMUNITY, BET, BURN, DEAL_COMMUNITY,
                             BET, BURN, DEAL_COMMUNITY, BET, SHOW_DOWN, PAY_OUT])
    nlhe.SetPayType(HI_ONLY)

    print(nlhe.__repr__())

if __name__ == "__main__":
    handpick()