import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8' #string
cIP = socket.gethostbyname(socket.gethostname()) 
# print(socket.gethostbyname(socket.gethostname()))
ADDR = (cIP, PORT)
SUCCESS = "You won the game."
LOST = "You lost the game."
END = "[ESCAPE COMPLETE] Game ended !!!"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' *(HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

guess=0
print(client.recv(HEADER).decode(FORMAT))
client.send(input("My Name-> ").encode(FORMAT))
while True:    
    hint = client.recv(HEADER).decode(FORMAT)
    print(hint)
    if (hint)== SUCCESS or (hint)== LOST:
        break
    guess +=1
    send(input(f"GUESS{guess}-> "))
    print(client.recv(HEADER).decode(FORMAT))
while True:
    end_wait = client.recv(HEADER).decode(FORMAT)
    if end_wait == END:
        print(END)
        client.close()
        break
# print(f"I guessed it right in {guess} guesses.YEEAAHHHHH!!!")