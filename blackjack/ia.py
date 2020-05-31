from time import sleep
from tabulate import tabulate

import math
import random


GAMMA = 0.9
K = 1.05


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


class State:

    def __init__(self, p, q):
        self.p = p
        self.q = q

    def __eq__(self, other):
        return self.p == other.p and self.q == other.q

    def __repr__(self):
        return "s({}, {})".format(self.p, self.q)


class QMatrixEntry:

    def __init__(self, state, action, reward):
        self.state = state
        self.action = action
        self.reward = reward
        self.visits = 0

    def visit(self):
        self.visits += 1

    def __repr__(self):
        return "{}, action={}, reward={}, visits={}".format(self.state, self.action, self.reward, self.visits)


class QMatrix:

    def __init__(self):
        self.entries = []
        for p in range(2, 22):
            for q in range(1, 11):
                self.entries.append(QMatrixEntry(State(p, q), HIT, 0))
                self.entries.append(QMatrixEntry(State(p, q), STAND, 0))
                self.entries.append(QMatrixEntry(State(p, q), DOUBLE, 0))

    def get_entry(self, state, action):
        for q_matrix_entry in self.entries:
            if q_matrix_entry.state == state and q_matrix_entry.action == action:
                return q_matrix_entry

    def get_probability(self, state, action, possible_actions):
        k_current_reward = K ** self.get_entry(state, action).reward
        k_sum_rewards = sum([K ** self.get_entry(state, action).reward for action in possible_actions])

        return k_current_reward / k_sum_rewards

    def get_max_reward(self, state, possible_actions):
        max_reward = self.get_entry(state, possible_actions[0]).reward

        for action in possible_actions:
            current_entry_reward = self.get_entry(state, action).reward

            if current_entry_reward > max_reward:
                max_reward = current_entry_reward

        return max_reward

    def pretty_print(self):
        headers, table = ['', 'HIT', 'STAND', 'DOUBLE'], []

        for i in range(0, len(self.entries), 3):
            table.append(['state({}, {})'.format(self.entries[i].state.p, self.entries[i].state.q),
                          self.entries[i].reward, self.entries[i + 1].reward, self.entries[i + 2].reward])

        print tabulate(table, headers, tablefmt="fancy_grid")


QM = QMatrix()
previous_state, previous_action, previous_hand_result = None, None, None

LOG = True

def log(msg):
    if LOG:
        with open("log.txt", "a") as file: 
            file.write("{}\n".format(msg))


def get_card_value(card_value):
    return 1 if card_value == 'a' else 10 if card_value in ['j', 'q', 'k'] else int(card_value)


def get_state(player_hand, dealer_hand):
    player_hand_value = sum([get_card_value(card[1:len(card)]) for card in player_hand])
    dealer_hand_value = get_card_value(dealer_hand[1:len(dealer_hand)])

    return State(player_hand_value, dealer_hand_value)


def random_choice(elements, weights):
    log("actions: {}".format(elements))
    log("weights: {}".format(weights))
    element_chosen = elements[-1]
    random_number = random.random()
    log("random: {}".format(random_number))
    suma = 0
    for i in range(len(weights)):
        suma += weights[i]
        if random_number < suma:
            return elements[i]

    return element_chosen


def get_reward(hand_result):
    rewards = {NO_RESULT_YET: 0, PLAYER_WON: 10, PLAYER_LOST: -10, DRAW: 0, PLAYER_WON_DOUBLE: 20, PLAYER_LOST_DOUBLE: -20}
    return rewards[hand_result]


def update_matrix(new_state, possible_actions):
    if not previous_state:
        log("Nothing to update")
        return
    
    entry_to_update = QM.get_entry(previous_state, previous_action)
    log("Before update: {}".format(entry_to_update))
    alpha = 1.0 / (1 + entry_to_update.visits)
    log("Alpha: " + str(alpha))

    if previous_hand_result == NO_RESULT_YET:
        max_reward = QM.get_max_reward(new_state, possible_actions)
        entry_to_update.reward = (1 - alpha) * entry_to_update.reward + alpha * math.floor(get_reward(previous_hand_result) + GAMMA * max_reward)
    else:
        entry_to_update.reward = (1 - alpha) * entry_to_update.reward + alpha * get_reward(previous_hand_result)
    entry_to_update.visit()
    log("After update: {}".format(entry_to_update))


# Method called by the game to request the next action
def get_action(player_hand, dealer_hand):
    global previous_state, previous_action
    update_matrix(get_state(player_hand, dealer_hand), [HIT, STAND, DOUBLE] if len(player_hand) == 2 else [HIT, STAND])

    log("Player hand: {}, dealer_hand: {}".format(player_hand, dealer_hand))

    current_state =  get_state(player_hand, dealer_hand)
    log("Current State: {}".format(current_state))

    possible_actions = [HIT, STAND, DOUBLE] if len(player_hand) == 2 else [HIT, STAND]
    actions_probabilities = [QM.get_probability(current_state, action, possible_actions) for action in possible_actions]
    current_action = random_choice(possible_actions, actions_probabilities)
    log("Chosen Action: {}".format("HIT" if current_action == 0 else ("STAND" if current_action == 1 else "DOUBLE")))

    previous_state = current_state
    previous_action = current_action
    return current_action


# Method called by the game which to process the hand result
def process_result(hand_result):
    global previous_hand_result
    previous_hand_result = hand_result
    results_name = ["NO_RESULT_YET", "PLAYER_LOST", "PLAYER_WON" , "PLAYER_LOST_DOUBLE", "PLAYER_WON_DOUBLE", "DRAW"]
    log("Result: {}".format(results_name[hand_result]))


# Method called by the game every time a new hand is deal
def on_game_start(handsPlayed, funds):
    global K

    if handsPlayed % 100 == 0:
        K += 0.03
        print("Table hand " + str(handsPlayed))
        QM.pretty_print()
        #sleep(5)

    log("\nHand #{}: ${}".format(handsPlayed, funds))
    """
    if handsPlayed % 50 == 0:
        with open("funds.txt", "a") as file: 
            file.write("{}\n".format(funds))
    """



""" random strategy
def get_action(player_hand, dealer_hand):
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

def on_game_start(handsPlayed, funds):
    print("\nHand #{}: ${}".format(handsPlayed, funds))

    if handsPlayed % 50 == 0:
        with open("funds.txt", "a") as file: 
            file.write("{}\n".format(funds))
"""
