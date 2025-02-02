"""
Tic Tac Toe Player
"""

import copy
import math
from typing import Optional, Union

X = "X"
O = "O"
EMPTY = None


def initial_state() -> list:
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board: list):
    """
    Returns player who has the next turn on a board.

    In the initial game state, X gets the first move. Subsequently, the player alternates with each additional move.

    Any return value is acceptable if a terminal board is provided as input (i.e., the game is already over).
    """
    actions = 0

    for i in board:
         for j in i:
              if j != EMPTY:
                   actions += 1

    if actions == 0 or actions % 2 == 0:
        return X

    return O


def actions(board: list) -> Optional[set]:
    """
    Returns set of all possible actions (i, j) available on the board.

    Each action should be represented as a tuple (i, j) where i corresponds to the row of the move (0, 1, or 2) and j corresponds to which cell in the row corresponds to the move (also 0, 1, or 2).

    Possible moves are any cells on the board that do not already have an X or an O in them.

    Any return value is acceptable if a terminal board is provided as input.
    """
    actions: set = set()

    # iterate through len and not list
    for i in range(len(board)):
         for j in range(len(board[i])):
             if board[i][j] == EMPTY:
                 actions.add((i, j))

    return actions


def result(board: list, action: tuple) -> list:
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # deep copy of board
    new_board: list = copy.deepcopy(board)

    if action not in actions(board):
        raise Exception("Invalid action")

    play = player(board)

    new_board[action[0]][action[1]] = play

    return new_board


def winner(board: list) -> Union[str | int | None]:
    """
    Returns the winner of the game, if there is one.

    If the X player has won the game, your function should return X. If the O player has won the game, your function should return O
    """
    # controlla se ci sono righe vincitrici
    for i in board:
        if i[0] != EMPTY and all(element == i[0] for element in i):
            return i[0]

    # controlla se colonne vincitrici
    for i in board:
        for j in range(len(board[0])):
            if board[0][j] != EMPTY and all(board[i][j] == board[0][j] for i in range(len(board))):
                return board[0][j]

    # controlla le due diagonali
    if board[0][0] != EMPTY and all(board[0][0] == board[n][n] for n in range(len(board))):
        return board[0][0]

    if board[0][len(board)-1] != EMPTY and all(board[0][len(board)-1] == board[n][len(board)-1-n] for n in range(len(board))):
        return board[0][len(board)-1]

    return None

def terminal(board: list) -> bool:
    """
    Returns True if game is over, False otherwise.
    """
    # controlla se ci sono righe vincitrici
    if winner(board) != None:
        return True

    # controlla se non ci sono più empty
    for i in board:
        for j in i:
            if j == EMPTY:
                return False

    # if not empty return True
    return True


def utility(board: list) -> int:
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    won = winner(board)
    if won == X:
        return 1
    elif won == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    The move returned should be the optimal action (i, j) that is one of the allowable actions on the board.

    If the board is a terminal board, the minimax function should return None

    Implement with alpha-beta pruning
    """
    # prendi primo valore della tupla
    move, state = best_move(board)

    if state == None:
        return None

    # debug statement
    print(f"Mossa: {move}")

    return move


def best_move(board: list):
    """
    Effettiva minimax function

    Tutti i print statement sono per il debug, non sono necessari per il codice finale

    Recursion con best_move o minimax?

    Errore: la funzione continua a fare la recursion anche dopo il base case
    TypeError: 'int' object is not iterable
    """
    best_action = tuple()

    # base case
    if terminal(board):
        print("Il board è terminale")
        print(f"Utility: {utility(board)}")
        # utility(board) è un int, l'errore nel docstring è riferito a questa parte
        return best_action, None

    # controllo del player
    play = player(board)
    print(play)
    alpha = -math.inf
    beta = math.inf

    # max player
    if play == X:
        # set min value
        v = -1
        # check di tutte le azioni
        for action in actions(board):
            if terminal(board):
                print("Il board è terminale")
                print(f"Utility: {utility(board)}")
        # utility(board) è un int, l'errore nel docstring è riferito a questa parte
                return best_action, None
            print(f"Azione: {action}")
            print(f"Risultato: {result(board, action)}")
            # scegliamo l'azione max
            value = max(v, best_move(result(board, action))[1])
            # aggiornamento variabili
            if value >= v:
                v = value
                best_action = action

            # aggiornamento alpha
            alpha = max(alpha, v)

            # pruning del branch
            if v >= beta:
                break

    # min player
    if play == O:
        # set max value
        v = 1
        # check di tutte le azioni
        for action in actions(board):
            if terminal(board):
                print("Il board è terminale")
                print(f"Utility: {utility(board)}")
                return best_action, None
            print(f"Azione: {action}")
            print(f"Risultato: {result(board, action)}")
            # scegliamo l'azione max
            value = min(best_move(result(board, action))[1])
            # aggiornamento variabili
            if value <= v:
                v = value
                best_action = action

            # aggiornamento beta
            beta = min(beta, v)

            # pruning del branch
            if v <= alpha:
                break

    # ritorno del recursion (ancora in corso, no base case)
    return best_action, v
