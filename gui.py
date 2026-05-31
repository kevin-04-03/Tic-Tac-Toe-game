import tkinter as tk
from tkinter import messagebox
import time
import threading



def isWinner(bo, le):
    return ((bo[1] == le and bo[2] == le and bo[3] == le) or
            (bo[4] == le and bo[5] == le and bo[6] == le) or
            (bo[7] == le and bo[8] == le and bo[9] == le) or
            (bo[1] == le and bo[4] == le and bo[7] == le) or
            (bo[2] == le and bo[5] == le and bo[8] == le) or
            (bo[3] == le and bo[6] == le and bo[9] == le) or
            (bo[1] == le and bo[5] == le and bo[9] == le) or
            (bo[3] == le and bo[5] == le and bo[7] == le))


def isSpaceFree(board, move):
    return board[move] == ' '


def isBoardFull(board):
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True


def getBoardCopy(board):
    boardCopy = []
    for i in board:
        boardCopy.append(i)
    return boardCopy


def makeMove(board, letter, move):
    board[move] = letter



nodes_explored = 0


def minimax(board, current_player_letter, ai_letter, ai_opponent_letter):
    global nodes_explored
    nodes_explored += 1

    if isWinner(board, ai_opponent_letter):
        return -1
    elif isWinner(board, ai_letter):
        return 1
    elif isBoardFull(board):
        return 0

    if current_player_letter == ai_letter:
        best_score = -float('inf')
        for move in range(1, 10):
            if isSpaceFree(board, move):
                boardCopy = getBoardCopy(board)
                makeMove(boardCopy, current_player_letter, move)
                score = minimax(boardCopy, ai_opponent_letter, ai_letter, ai_opponent_letter)
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for move in range(1, 10):
            if isSpaceFree(board, move):
                boardCopy = getBoardCopy(board)
                makeMove(boardCopy, current_player_letter, move)
                score = minimax(boardCopy, ai_letter, ai_letter, ai_opponent_letter)
                best_score = min(best_score, score)
        return best_score


def getComputerMove(board, computerLetter):
    global nodes_explored
    nodes_explored = 0

    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    best_score = -float('inf')
    best_move = None

    for move in range(1, 10):
        if isSpaceFree(board, move):
            boardCopy = getBoardCopy(board)
            makeMove(boardCopy, computerLetter, move)
            score = minimax(boardCopy, playerLetter, computerLetter, playerLetter)
            if score > best_score:
                best_score = score
                best_move = move
    return best_move



