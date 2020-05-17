def get_card_value(card_value):
    return 1 if card_value == 'a' else 10 if card_value in ['j', 'q', 'k'] else int(card_value)


def get_action(player_hand, dealer_hand):
    player_hand_value = sum([get_card_value(card[1:len(card)]) for card in player_hand])
    if player_hand_value < 16:
        return HIT
    else:
        return STAND

def process_result(hand_result):
    pass

def on_game_start(handsPlayed, funds):
    #print("\nHand #{}: ${}".format(handsPlayed, funds))

    if handsPlayed % 50 == 0:
        with open("funds.txt", "a") as file: 
            file.write("{}\n".format(funds))