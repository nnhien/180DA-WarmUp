import paho.mqtt.client as mqtt

PUB_TOPIC = f'ece180d/rps/nn'
RECV_TOPIC = f'ece180d/rps/mf'

valid_moves = ['r', 'p', 's']

move_buffer = {
    'other': None,
    'self': None,
}

# returns whether user wins: 
#   1 for win
#   0 for tie
#   -1 for lose
def check_win(other_move, user_move):
    # Maps to a tuple for results of particular user move (win, lose, tie)
    other_move_results = {
        'r': ('p', 's', 'r'),
        'p': ('s', 'r', 'p'),
        's': ('r', 'p', 's'),
    }

    result = other_move_results[other_move]
    if user_move == result[0]:
        return 1
    if user_move == result[1]:
        return -1
    return 0

# MQTT initialization
def on_connect(client, userdata, flags, rc):
    print("Connected!")

    print(f'subscribing to {RECV_TOPIC}')
    client.subscribe(RECV_TOPIC, qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    move_buffer['other'] = message.payload.decode()

client = mqtt.Client()

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect('mqtt.eclipseprojects.io')
client.loop_start()

# Rock paper scissors loop

while True:
    user_move = input("Rock, paper, or scissors? (r, p, s) ")
    if user_move not in valid_moves:
        continue
    move_buffer['self'] = user_move
    client.publish(PUB_TOPIC, user_move, qos=1)

    while move_buffer['other'] == None:
        continue

    print(f'Other player played {move_buffer['other']}')
    user_won = check_win(move_buffer['other'], move_buffer['self'])

    match user_won:
        case 1:
            print("You win!")
        case 0:
            print("You tied.")
        case -1:
            print("You lost...")
    
    move_buffer['other'] = None
    move_buffer['self'] = None
