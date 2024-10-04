# How the Code Works

The project consists of a server and multiple client instances that simulate a number guessing game. Below is a detailed explanation of how the code operates:

## Client-Side
```
import socket
```

The socket module is crucial for creating and managing network connections between different devices over __protocols__ like TCP and UDP.
> Why import `socket` ?
> 1. The `socket` module is the gateway to network programming in Python.
> 2. Supports Key Protocols like TCP and UDP.
> 3. The socket module is cross-platform.

### What Are Protocols?
Protocols are sets of rules and standards that define how data is transmitted and received over a network. 

In `server.py` and `client.py` scripts, **TCP** (Transmission Control Protocol) is being used to establish communication between the client and the server.

#### TCP (Transmission Control Protocol)
**TCP** is one of the core protocols of the Internet Protocol (IP) suite, commonly known as **TCP/IP**.
* TCP establishes a connection between the client and the server before transmitting data, which involves a **three-way handshake** (SYN, SYN-ACK, ACK)
* It is used for **reliable**, **ordered**, and **error-checked** delivery of data between applications running on hosts in a network.

```
# Constants for the socket connection
HEADER = 64                                         # Number of bytes for the header, specifying the message length
PORT = 5050                                         # Port to connect to the server
FORMAT = 'utf-8'                                    # Encoding format for messages
cIP = socket.gethostbyname(socket.gethostname())    # Get the local machine's IP address
ADDR = (cIP, PORT)                                  # Tuple containing IP address and port
```

####  Why call `gethostbyname` on `gethostname`?

This is a common way to find the IP address of the local machine when the program runs. The reason it's necessary is that `socket.gethostname()` returns a human-readable hostname, but the program needs an IP address to establish a network connection. By calling `socket.gethostbyname()` on that hostname, the IP address is resolved.

```
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```
This line creates a new **socket** object, which is essentially an endpoint for sending and receiving data over a network.
* `socket.AF_INET` refers to the **address family** :
    * `AF_INET` stands for **Address Family - Internet**, which means the socket is using the IPv4 protocol.
* `socket.SOCK_STREAM` refers to the **socket type** : 
    * `SOCK_STREAM` is used for **TCP** connections, which provide a reliable, ordered, and error-checked stream of data.

```
client.connect(ADDR)
```
This line connects the client socket to a server.

#### What Happens During `connect`:
1. Create a Connection Request:
    * The `client.connect(ADDR)` method sends a connection request to the server located at the specified IP address and port.
2. Handshake:
    * TCP performs a **three-way handshake** to establish a reliable connection:
        1. The client sends a **SYN** (synchronize) packet to the server.
        2. The server replies with a **SYN-ACK** (synchronize-acknowledge).
        3. The client responds with an **ACK** (acknowledge), and the connection is established.
3. Connection Established:
    * Once the handshake is complete, a reliable connection is formed between the client and the server, allowing data to be sent back and forth in an orderly manner.

```
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
```
The function first sends the length of the message, followed by the message itself, allowing the server to know how many bytes to expect for the incoming message.


#### Game Loop:

* The client receives an initial message from the server to enter their name.
* The player sends their name to the server.
* The game loop receives hints from the server (e.g., if the guess is too high or low) and sends guesses back until the player either wins or loses.
* The loop waits for the server to send a final "end game" message, after which the client socket is closed.


## Server-Side
```
import threading 
```
Threading in programming allows multiple threads to execute concurrently, enabling tasks to run in parallel.
* A thread is a separate flow of execution within a program. Each thread can run independently while sharing the same memory space with other threads of the same process.
* Concurrency vs. Parallelism:
    * **Concurrency**: Multiple threads make progress within overlapping time periods, which may involve switching execution context between threads.
    * **Parallelism**: Multiple threads run simultaneously on different processors or cores.


Server generates two random numbers such that the range is >10000 and <100000, that will be the lower and upper bounds of the escape key

Server randomly generates an escape key in that range.

```
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```
This line creates another **socket** object, which is essentially an endpoint for sending and receiving data over a network.

#### Differences Between Server and Client Sockets
*  The server socket listens for connections and accepts them, while the client socket initiates a connection to the server.
* The server socket binds and listens first, while the client socket connects to the server after it's ready.

```
server.bind(ADDR)
```
Binding a socket informs the OS that the server wants to listen on the given address. This step essentially "claims" the specified port so that any incoming traffic directed to that IP/port is routed to this server.

> * In a client-server architecture using sockets, the server IP (server IP) and the client IP (cIP) can be different.
> * The port number used by the server must be the same as the one the client is trying to connect to.


#### Main Game Logic:
* The server listens for incoming player connections using `server.listen()`
* The `handle_client()` function manages the connection with each player. It:
    * Welcomes the player and requests their name.
    * Runs a loop where it accepts guesses from the player and provides hints (too high, too low).
    * If the player guesses the correct number (referred to as the "escape key"), they win. After 5 incorrect guesses, the player loses.
    
#### Threading for Multiple Players: 
The server uses threads to handle multiple players concurrently. Each connection is managed in a separate thread, allowing simultaneous gameplay for multiple clients.

### What are Threads?
* Threads are the smallest unit of execution in a program, allowing multiple tasks to be performed concurrently within the same process.
* A thread represents a separate flow of control that can run independently, but shares the same resources, such as memory, with other threads in the same process.

#### States of a Thread:
* New
* Runnable (Active)
* Blocked/Waiting
* Terminated

#### Active Threads
An active thread is a thread that is in a runnable state, meaning it is either currently executing or is ready to execute its task as soon as it gets CPU time.

>A thread becomes active when:
> * It is created and the `start()` method is called.

#### Connection from a client
When the server is set up using `socket.bind()` and `socket.listen()`, it begins listening for incoming connection requests.
```
conn, addr = server.accept()
```
* The `server.accept()` method in socket programming is used to accept a connection from a client. 
* It is a blocking call, meaning the server will pause execution at this line until a client attempts to connect. 
* Once a connection is established, it returns two values:
    * `conn` (Connection Object):
        * This is a new **socket** object that is used to communicate with the client.
        * Through this `conn` object, you can send and receive data to and from the connected client.
        
    * `addr` (Address):
        * This is a tuple containing the **IP address** and **port number** of the client that has connected to the server.
        * You can use this to identify the client.

#### Creating a new thread
```
thread = threading.Thread(target=handle_client, args=(conn, addr))
thread.start()
```
* The `threading.Thread()` constructor takes a target function, which specifies what the thread will execute, and args, which are the arguments to pass to that function.
* The target parameter in the `threading.Thread()` constructor is designed to point to a **single** callable (function or method) that the thread will execute.
* The `start()` method is called to begin the execution of the thread.


#### Why is Multithreading Used Here?
* **Concurrency**: Without threading, the server would have to handle each client sequentially, meaning it could only serve one client at a time. While waiting for one client to finish, no other clients could connect.

* **Handling Multiple Clients**: By using multithreading, each client connection is handled in its own thread. This allows the server to accept new connections and interact with multiple clients simultaneously.

#### Game Conclusion:

When all players have entered, and all active threads (players) have finished, the server prints the order in which players escaped and sends a final message indicating the end of the game.