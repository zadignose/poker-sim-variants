from variants import *
def main():
    myVariant = variant()
    myVariant.SetName(HOLDEM)
    myVariant.SetStructure(NO_LIMIT)
    myVariant.SetActionList([POST, DEAL_DOWN, DEAL_DOWN, BET, BURN, DEAL_COMMUNITY,
                             DEAL_COMMUNITY, DEAL_COMMUNITY, BET, BURN, DEAL_COMMUNITY,
                             BET, BURN, DEAL_COMMUNITY, BET, SHOW_DOWN, PAY_OUT])
    myVariant.SetPayType(HI_ONLY)

    print(myVariant.__repr__())
main()