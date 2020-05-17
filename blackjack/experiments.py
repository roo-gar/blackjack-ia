from time import sleep

import random

GAMMA = 0.5
K = 0.8


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
        for p in range(2, 21):
            for q in range(1, 10):
                self.entries.append(QMatrixEntry(State(p, q), HIT, 0))
                self.entries.append(QMatrixEntry(State(p, q), STAND, 0))
                self.entries.append(QMatrixEntry(State(p, q), DOUBLE, 0))

    def get_entry(self, state, action):
        for q_matrix_entry in self.entries:
            if q_matrix_entry.state == state and q_matrix_entry.action == action:
                return q_matrix_entry

    def get_probability(self, state, action, possible_actions):
        log("{}, {}, {}".format(state, action, possible_actions))
        k_current_reward = K ** self.get_entry(state, action).reward
        k_sum_rewards = sum([K ** self.get_entry(state, action).reward for action in possible_actions])

        return current_reward / sum_rewards


QM = QMatrix()
current_state, current_action = None, None
previous_state, previous_action, previous_hand_result = None, None, None

LOG = True

def log(msg):
    if LOG:
        print(msg)
        sleep(3.0)


def get_card_value(card_value):
    return 1 if card_value == 'a' else 10 if card_value in ['j', 'q', 'k'] else int(card_value)


def get_state(player_hand, dealer_hand):
    player_hand_value = sum([get_card_value(card[1:len(card)]) for card in player_hand])
    dealer_hand_value = get_card_value(dealer_hand[1:len(dealer_hand)])

    return State(player_hand_value, dealer_hand_value)


def random_choice(elements, weights):
    log("actions: {}", elements)
    log("weights: {}", elements)
    element_chosen = elements[-1]
    random_number = random.random()
    log("random: {}".format(random_number))
    suma = 0
    for i in range(len(weights)):
        suma += weights[i]
        if random_number < suma:
            return element_chosen
    return element_chosen


def get_reward(hand_result):
    rewards = {NO_RESULT_YET: 0, PLAYER_WON: 1, PLAYER_LOST: -1, DRAW: 0, PLAYER_WON_DOUBLE: 2, PLAYER_LOST_DOUBLE: -2}
    return rewards[hand_result]


def update_matrix(possible_actions):
    if not (previous_state and current_state and previous_action and current_action and previous_hand_result):
        return
    
    entry_to_update = QM.get_entry(previous_state, previous_action)
    print("Before update: {}".format(entry_to_update))
    entry_to_update.visit()
    alpha = 1 / (1 + entry_to_update.visits)

    if previous_hand_result == NO_RESULT_YET:
        max_reward = get_max_reward(current_state, possible_actions)
        entry_to_update.reward = (1 - alpha) * entry_to_update.reward + alpha * math.floor(get_reward(previous_hand_result) + GAMMA * max_reward)
    else:
        entry_to_update.reward = (1 - alpha) * entry_to_update.reward + alpha * get_reward(previous_hand_result)
    print("After update: {}".format(entry_to_update))


# Method called by the game to request the next action
def get_action(player_hand, dealer_hand):
    global previous_state, current_state, previous_action, current_action
    log("Player hand: {}, dealer_hand: {}".format(player_hand, dealer_hand))

    previous_state = current_state
    current_state =  get_state(player_hand, dealer_hand)
    log("Current State: {}".format(current_state))

    previous_action = current_action
    possible_actions = [HIT, STAND, DOUBLE] if len(player_hand) == 2 else [HIT, STAND]
    actions_probabilities = [QM.get_probability(current_state, action, possible_actions) for action in possible_actions]
    current_action = random_choice(possible_actions, actions_probabilities)
    log("Current Action: {}".format(current_action))
    update_matrix(possible_actions)

    return current_action


# Method called by the game which to process the hand result
def process_result(hand_result):
    global previous_hand_result
    previous_hand_result = hand_result


# Method called by the game every time a new hand is deal
def on_game_start(handsPlayed, funds):
    log("Hand #{}: ${}".format(handsPlayed, funds))

    with open("funds.txt", "a") as file: 
        file.write("{}, {}\n".format(handsPlayed, funds))


""" Random strategy 
def get_action(player_hand, dealer_hand):
    state = get_state(player_hand, dealer_hand)

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
"""

s1 = State(2, 2)
s2 = State(2, 2)
print(s1 == s2)
""" Random strategy 
def get_action(player_hand, dealer_hand):
    state = get_state(player_hand, dealer_hand)

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
"""
