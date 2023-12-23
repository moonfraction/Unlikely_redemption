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

HEADER = 64                # Number of bytes for the header, specifying the message length
PORT = 5050                # Port to bind the server socket
SERVER = socket.gethostbyname(socket.gethostname()) 
print(socket.gethostbyname(socket.gethostname()))
# SERVER = "192.168.1.13"  # IPv4 address, uncomment and replace if needed
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'           # Encoding format for messages
SUCCESS = "You won the game."
LOST = "You lost the game."
END = "[ESCAPE COMPLETE] Game ended !!!"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


# Function to handle each connected client
def handle_client(conn, addr):
    print(f"[NEW Player] {addr} connected.")
    conn.send("Enter your name: ".encode(FORMAT))
    name = str(conn.recv(HEADER).decode(FORMAT))
    print(f"{addr} is named {name}")
    upper_bound = upper_limit
    lower_bound = lower_limit    
    guess = 0
    while True:
        conn.send(f"Guess 'escape-key' between {lower_bound} and {upper_bound}".encode(FORMAT))
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            msg = int(msg)
            
            # If client takes more than 5 guesses, they will lose the game
            guess += 1
            if guess == 5:
                print(f"{name} lost the game in {guess} guesses.")
                conn.send("You lost the game.".encode(FORMAT))
                conn.close()
                break
            
            print(f"[{name}] guessed {msg}")
            if msg == escape_key:
                conn.send(f"You guessed it right in {guess} guesses.".encode(FORMAT))
                break
            elif (msg > escape_key):
                conn.send("The value is too high".encode(FORMAT))
                if msg < upper_bound:
                    upper_bound = msg
            else:
                conn.send("The value is too low".encode(FORMAT))
                if msg > lower_bound:
                    lower_bound = msg
    if msg == escape_key:
        print(f"{name} won the game in {guess} guesses.")
        conn.send("You won the game.".encode(FORMAT))
        print(f"{name} escaped")
    players[guess] = name
    active = threading.active_count() - 2
    print(f"[ACTIVE Players] = {active}")
    
    if totP == 2:
        if active == 0:
            esc = list(players.keys())
            esc.sort()
            sorted_p = {i: players[i] for i in esc}
            print(f"Players escaped in this order {sorted_p}")
            print("[ESCAPE COMPLETE] Game ended !!!")
            conn.send(END.encode(FORMAT))
    conn.close()

# Function to start the server and listen for incoming connections
def start():
    global totP
    server.listen()
    print(f"[JOINING] Game is accepting players on {SERVER}")
    while True:
        if totP == 2:
            break
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        totP += 1
        print(f"[ACTIVE PLAYERS] = {threading.active_count() - 1}") 
        print(f"Total players entered the game = {totP}")

# Main execution
print("[STARTING] Game is starting...")
players = {}
totP = 0
start()
