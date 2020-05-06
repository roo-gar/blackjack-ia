import random

# LIST POSSIBLE ACTIONS
HIT = 0
STAND = 1
DOUBLE = 2

# LIST POSSIBLE OUTCOMES
NO_RESULT_YET = 0
PLAYER_LOST = 1
PLAYER_WON = 2
PLAYER_LOST_DOUBLE = 3
PLAYER_WON_DOUBLE = 4
DRAW = 5


def get_action(player_hand, dealer_hand):
    print(player_hand, dealer_hand)

    if len(player_hand) == 2:
        return random.choice([HIT, STAND, DOUBLE])
    return random.choice([HIT, STAND])

def process_result(hand_result):
    if hand_result == NO_RESULT_YET:
        print("no result yet")
    elif hand_result == PLAYER_WON:
        print("player won")
    elif hand_result == PLAYER_LOST:
        print("player lost")
    elif hand_result == DRAW:
        print("draw")
    elif hand_result == PLAYER_WON_DOUBLE:
        print("player won double")
    elif hand_result == PLAYER_LOST_DOUBLE:
        print("player lost double")
