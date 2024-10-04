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
# print(socket.gethostbyname(socket.gethostname()))
# SERVER = "192.168.1.13"  # IPv4 address, uncomment and replace if needed
ADDR = (SERVER, PORT)

FORMAT = 'utf-8'           # Encoding format for messages
SUCCESS = "You won the game."
LOST = "You lost the game."
END = "Game ended !!!"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def send(msg, conn):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


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
            
            # If client takes more than 5 guesses, they will lose the game
            guess += 1
            # if guess == 5:
            #     print(f"{name} lost the game in {guess} guesses.")
            #     conn.send("You lost the game.".encode(FORMAT).ljust(HEADER))
            #     conn.close()
            #     break
            
            print(f"[{name}] guessed {msg}")
            if msg == escape_key:
                print(f"{name} won the game in {guess} guesses.")
                print(f"{name} escaped")
                conn.send(SUCCESS.encode(FORMAT).ljust(HEADER))
                # conn.close()
                won = True
                break
            elif guess == attemptes_allowed:
                print(f"{name} lost the game in {guess} guesses.")
                conn.send(LOST.encode(FORMAT).ljust(HEADER))
                # conn.close()
                break
            elif (msg > escape_key):
                conn.send("The value is too high".encode(FORMAT).ljust(HEADER))
                if msg < upper_bound:
                    upper_bound = msg
            else:
                conn.send("The value is too low".encode(FORMAT).ljust(HEADER))
                if msg > lower_bound:
                    lower_bound = msg

    # if msg == escape_key:
    #     print(f"{name} won the game in {guess} guesses.")
    #     conn.send("You won the game.".encode(FORMAT).ljust(HEADER))
    #     print(f"{name} escaped")
    if(won):
        wonP[guess] = [name, conn]
    players[name] = [guess, conn]
    activeP -= 1
    # active = threading.active_count() - 2
    # conn.join()
    # activeP = threading.active_count() - 1
    print(f"[ACTIVE PLAYERS] = {activeP}")
    if(currentP == totP and activeP == 0):
        end_game()
    
    # if currentP == totP:
    #     if active == 0:
    #         esc = list(players.keys())
    #         esc.sort()
    #         sorted_p = {i: players[i] for i in esc}
    #         print(f"Players escaped in this order {sorted_p}")
    #         print("[ESCAPE COMPLETE] Game ended !!!")
    #         conn.send(END.encode(FORMAT).ljust(HEADER))

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