class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minimax Tic-Tac-Toe")
        self.root.geometry("400x600")

        self.board = [' '] * 10
        self.buttons = {}
        self.game_mode = None
        self.player_letter = 'X'
        self.computer_letter = 'O'
        self.turn = 'X'
        self.game_active = False

        self.setup_ui()
        self.show_mode_selection()

    def setup_ui(self):
        self.status_label = tk.Label(self.root, text="Select Mode", font=('Arial', 14), pady=10)
        self.status_label.pack()

        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=10)

        for i in range(1, 10):
            btn = tk.Button(self.board_frame, text="", font=('Arial', 24, 'bold'),
                            width=5, height=2,
                            command=lambda move=i: self.on_button_click(move))
            row = (i - 1) // 3
            col = (i - 1) % 3
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.buttons[i] = btn

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=20)

        self.reset_btn = tk.Button(self.control_frame, text="Reset Game", font=('Arial', 12),
                                   command=self.reset_game, state=tk.DISABLED, width=12)
        self.reset_btn.grid(row=0, column=0, padx=10)

        self.quit_btn = tk.Button(self.control_frame, text="Quit Program", font=('Arial', 12),
                                  command=self.quit_program, bg="#ffcccc", fg="red", width=12)
        self.quit_btn.grid(row=0, column=1, padx=10)

    def show_mode_selection(self):
        selection = tk.Toplevel(self.root)
        selection.title("Choose Mode")
        selection.geometry("300x200")

        tk.Label(selection, text="Select Game Mode:", font=('Arial', 12, 'bold')).pack(pady=10)

        def choose_side():
            selection.destroy()
            self.show_side_selection()

        tk.Button(selection, text="Human vs AI", command=choose_side, width=20, pady=5).pack(pady=5)

        def set_ai_mode():
            self.game_mode = 'AIvAI'
            selection.destroy()
            self.start_game()

        tk.Button(selection, text="AI vs AI Simulation", command=set_ai_mode, width=20, pady=5).pack(pady=5)

        self.root.wait_window(selection)

    def show_side_selection(self):
        side_select = tk.Toplevel(self.root)
        side_select.title("Choose Side")
        side_select.geometry("300x200")

        tk.Label(side_select, text="Do you want to play as X or O?", font=('Arial', 12)).pack(pady=10)
        tk.Label(side_select, text="(X always goes first)", font=('Arial', 10, 'italic')).pack(pady=0)

        def set_side(p_letter):
            self.game_mode = 'HvAI'
            self.player_letter = p_letter
            self.computer_letter = 'O' if p_letter == 'X' else 'X'
            side_select.destroy()
            self.start_game()

        tk.Button(side_select, text="Play as X (Go First)", command=lambda: set_side('X'), width=20, pady=5).pack(
            pady=10)
        tk.Button(side_select, text="Play as O (Go Second)", command=lambda: set_side('O'), width=20, pady=5).pack(
            pady=5)

        self.root.wait_window(side_select)

    def start_game(self):
        self.reset_board_ui()
        self.game_active = True
        self.reset_btn.config(state=tk.NORMAL)
        self.turn = 'X'

        if self.game_mode == 'HvAI':
            if self.player_letter == 'X':
                self.status_label.config(text="Your Turn (X)")
            else:
                self.status_label.config(text="Computer is thinking...")
                self.root.after(500, self.computer_turn_gui)

        elif self.game_mode == 'AIvAI':
            self.status_label.config(text="AI Simulation Running...")
            threading.Thread(target=self.run_ai_vs_ai_step, daemon=True).start()

    def reset_board_ui(self):
        self.board = [' '] * 10
        for i in range(1, 10):
            self.buttons[i].config(text="", state=tk.NORMAL, bg="SystemButtonFace")

    def reset_game(self):
        self.game_active = False
        self.show_mode_selection()

    def quit_program(self):
        self.root.destroy()

    def on_button_click(self, move):
        if not self.game_active or self.game_mode != 'HvAI':
            return

        if self.turn != self.player_letter:
            return

        if isSpaceFree(self.board, move):
            self.make_move_gui(move, self.player_letter)

            if self.check_game_over(self.player_letter):
                return

            self.turn = self.computer_letter
            self.status_label.config(text="Computer is thinking...")

            self.root.after(500, self.computer_turn_gui)

    def computer_turn_gui(self):
        if not self.game_active: return

        move = getComputerMove(self.board, self.computer_letter)
        self.make_move_gui(move, self.computer_letter)

        if not self.check_game_over(self.computer_letter):
            self.turn = self.player_letter
            self.status_label.config(text=f"Your Turn ({self.player_letter})")

    def run_ai_vs_ai_step(self):
        while self.game_active:
            time.sleep(0.5)

            current_player = self.turn
            move = getComputerMove(self.board, current_player)

            if move is None: break

            makeMove(self.board, current_player, move)

            self.root.after(0, lambda m=move, p=current_player:
            self.buttons[m].config(text=p, fg=("blue" if p == 'X' else "red")))

            if isWinner(self.board, current_player):
                self.root.after(0, lambda: self.end_game(f"{current_player} Wins!"))
                return
            elif isBoardFull(self.board):
                self.root.after(0, lambda: self.end_game("It's a Tie!"))
                return

            self.turn = 'O' if self.turn == 'X' else 'X'

    def make_move_gui(self, move, letter):
        makeMove(self.board, letter, move)
        color = "blue" if letter == 'X' else "red"
        self.buttons[move].config(text=letter, fg=color)

    def check_game_over(self, player):
        if isWinner(self.board, player):
            msg = "You Won!" if player == self.player_letter and self.game_mode == 'HvAI' else "Computer Won!"
            self.end_game(msg)
            return True
        elif isBoardFull(self.board):
            self.end_game("It's a Tie!")
            return True
        return False

    def end_game(self, message):
        self.game_active = False
        self.status_label.config(text=message)
        messagebox.showinfo("Game Over", message)
        for i in range(1, 10):
            self.buttons[i].config(state=tk.DISABLED)



if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()

