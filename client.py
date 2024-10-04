import socket

# Constants for the socket connection
HEADER = 64                                         # Number of bytes for the header, specifying the message length
PORT = 5050                                         # Port to connect to the server
FORMAT = 'utf-8'                                    # Encoding format for messages
cIP = socket.gethostbyname(socket.gethostname())    # Get the local machine's IP address
ADDR = (cIP, PORT)                                  # Tuple containing IP address and port


SUCCESS = "You won the game."
LOST = "You lost the game."
END = "Game ended !!!"

# Create a socket object and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# Function to send messages to the server
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

guess = 0
print(client.recv(HEADER).decode(FORMAT))  # Receive and print the initial message from the server
client.send(input("My Name-> ").encode(FORMAT))  # Send the player's name to the server

# Loop to receive hints and send guesses to the server
while True:    
    hint = client.recv(HEADER).decode(FORMAT)
    print(hint.strip())
    
    guess += 1
    send(input(f"GUESS{guess}-> "))
    result = client.recv(HEADER).decode(FORMAT).strip()
    print(result)

    # Check if the game is over (won or lost)
    if result == SUCCESS or result == LOST:
        break

# Loop to wait for the end signal from the server
while True:
    end_wait = client.recv(HEADER).decode(FORMAT).strip()
    
    # Check if the game has officially ended
    if end_wait == END:
        print(END)
        client.close()  # Close the client socket
        break
