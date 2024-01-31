import random

valid_moves = ['r', 'p', 's']

# returns whether user wins: 
#   1 for win
#   0 for tie
#   -1 for lose
def check_win(bot_move, user_move):
    # Maps to a tuple for results of particular user move (win, lose, tie)
    bot_move_results = {
        'r': ('p', 's', 'r'),
        'p': ('s', 'r', 'p'),
        's': ('r', 'p', 's'),
    }

    result = bot_move_results[bot_move]
    if user_move == result[0]:
        return 1
    if user_move == result[1]:
        return -1
    return 0

while True:
    user_move = input("Rock, paper, or scissors? (r, p, s) ")
    if user_move not in valid_moves:
        continue
    
    bot_move = random.choice(valid_moves)
    print(f'Bot plays {bot_move}')
    user_won = check_win(bot_move, user_move)

    match user_won:
        case 1:
            print("You win!")
        case 0:
            print("You tied.")
        case -1:
            print("You lost...")
