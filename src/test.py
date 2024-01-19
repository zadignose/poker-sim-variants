from variants import *
from setup import *

def main():
    nlhe = variant()
    nlhe.SetName(HOLDEM)
    nlhe.SetStructure(NO_LIMIT)
    nlhe.SetActionList([POST, DEAL_DOWN, DEAL_DOWN, BET, BURN, DEAL_COMMUNITY,
                             DEAL_COMMUNITY, DEAL_COMMUNITY, BET, BURN, DEAL_COMMUNITY,
                             BET, BURN, DEAL_COMMUNITY, BET, SHOW_DOWN, PAY_OUT])
    nlhe.SetPayType(HI_ONLY)

    print(nlhe.__repr__())
main()