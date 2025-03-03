import random
import math
from enum import Enum

class FieldType(Enum):
    SPEED_FIELD = 1
    TRAP_FIELD = -1
    RETURN_TO_START = -2
    NORMAL_FIELD = 0

MIN_FIELD_NUMBER = 30
MIN_NUMBER_PLAYERS = 1

field_number = int(input("Enter field number: "))
while field_number <= MIN_FIELD_NUMBER:
    print(f"Please enter a number bigger than {MIN_FIELD_NUMBER}")
    field_number = int(input("Enter field number: "))

if field_number > 200:
    MAX_NUMBER_ON_DICE = int(input("You can choose octagonal (type: 8) or hexagonal (type: 6) dice: "))
    if MAX_NUMBER_ON_DICE != 6 and MAX_NUMBER_ON_DICE != 8:
        MAX_NUMBER_ON_DICE = int(input("Please enter 6 or 8: "))
else:
    MAX_NUMBER_ON_DICE = 6

board = [FieldType.NORMAL_FIELD] * field_number
number_of_players = int(input("Enter the number of players: "))

if number_of_players <= MIN_NUMBER_PLAYERS:
    print("Please enter a number bigger than 1")
    number_of_players = int(input("Enter the number of players: "))

NUMBER_OF_TRAP_FIELDS = math.ceil(0.07 * field_number)
NUMBER_OF_SPEED_FIELDS = math.ceil(0.05 * field_number)

if field_number > 200:
    NUMBER_OF_START_RETURN_FIELD = 2
elif field_number > 50:
    NUMBER_OF_START_RETURN_FIELD = 1
else:
    NUMBER_OF_START_RETURN_FIELD = 0
traps_indices = random.sample(range(3, field_number), NUMBER_OF_TRAP_FIELDS)
print(f"There are {NUMBER_OF_TRAP_FIELDS} trap fields, {NUMBER_OF_SPEED_FIELDS} speed fields and {NUMBER_OF_START_RETURN_FIELD} return to start fields in the game.")

for index in traps_indices:
    board[index] = FieldType.TRAP_FIELD

remaining_indices = [i for i in range(1, field_number - 3) if board[i] == FieldType.NORMAL_FIELD]
speed_indices = random.sample(remaining_indices, NUMBER_OF_SPEED_FIELDS)

for index in speed_indices:
    board[index] = FieldType.SPEED_FIELD

remaining_indices = [i for i in range(10, field_number) if board[i] == FieldType.NORMAL_FIELD]
start_return_indices = random.sample(remaining_indices, NUMBER_OF_START_RETURN_FIELD)

for index in start_return_indices:
    board[index] = FieldType.RETURN_TO_START


def draw_dice() -> int:
    dice = random.randint(1, MAX_NUMBER_ON_DICE)
    print(f"Dice drew the number: {dice}")
    return dice


def overshoot(players, i) -> None:
    backward_move = players[i] - field_number
    players[i] = field_number - backward_move
    print(f"You overshoot! You have to go back {backward_move} fields from the goal 😒. ")


def double_move(players, i) -> None:
    if players[i] > field_number:
        overshoot(players, i)
    elif players[i] == field_number:
        return
    extra_field(players, i)
    print(f"Player {i + 1} you have an additional move ✌️")
    check_field_not_occupied(players, i, players[i])
    if players[i] > field_number:
        overshoot(players, i)
    dice_value = draw_dice()
    players[i] += dice_value


def start_moving(players, i) -> None:
    print(f"Player {i + 1} you can skip start and roll the dice again 😊.")
    dice_value = draw_dice()
    if dice_value == MAX_NUMBER_ON_DICE:
        double_move(players, i)
    players[i] += dice_value


def extra_field(players, i) -> None:
    current_field = board[players[i]]
    if current_field == FieldType.TRAP_FIELD:
        print(f"Player {i + 1} you have entered a trap field. You move back two fields ⛈️.")
        players[i] -= 2
    elif current_field == FieldType.SPEED_FIELD:
        print(f"Player {i + 1} you have entered a speed field. You move forward 3 fields 🚀.")
        players[i] += 3
    elif current_field == FieldType.RETURN_TO_START:
        print(f"Player {i + 1} you have entered a field, where you go back to start 😭.")
        players[i] = 0

    if players[i] > field_number:
        overshoot(players, i)

    if board[players[i]] != FieldType.NORMAL_FIELD:
        extra_field(players, i)
    else:
        print(f"Player {i + 1} is on the field {players[i]}")


def check_field_not_occupied(players, i, field_to_check) -> None:
    for j in range(len(players)):
        if field_to_check != 0 and field_to_check == players[j] and i != j:
            players[j] = 0
            print(f"You knocked out player {j + 1}, and he goes to start field. Congrats 😎!")


def player_move() -> tuple[str, int]:
    players = [0 for _ in range(number_of_players)]
    turn = 1
    while field_number not in players:
        for i in range(len(players)):
            print(f"Player {i + 1} turn:")
            dice = random.randint(1, MAX_NUMBER_ON_DICE)
            print(f"Dice drew the number: {dice}")

            if not players[i] == 0:
                players[i] += dice
            if players[i] == 0 and dice % 2 == 0:
                start_moving(players, i)
            elif dice == MAX_NUMBER_ON_DICE:
                double_move(players, i)
            if players[i] > field_number:
                overshoot(players, i)


            if players[i] == field_number:
                print(f"Player {i + 1} is on the field {field_number}")
                print(f"Player {i + 1} has won the game 🎉!")
                return f"Player {i + 1}", turn

            extra_field(players, i)
            check_field_not_occupied(players, i, players[i])

            if players[i] > field_number:
                overshoot(players, i)

            if players[i] == field_number:
                print(f"Player {i + 1} is on the field {field_number}")
                print(f"Player {i + 1} has won the game 🎉!")
                return f"Player {i + 1}", turn

            print("")
        turn += 1


player_move()

NUMBER_OF_GAMES = 500


def game_on() -> None:
    game_results = [player_move() for _ in range(NUMBER_OF_GAMES)]
    players_win_name = list(list(zip(*game_results))[0])

    win_counts = {}
    for i in range(1, number_of_players + 1):
        win_counts[f"Player {i}"] = 0

    statistics = {}
    for player in players_win_name:
        if player in win_counts:
            win_counts[player] += 1
        else:
            win_counts[player] = 1

    sorted_desc_win_counts = dict(sorted(win_counts.items(), key=lambda item: item[1], reverse=True))

    print("")
    print("")
    print("Statistics 📋:")
    print(f"Players played the game {NUMBER_OF_GAMES} times.")
    print(f"The number of wins of each player: {sorted_desc_win_counts} 🎉🎉")
    least_wins = min(win_counts, key=win_counts.get)
    print("The smallest number of wins:", least_wins, "only", win_counts[least_wins], "wins 😓")
    most_wins = max(win_counts, key=win_counts.get)
    print("The biggest number of wins:", most_wins, "as many as", win_counts[most_wins], " wins 😎")

    for player in game_results:
        if player[0] in statistics:
            statistics[player[0]] += player[1]
        else:
            statistics[player[0]] = player[1]

    average_number_turn_win = {key: int(round(value / win_counts[key], 0)) for key, value in statistics.items()}
    sorted_desc_avg_number_turn_win = dict(
        sorted(average_number_turn_win.items(), key=lambda item: item[1], reverse=True))
    print(f"The average number of turns each player needs to win: {sorted_desc_avg_number_turn_win}")


game_on()
