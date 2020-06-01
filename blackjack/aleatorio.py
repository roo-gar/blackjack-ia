from tabulate import tabulate

import json
import math
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
    if len(player_hand) == 2:
        return random.choice([HIT, STAND, DOUBLE])
    return random.choice([HIT, STAND])

def process_result(hand_result):
    pass

def on_game_start(handsPlayed, funds):
    if handsPlayed % 50 == 0:
        with open("logs/funds-random.txt", "a") as file: 
            file.write("{}\n".format(funds))

