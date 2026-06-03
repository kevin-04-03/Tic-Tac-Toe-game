Minimax Tic-Tac-Toe
This project contains a Python implementation of Tic-Tac-Toe featuring an unbeatable AI powered by the Minimax algorithm. It includes two separate versions: a fast Command-Line Interface (CLI) for terminal users and a Graphical User Interface (GUI) built with tkinter.

Features
Unbeatable AI: The computer uses the Minimax algorithm to calculate every possible future move, ensuring it will always win or force a tie.

Dual Interfaces:

CLI Version: A lightweight terminal version perfect for running high-speed simulations.

GUI Version: A clean, interactive visual interface built with tkinter.

Multiple Game Modes:

Human vs. AI: Play against the computer as either 'X' or 'O'.

AI vs. AI Simulation: * In CLI: Simulate hundreds of matches instantly to view win/draw statistics, execution time, and total nodes explored.

In GUI: Watch the AI play a visual match against itself in real-time.

Prerequisites
Python 3.x

Tkinter: Included with the standard Python library on most systems. (Note: Linux users may need to install it manually via their package manager, e.g., sudo apt-get install python3-tk).

Getting Started
Save the two code blocks into separate files in your directory. For example:

cli_tictactoe.py (The terminal version)

gui_tictactoe.py (The Tkinter version)

Running the GUI Version
To play the game using the graphical interface, run the following command in your terminal:

Bash
python gui_tictactoe.py
A window will appear asking you to choose your game mode and select your side (X or O).

Running the CLI Version
To play the terminal version or run bulk simulations, run:

Bash
python cli_tictactoe.py
Follow the on-screen prompts to either play a match manually or enter the number of AI vs. AI games you wish to simulate.

How the AI Works (Minimax)
The Minimax algorithm is a recursive function used in decision-making and game theory. When it is the AI's turn, it:

Simulates all available moves on the board.

Plays out every possible subsequent move for both itself and the opponent until the game ends (Win, Lose, or Tie).

Assigns a score to the end state (e.g., +1 for an AI win, -1 for a Player win, 0 for a tie).

Assumes the opponent will always play their absolute best move to minimize the AI's score.

Chooses the path that maximizes its minimum possible score (hence, Mini-max).

Because Tic-Tac-Toe is a solved game, perfect play from both sides will always result in a tie. You will see this proven if you run the AI vs. AI Simulation.
