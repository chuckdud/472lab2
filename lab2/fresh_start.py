import random

import numpy as np
from copy import copy

NONE, X, O = '.', 'X', 'O'
MT, P1, P2 = 0, 1, 2
POTENTIAL = 3

deepest = 0


def other_player(turn):
    return P2 if turn == P1 else P1


class Action:
    def __init__(self, x, y, flippers):
        self.x = x
        self.y = y
        self.flippers = flippers


class State:
    def __init__(self, board, to_move):
        self.board = board
        self.to_move = to_move

    def __copy__(self):
        return type(self)(copy(self.board), self.to_move)

    # return 0 if not terminal
    # return P1 if P1 wins
    # return P2 if P2 wins
    def terminal_test(self):
        P1_score, P2_score = 0, 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == MT:
                    return 0
                elif self.board[i][j] == P1:
                    P1_score += 1
                elif self.board[i][j] == P2:
                    P2_score += 1
        if P1_score > P2_score:
            return P1
        elif P2_score > P1_score:
            return P2
        else:
            return 0


def init_board():
    board = np.zeros((8, 8))
    board[3][3] = P2
    board[3][4] = P1
    board[4][3] = P1
    board[4][4] = P2
    return board


def alt_init_board():
    # board = np.array([[P2, P1, MT, MT, MT, MT, MT, MT],
    #                   [MT, P2, MT, MT, MT, MT, MT, MT],
    #                   [MT, P1, P2, P1, MT, MT, MT, MT],
    #                   [MT, MT, MT, P2, P1, MT, MT, MT],
    #                   [MT, MT, MT, P1, P2, MT, MT, MT],
    #                   [MT, MT, MT, MT, MT, MT, MT, MT],
    #                   [MT, MT, MT, MT, MT, MT, MT, MT],
    #                   [MT, MT, MT, MT, MT, MT, MT, MT]])
    board = np.array([[MT, MT, MT, MT, MT, MT, MT, MT],
                      [MT, MT, MT, P2, MT, MT, MT, MT],
                      [MT, P1, P2, MT, MT, MT, MT, MT],
                      [MT, MT, MT, MT, MT, MT, MT, MT],
                      [MT, MT, MT, MT, MT, MT, MT, MT],
                      [MT, MT, MT, MT, MT, MT, MT, MT],
                      [MT, MT, MT, MT, MT, MT, MT, MT],
                      [MT, MT, MT, MT, MT, MT, MT, MT]])
    return board


def print_board(board):
    ret = "  0 1 2 3 4 5 6 7\n"
    for i in range(8):
        ret += str(i) + ' '
        for j in range(8):
            if board[i][j] == MT:
                ret += NONE
            elif board[i][j] == P1:
                ret += X
            elif board[i][j] == P2:
                ret += O
            else:
                print("ERROR")
                exit()
            ret += ' '
        ret += "\n"
    print(ret)


def print_with_actions(board, actions):
    to_print = np.copy(board)
    for m in actions:
        to_print[m.y][m.x] = POTENTIAL
    ret = "  0 1 2 3 4 5 6 7 x\n"
    for i in range(8):
        ret += str(i) + ' '
        for j in range(8):
            if to_print[i][j] == MT:
                ret += NONE
            elif to_print[i][j] == P1:
                ret += X
            elif to_print[i][j] == P2:
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


