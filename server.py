import socket
import threading 
import random 

# Generate a random number for the players to guess
lower_limit = random.randint(1, 10000)
while True:
    upper_limit = random.randint(20000, 110000)
    if (upper_limit - lower_limit) > 10000 and (upper_limit - lower_limit) < 100000:
        break
escape_key = random.randint(lower_limit, upper_limit)
print(f"Escape-key = {escape_key}  (won't be visible to the client)")


# Configuration for Socket Connection
HEADER = 64                                             # Number of bytes for the header, specifying the message length
PORT = 5050                                             # Port to bind the server socket
SERVER = socket.gethostbyname(socket.gethostname())     # Get the local machine's IP address
ADDR = (SERVER, PORT)                                   # Tuple containing IP address and port
FORMAT = 'utf-8'                                        # Encoding format for messages

SUCCESS = "You won the game."
LOST = "You lost the game."
END = "Game ended !!!"

# Create a socket object and bind it to the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Function to handle each connected client
def handle_client(conn, addr):
    print(f"[NEW Player] {addr} connected.")
    global activeP
    global currentP
    global totP
    global attemptes_allowed
    activeP +=1
    conn.send("Enter your name: ".encode(FORMAT))
    name = str(conn.recv(HEADER).decode(FORMAT))
    print(f"{addr} is named {name}")
    upper_bound = upper_limit
    lower_bound = lower_limit    
    guess = 0
    won = False
    while True:
        conn.send(f"Guess 'escape-key' between {lower_bound} and {upper_bound}".encode(FORMAT).ljust(HEADER))
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            msg = int(msg)
            
            guess += 1
            
            print(f"[{name}] guessed {msg}")
            if msg == escape_key:
                print(f"{name} won the game in {guess} guesses.")
                print(f"{name} escaped")
                conn.send(SUCCESS.encode(FORMAT).ljust(HEADER))
                won = True
                break
            elif guess == attemptes_allowed:
                print(f"{name} lost the game in {guess} guesses.")
                conn.send(LOST.encode(FORMAT).ljust(HEADER))
                break
            elif (msg > escape_key):
                conn.send("The value is too high".encode(FORMAT).ljust(HEADER))
                if msg < upper_bound:
                    upper_bound = msg
            else:
                conn.send("The value is too low".encode(FORMAT).ljust(HEADER))
                if msg > lower_bound:
                    lower_bound = msg

    if(won):
        wonP[name] = [guess, conn]
    players[name] = [guess, conn]
    activeP -= 1
    
    print(f"[ACTIVE PLAYERS] = {activeP}")
    if(currentP == totP and activeP == 0):
        end_game()

# Function to start the server and listen for incoming connections
def start():
    global totP
    global currentP
    server.listen()
    print(f"[JOINING] Game is accepting players on {SERVER}")
    while currentP != totP:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        currentP += 1
        print(f"[ACTIVE PLAYERS] = {threading.active_count() - 1}") 
        print(f"Total players entered the game = {currentP}")

# Function to end the game and send the results to the players
def end_game():
    esc = list(wonP.keys())
    esc.sort()
    # send END to all players in the order of escape
    sorted_p = {i: wonP[i][0] for i in esc}
    print(f"Players escaped in this order {sorted_p}")
    print(END)
    for i in players:
        conn = players[i][1]
        conn.send(END.encode(FORMAT).ljust(HEADER))
        if i in wonP:
            conn.send(f"Congratulations {i}, you escaped in {players[i][0]} guesses".encode(FORMAT).ljust(HEADER))
        else:
            conn.send(f"Sorry {i}, you couldn't escape".encode(FORMAT).ljust(HEADER))
        conn.close()
    
    server.close()
    exit()


# Main execution
print("[STARTING] Game is starting...")
players = {}
wonP = {}
currentP = 0
activeP = 0
totP = int(input("Enter the number of players: "))
if(totP < 2):
    print("Minimum 2 players required to start the game")
    exit()
attemptes_allowed = int(input("Enter the number of attempts allowed: "))
start()
