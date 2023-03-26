import random

import numpy as np

# 0 is empty
# 1 is player 1
# 2 is player 2
NONE, X, O = '.', 'X', 'O'
EMP, MAX, MIN = 0, 1, 2
POTENTIAL = 3


def other_player(turn):
    return MIN if turn == MAX else MAX


class Move:
    def __init__(self, x, y, flippers, who):
        self.x = x
        self.y = y
        self.flippers = flippers
        self.who = who


def print_board(board):
    ret = "  0 1 2 3 4 5 6 7\n"
    for i in range(8):
        ret += str(i) + ' '
        for j in range(8):
            if board[i][j] == EMP:
                ret += NONE
            elif board[i][j] == MAX:
                ret += X
            elif board[i][j] == MIN:
                ret += O
            else:
                print("ERROR")
                exit()
            ret += ' '
        ret += "\n"
    print(ret)


def print_with_moves(board, moves):
    to_print = np.copy(board)
    for m in moves:
        to_print[m.y][m.x] = POTENTIAL
    ret = "  0 1 2 3 4 5 6 7 x\n"
    for i in range(8):
        ret += str(i) + ' '
        for j in range(8):
            if to_print[i][j] == EMP:
                ret += NONE
            elif to_print[i][j] == MAX:
                ret += X
            elif to_print[i][j] == MIN:
                ret += O
            elif to_print[i][j] == POTENTIAL:
                ret += '?'
            else:
                print("ERROR")
                exit()
            ret += ' '
        ret += "\n"
    ret += 'y'
    print(ret)
    # print("Enter x and y coordinate separated by a space")


# valid moves are any moves which allow player to flip an opponent's piece
# check vertically, horizontallly, and diagonally to see if a piece can be captured
def valid_move(board, x, y, turn):
    flippers = []
    if x < 0 or y < 0 or x > 7 or y > 7:
        return False, flippers
    if board[y][x] != EMP:
        return False, flippers

    # capture below
    flank = False
    below_flippers = []
    i = y + 1
    while i < 8:
        if board[i][x] == EMP:
            below_flippers.clear()
            break
        elif board[i][x] == other_player(turn):
            below_flippers.append((i, x))
        # found flank
        elif board[i][x] == turn:
            flank = True
            break

        i += 1
    if flank and len(below_flippers) > 0:
        flippers += below_flippers

    # capture above
    above_flippers = []
    flank = False
    i = y - 1
    while i >= 0:
        if board[i][x] == EMP:
            above_flippers.clear()
            break
        elif board[i][x] == other_player(turn):
            above_flippers.append((i, x))
        # found flank
        elif board[i][x] == turn:
            flank = True
            break
        i -= 1
    if flank and len(above_flippers) > 0:
        flippers += above_flippers

    # capture right
    right_flippers = []
    flank = False
    j = x + 1
    while j < 8:
        if board[y][j] == EMP:
            right_flippers.clear()
            break
        elif board[y][j] == other_player(turn):
            right_flippers.append((y, j))
        # found flank
        elif board[y][j] == turn:
            flank = True
            break
        j += 1
    if flank and len(right_flippers) > 0:
        flippers += right_flippers

    # capture left
    left_flippers = []
    flank = False
    j = x - 1
    while j >= 0:
        if board[y][j] == EMP:
            left_flippers.clear()
            break
        elif board[y][j] == other_player(turn):
            left_flippers.append((y, j))
        # found flank
        elif board[y][j] == turn:
            flank = True
            break
        j -= 1
    if flank and len(left_flippers) > 0:
        flippers += left_flippers

    # below right
    br_flippers = []
    flank = False
    i = y - 1
    j = x - 1
    while i >= 0 and j >= 0:
        if board[i][j] == EMP:
            br_flippers.clear()
            break
        elif board[i][j] == other_player(turn):
            br_flippers.append((i, j))
        # found flank
        elif board[i][j] == turn:
            flank = True
            break
        i -= 1
        j -= 1
    if flank and len(br_flippers) > 0:
        flippers += br_flippers

    # above right
    ar_flippers = []
    flank = False
    i = y + 1
    j = x - 1
    while i < 8 and j >= 0:
        if board[i][j] == EMP:
            ar_flippers.clear()
            break
        elif board[i][j] == other_player(turn):
            ar_flippers.append((i, j))
        # found flank
        elif board[i][j] == turn:
            flank = True
            break
        i += 1
        j -= 1
    if flank and len(ar_flippers) > 0:
        flippers += ar_flippers

    # below left
    bl_flippers = []
    flank = False
    i = y - 1
    j = x + 1
    while i >= 0 and j < 8:
        if board[i][j] == EMP:
            bl_flippers.clear()
            break
        elif board[i][j] == other_player(turn):
            bl_flippers.append((i, j))
        # found flank
        elif board[i][j] == turn:
            flank = True
            break
        i -= 1
        j += 1
    if flank and len(bl_flippers) > 0:
        flippers += bl_flippers

    # above left
    al_flippers = []
    flank = False
    i = y + 1
    j = x + 1
    while i < 8 and j < 8:
        if board[i][j] == EMP:
            al_flippers.clear()
            break
        elif board[i][j] == other_player(turn):
            al_flippers.append((i, j))
        # found flank
        elif board[i][j] == turn:
            flank = True
            break
        i += 1
        j += 1
    if flank and len(al_flippers) > 0:
        flippers += al_flippers

    # return True, flippers if board[x][y] == EMP else False, NONE
    return (True, flippers) if len(flippers) > 0 else (False, flippers)


