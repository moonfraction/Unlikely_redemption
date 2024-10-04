# Unlikely Redemption: Number Guessing Game

## Description

Welcome to the Unlikely Redemption Number Guessing Game! In this text-based multiplayer game, players take on the role of prisoners attempting to escape from their virtual prison. The only way to break free is by successfully guessing a escape-key within a limited number of attempts.


## Skills Utilized

- **Socket Programming:** Implemented client-server communication using socket programming to facilitate multiplayer interaction.
- **Multithreading:** Utilized multithreading to handle concurrent connections from multiple prisoners, ensuring a seamless and responsive gaming experience.
- **Programming Language:** Developed the game using Python 3.12.1
- **Algorithm Design:** Implemented efficient algorithms for number generation, player interaction, and game logic.
- **Documentation:** Provided clear and concise documentation for code, making it accessible for contributors and users.


## How to Play

### Server Setup

- The game is hosted on a server, serving as the virtual prison warden.
- The server generates a secret number[escape key] between a predefined range.
- run `python3 server.py`

### Client (Prisoner) Interaction

- Prisoners (clients) connect to the server via the terminal.
- Each prisoner gets up to 5 attempts to guess the secret number and secure their escape.
- run `python3 client.py`

### Winning

- If a prisoner successfully guesses the number within the allowed attempts, they break free from the prison.
- Otherwise, the prisoner is detained in virtual confinement.

## Features

- Multiplayer interaction through client-server architecture.
- Limited attempts create a sense of urgency and strategy for the prisoners.
- Server-side management ensures fair and controlled gameplay.

## How to Run

1. Clone the repository to your local machine.
2. Compile and run the server code.
3. Run multiple instances of the client code for each prisoner to connect. 
4. Follow the prompts in the terminal to make guesses and attempt an escape.

For code explanation and concept clarity, please refer to [Additional Documentation](documentation.md)

## Contribution
Feel free to contribute by submitting bug reports, feature requests, or pull requests.


Enjoy the thrill of escaping the virtual prison through the art of number guessing! May the odds be ever in your favour.
