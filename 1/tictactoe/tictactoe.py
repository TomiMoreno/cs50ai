"""
Tic Tac Toe Player
"""

import math, copy
from random import random

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xCount = 0
    oCount = 0
    for row in board:
        for cell in row: 
            if cell == X:
                xCount += 1
            if cell == O:
                oCount += 1

    if xCount > oCount: return O
    return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleActions = []
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if(board[i][j] == EMPTY):
                possibleActions.append((i,j))
    return possibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    currentPlayer = player(board)
    newBoard = copy.deepcopy(board)
    newBoard[action[0]][action[1]] = currentPlayer
    return newBoard
    


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(0, len(board)):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) != None or len(actions(board)) == 0


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    return 0

def maxValue(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, minValue(result(board, action)))
    return v

def minValue(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, maxValue(result(board, action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    bestAction = None
    v = -math.inf if player(board) == X else math.inf
    for action in actions(board):
        if player(board) == X:
            currentValue = minValue(result(board, action))
            if currentValue == 1:
                return action
            elif(currentValue > v):
                v = currentValue
                bestAction = action
        else:
            currentValue = maxValue(result(board, action))
            if currentValue == -1:
                return action
            elif(currentValue < v):
                v = currentValue
                bestAction = action
        if(currentValue == v and random() > 0.5):
            bestAction = action
    return bestAction