# find all legal moves that player <turn> can make given the current board
# return an array of Move objects representing each legal move
def find_all_moves(board, turn):
    moves = []
    for y in range(8):
        for x in range(8):
            valid, flippers = valid_move(board, x, y, turn)
            if valid:
                moves.append(Move(x, y, flippers, turn))
    return moves


def init_board():
    board = np.zeros((8, 8))
    board[3][3] = MIN
    board[3][4] = MAX
    board[4][3] = MAX
    board[4][4] = MIN
    return board


def alt_init_board():
    # board = np.array([[MIN, MAX, EMP, EMP, EMP, EMP, EMP, EMP],
    #                   [EMP, MIN, EMP, EMP, EMP, EMP, EMP, EMP],
    #                   [EMP, MAX, MIN, MAX, EMP, EMP, EMP, EMP],
    #                   [EMP, EMP, EMP, MIN, MAX, EMP, EMP, EMP],
    #                   [EMP, EMP, EMP, MAX, MIN, EMP, EMP, EMP],
    #                   [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
    #                   [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
    #                   [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP]])
    board = np.array([[EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
                      [EMP, EMP, EMP, MIN, EMP, EMP, EMP, EMP],
                      [EMP, MAX, MIN, EMP, EMP, EMP, EMP, EMP],
                      [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
                      [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
                      [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
                      [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
                      [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP]])
    return board


def apply_move(board, mv):
    flip(board, mv.flippers)
    board[mv.y][mv.x] = mv.who
    return board


def max_move(board):
    if len(find_all_moves(board, MAX)) == 0:
        print("P2 wins!")
        exit()
    x, y = map(int, input().split())
    valid, flippers = valid_move(board, x, y, MAX)
    while not valid:
        x, y = map(int, input().split())
        valid, flippers = valid_move(board, x, y, MAX)
    mv = Move(x, y, flippers, MAX)
    return apply_move(board, mv)


# TODO replace with alphabeta pruning
def min_move(board):
    if len(find_all_moves(board, MAX)) == 0:
        print("P1 wins!")
        exit()
    x, y = map(int, input().split())
    valid, flippers = valid_move(board, x, y, MIN)
    while not valid:
        x, y = map(int, input().split())
        valid, flippers = valid_move(board, x, y, MIN)
    mv = Move(x, y, flippers, MIN)
    return apply_move(board, mv)


def flip(board, flippers):
    for piece in flippers:
        y = piece[0]
        x = piece[1]
        board[y][x] = other_player(board[y][x])


def move(board, turn):
    moves = find_all_moves(board, turn)
    if turn == MAX:
        print("MAX turn:")
    else:
        print("MIN turn:")
    print_with_moves(board, moves)
    if turn == MAX:
        return max_move(board)
    else:
        return min_move(board)


def play():
    board = init_board()
    # board = alt_init_board()
    turn = MAX
    while True:
        board = move(board, turn)
        if turn == MAX:
            turn = MIN
        else:
            turn = MAX


def test():
    board = alt_init_board()
    print_with_moves(board, find_all_moves(board, MIN))
    # board = move(board, MIN)


play()
# test()
