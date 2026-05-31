import random
import time



def drawBoard(board):
    print(board[1] + '|' + board[2] + '|' + board[3])
    print('-+-+-')
    print(board[4] + '|' + board[5] + '|' + board[6])
    print('-+-+-')
    print(board[7] + '|' + board[8] + '|' + board[9])


def inputPlayerLetter():
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        print('Do you want to be X or O?')
        letter = input().upper()

    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def makeMove(board, letter, move):
    board[move] = letter


def isWinner(bo, le):
    return ((bo[1] == le and bo[2] == le and bo[3] == le) or
            (bo[4] == le and bo[5] == le and bo[6] == le) or
            (bo[7] == le and bo[8] == le and bo[9] == le) or
            (bo[1] == le and bo[4] == le and bo[7] == le) or
            (bo[2] == le and bo[5] == le and bo[8] == le) or
            (bo[3] == le and bo[6] == le and bo[9] == le) or
            (bo[1] == le and bo[5] == le and bo[9] == le) or
            (bo[3] == le and bo[5] == le and bo[7] == le))


def getBoardCopy(board):
    boardCopy = []
    for i in board:
        boardCopy.append(i)
    return boardCopy


def isSpaceFree(board, move):
    return board[move] == ' '


def getPlayerMove(board):
    while True:
        print('What is your next move? (1-9)')
        move = input()

        try:
            move_int = int(move)
            if move_int < 1 or move_int > 9:
                print('Invalid input. Please enter a number from 1 to 9.')
                continue

        except ValueError:
            print('Invalid input. Please enter a number from 1 to 9.')
            continue

        if not isSpaceFree(board, move_int):
            print('Invalid move. That space is already taken. Please make a new move.')
            continue

        return move_int


def isBoardFull(board):
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True



nodes_explored = 0


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



def playHumanVsAI():
    print('Welcome to Tic-Tac-Toe!')
    while True:
        theBoard = [' '] * 10
        playerLetter, computerLetter = inputPlayerLetter()

        if playerLetter == 'X':
            turn = 'player'
        else:
            turn = 'computer'

        print('The ' + turn + ' (X) will go first.')
        gameIsPlaying = True

        while gameIsPlaying:
            if turn == 'player':
                drawBoard(theBoard)
                move = getPlayerMove(theBoard)
                makeMove(theBoard, playerLetter, move)

                if isWinner(theBoard, playerLetter):
                    drawBoard(theBoard)
                    print('Hooray! You have won the game!')
                    gameIsPlaying = False
                else:
                    if isBoardFull(theBoard):
                        drawBoard(theBoard)
                        print('The game is a tie!')
                        break
                    else:
                        turn = 'computer'

            else:
                print("Computer is thinking...")
                start_time = time.time()
                move = getComputerMove(theBoard, computerLetter)
                end_time = time.time()

                print(f"Computer explored {nodes_explored} nodes in {end_time - start_time:.4f} seconds.")
                makeMove(theBoard, computerLetter, move)

                if isWinner(theBoard, computerLetter):
                    drawBoard(theBoard)
                    print('The computer has beaten you! You lose.')
                    gameIsPlaying = False
                else:
                    if isBoardFull(theBoard):
                        drawBoard(theBoard)
                        print('The game is a tie!')
                        break
                    else:
                        turn = 'player'

        print('Do you want to play again? (yes or no)')
        if not input().lower().startswith('y'):
            break


def runAIGames(num_games):
    print(f"Starting {num_games} AI-vs-AI games...")
    start_time = time.time()
    stats = {'X': 0, 'O': 0, 'Draw': 0}
    total_simulation_nodes = 0
    if num_games < 10:
        print_interval = 1
    else:
        print_interval = num_games // 10
    for i in range(num_games):
        theBoard = [' '] * 10
        turn = 'X'
        while True:
            if turn == 'X':
                move = getComputerMove(theBoard, 'X')
                total_simulation_nodes += nodes_explored
                makeMove(theBoard, 'X', move)
                if isWinner(theBoard, 'X'):
                    stats['X'] += 1
                    break
                turn = 'O'
            else:
                move = getComputerMove(theBoard, 'O')
                total_simulation_nodes += nodes_explored
                makeMove(theBoard, 'O', move)
                if isWinner(theBoard, 'O'):
                    stats['O'] += 1
                    break
                turn = 'X'
            if isBoardFull(theBoard):
                stats['Draw'] += 1
                break
        if (i + 1) % print_interval == 0:
            print(f"  ...Game {i + 1}/{num_games} completed.")
    end_time = time.time()
    total_time = end_time - start_time
    print("\n--- Simulation Complete ---")
    print(f"Total Games: {num_games}")
    print(f"AI 'X' Wins: {stats['X']}")
    print(f"AI 'O' Wins: {stats['O']}")
    print(f"Draws:       {stats['Draw']}")
    print(f"Total Nodes Explored: {total_simulation_nodes:,}")
    print(f"Total time taken: {total_time:.4f} seconds")




if __name__ == "__main__":
    print("Select Mode:")
    print("1: Play against the Minimax AI")
    print("2: Run AI-vs-AI simulation")

    choice = ''
    while choice not in ['1', '2']:
        choice = input("Enter 1 or 2: ")

    if choice == '1':
        playHumanVsAI()
    else:
        try:
            num = int(input("Enter number of games to simulate (e.g., 100): "))
            if num > 0:
                runAIGames(num)
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input.")