def valid_action(state, x, y):
    flippers = []
    if x < 0 or y < 0 or x > 7 or y > 7:
        return False, flippers
    if state.board[y][x] != MT:
        return False, flippers

    # capture below
    flank = False
    below_flippers = []
    i = y + 1
    while i < 8:
        if state.board[i][x] == MT:
            below_flippers.clear()
            break
        elif state.board[i][x] == other_player(state.to_move):
            below_flippers.append((i, x))
        # found flank
        elif state.board[i][x] == state.to_move:
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
        if state.board[i][x] == MT:
            above_flippers.clear()
            break
        elif state.board[i][x] == other_player(state.to_move):
            above_flippers.append((i, x))
        # found flank
        elif state.board[i][x] == state.to_move:
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
        if state.board[y][j] == MT:
            right_flippers.clear()
            break
        elif state.board[y][j] == other_player(state.to_move):
            right_flippers.append((y, j))
        # found flank
        elif state.board[y][j] == state.to_move:
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
        if state.board[y][j] == MT:
            left_flippers.clear()
            break
        elif state.board[y][j] == other_player(state.to_move):
            left_flippers.append((y, j))
        # found flank
        elif state.board[y][j] == state.to_move:
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
        if state.board[i][j] == MT:
            br_flippers.clear()
            break
        elif state.board[i][j] == other_player(state.to_move):
            br_flippers.append((i, j))
        # found flank
        elif state.board[i][j] == state.to_move:
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
        if state.board[i][j] == MT:
            ar_flippers.clear()
            break
        elif state.board[i][j] == other_player(state.to_move):
            ar_flippers.append((i, j))
        # found flank
        elif state.board[i][j] == state.to_move:
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
        if state.board[i][j] == MT:
            bl_flippers.clear()
            break
        elif state.board[i][j] == other_player(state.to_move):
            bl_flippers.append((i, j))
        # found flank
        elif state.board[i][j] == state.to_move:
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
        if state.board[i][j] == MT:
            al_flippers.clear()
            break
        elif state.board[i][j] == other_player(state.to_move):
            al_flippers.append((i, j))
        # found flank
        elif state.board[i][j] == state.to_move:
            flank = True
            break
        i += 1
        j += 1
    if flank and len(al_flippers) > 0:
        flippers += al_flippers

    # return True, flippers if state.board[x][y] == MT else False, NONE
    return (True, flippers) if len(flippers) > 0 else (False, flippers)


def find_all_actions(state):
    actions = []
    for y in range(8):
        for x in range(8):
            valid, flippers = valid_action(state, x, y)
            if valid:
                actions.append(Action(x, y, flippers))
    return actions


def flip(state, flippers):
    for piece in flippers:
        y = piece[0]
        x = piece[1]
        state.board[y][x] = other_player(state.board[y][x])
    return state


def result(state, action):
    if action is None:
        state.to_move = other_player(state.to_move)
        return state
    state.board[action.y][action.x] = state.to_move
    state = flip(state, action.flippers)
    state.to_move = other_player(state.to_move)
    return state


def random_play(state):
    moves = find_all_actions(state)
    x = random.randint(0, len(moves) - 1)
    return moves[x]


def user_play(state):
    x, y = map(int, input().split())
    valid, flippers = valid_action(state, x, y)
    while not valid:
        x, y = map(int, input().split())
        valid, flippers = valid_action(state, x, y)
    return Action(x, y, flippers)


def computer_play(state):
    action = alpha_beta_search(state)
    return action


# TODO
def alpha_beta_search(state):

    def max_value(state, alpha, beta, depth):
        global deepest
        if depth > deepest:
            deepest = depth
        if state.terminal_test() != 0 or cutoff_test(depth):
            return eval_fn(state)
        v = -np.inf
        for action in find_all_actions(state):
            v = max(v, min_value(result(state, action), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        global deepest
        if depth > deepest:
            deepest = depth
        if state.terminal_test() != 0 or cutoff_test(depth):
            return eval_fn(state)
        v = np.inf
        for action in find_all_actions(state):
            v = min(v, max_value(result(state, action), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def cutoff_test(depth):
        if depth < max_depth:
            return False
        else:
            return True

    best_score = -np.inf
    beta = np.inf
    best_action = None
    actions = find_all_actions(state)
    for a in actions:
        v = min_value(result(copy(state), a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    if best_action is None:
        print("ERROR in alphabeta generating move")
        exit()
    return best_action


# TODO
def eval_fn(state):
    actions = find_all_actions(state)
    alt_state = copy(state)
    alt_state.to_move = other_player(state.to_move)
    alt_actions = find_all_actions(alt_state)
    return len(actions) - len(alt_actions)


def utility(state):
    if state.terminal_test() == state.to_move:
        return 1
    elif state.terminal_test() == other_player(state.to_move):
        return -1
    else:
        return 0


def take_action(state):
    actions = find_all_actions(state)
    if len(actions) == 0:
        return result(state, None)
    print("Player " + str(state.to_move) + " turn:")
    print_with_actions(state.board, actions)

    if state.to_move == P1:
        action = user_play(state)
    else:
        action = computer_play(state)

    return result(state, action)


def play():
    state = State(init_board(), P1)
    winner = 0
    while True:
        state = take_action(state)
        if state.terminal_test() != 0:
            break
    print_board(state.board)
    if winner == P1:
        print("User wins!")
    else:
        print("CPU wins")


max_depth = int(input("Please enter a maximum depth for alpha-beta cutoff search. Enter -1 for maximum depth\n"))
if max_depth < 0:
    max_depth = np.inf
play()
print(deepest)
# test()
