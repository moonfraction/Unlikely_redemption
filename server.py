import socket
import threading 
import random 

l = random.randint(1, 10000)
while True:
    r = random.randint(20000, 110000)
    if (r-l)>10000 and (r-l)<100000:
        break
x= random.randint(l, r)
print(f"Escape-key = {x}  (won't be visible to client)")

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) 
print(socket.gethostbyname(socket.gethostname()))
# SERVER = "192.168.1.13"  IPv4 address
ADDR = (SERVER, PORT)
FORMAT = 'utf-8' #string
SUCCESS = "You won the game."
LOST = "You lost the game."
END = "[ESCAPE COMPLETE] Game ended !!!"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW Player] {addr} connected.")
    conn.send("Enter your name: ".encode(FORMAT))
    name = str(conn.recv(HEADER).decode(FORMAT))
    print(f"{addr} is named {name}")
    R= r
    L= l    
    guess =0
    while True:
        conn.send(f"Guess 'escape-key' between {L} and {R}".encode(FORMAT))
        # conn.send("Type your guess: ".encode(FORMAT))#client terminal will not show this message
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            msg = int(msg)
            
            #if client takes more than 5 guesses, he/she will loose the game
            guess += 1
            if guess ==5:
                print(f"{name} lost the game in {guess} guesses.")
                conn.send("You lost the game.".encode(FORMAT))
                conn.close()
                break
            
            print(f"[{name}] guessed {msg}")
            if msg == x:
                conn.send(f"You guessed it right in {guess} guesses.".encode(FORMAT))
                break
            elif (msg >x):
                conn.send("The value is too high".encode(FORMAT))
                if msg< R :
                    R = msg
            else:
                conn.send("The value is too low".encode(FORMAT))
                if msg >L:
                    L = msg
    if msg == x:
        print(f"{name} won the game in {guess} guesses.")
        conn.send("You won the game.".encode(FORMAT))
        print(f"{name} escaped")
    players[guess] = name
    active = threading.active_count()-2
    print(f"[ACTIVE Players] = {active}")
    
    if totP ==2 :
        if active == 0:
            esc = list(players.keys())
            esc.sort()
            sorted_p ={i: players[i] for i in esc}
            print(f"Players escaped in this order {sorted_p}")
            print("[ESCAPE COMPLETE] Game ended !!!")
            conn.send(END.encode(FORMAT))
    conn.close()


def start():
    global totP
    server.listen()
    print(f"[JOINING] Game is accepting players on {SERVER}")
    while True:
        if totP ==2:
            break
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        totP +=1
        print(f"[ACTIVE PLAYERS] = {threading.active_count()-1}") 
        print(f"Total players entered the game = {totP}")


print("[STARTING] Game is starting...")
players = {}
totP = 0
start()