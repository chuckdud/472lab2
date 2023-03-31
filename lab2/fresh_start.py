import random
import numpy as np
from copy import copy

NONE, X, O = '.', 'X', 'O'
MT, P1, P2 = 0, 1, 2
POTENTIAL = 3

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

    # return:
    #   -1 if not terminal
    #   0 if terminal and tie
    #   P1 if terminal and P1 wins
    #   P2 if terminal and P2 wins
    def terminal_test(self):
        if len(find_all_actions(self)) != 0 or len(find_all_actions(result(self.__copy__(), None))) != 0:
            return -1
        score = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == P1:
                    score += 1
                elif self.board[i][j] == P2:
                    score -= 1
        if score > 0:
            return P1
        elif score < 0:
            return P2
        else:
            return 0


# board initialization
def init_board():
    board = np.zeros((8, 8))
    board[3][3] = P2
    board[3][4] = P1
    board[4][3] = P1
    board[4][4] = P2
    return board


# alternate board initialization for testing
def alt_init_board():
    # board = np.array([[P2, P2, P2, P2, P2, P2, P2, MT],
    #                   [P2, P2, P2, P2, P2, P2, P2, P2],
    #                   [P2, P2, P2, P2, P2, P2, P2, P2],
    #                   [P2, P2, P2, P2, P2, P2, MT, MT],
    #                   [P2, P2, P2, P2, P2, P2, P1, P1],
    #                   [P2, MT, MT, P2, MT, P2, MT, MT],
    #                   [P2, MT, P2, MT, P1, MT, P2, MT],
    #                   [MT, MT, MT, MT, MT, MT, MT, MT]])
    board = np.array([[P2, P2, P2, P2, P2, P2, P2, P2],
                      [P2, P2, P2, P2, P2, P2, P2, P2],
                      [P2, P1, P2, P2, P2, P2, P2, P2],
                      [P2, P2, P1, P2, P2, P2, P2, P2],
                      [P2, P2, P1, P1, P2, P2, P2, P2],
                      [P2, P2, P1, P2, P2, P2, P2, MT],
                      [P2, P1, P1, P1, P1, P1, P1, MT],
                      [P1, P1, P1, P2, P2, P2, MT, MT]])
    return board


# print game board
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


# print game board with '?' in spaces where a player can make a move
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


# check if placing a stone at (x, y) is a valid move according to rules of othello
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


# find all valid actions given a current state
def find_all_actions(state):
    actions = []
    for y in range(8):
        for x in range(8):
            valid, flippers = valid_action(state, x, y)
            if valid:
                actions.append(Action(x, y, flippers))
    return actions


# flip all captured pieces when applying an action
def flip(state, flippers):
    for piece in flippers:
        y = piece[0]
        x = piece[1]
        state.board[y][x] = other_player(state.board[y][x])
    return state


# apply an action to current state
# if the action is None forfeit turn to other player
def result(state, action):
    ret = state.__copy__()
    if action is None:
        ret.to_move = other_player(ret.to_move)
        return ret
    ret.board[action.y][action.x] = ret.to_move
    ret = flip(ret, action.flippers)
    ret.to_move = other_player(ret.to_move)
    return ret


# select a random valid action
def random_play(state):
    actions = find_all_actions(state)
    x = random.randint(0, len(actions) - 1)
    return actions[x]


# allow user to enter an action
def user_play(state):
    print("Enter an x and y coordinate separated by a space:")
    x, y = map(int, input().split())
    valid, flippers = valid_action(state, x, y)
    while not valid:
        print("Invalid move. Try again:")
        x, y = map(int, input().split())
        valid, flippers = valid_action(state, x, y)
    return Action(x, y, flippers)


# CPU play using alpha-beta-cutoff search
def computer_play(state):
    if len(find_all_actions(state)) == 1:
        return find_all_actions(state)[0]
    action = alpha_beta_search(state)
    return action


# alpha-beta-cutoff search
def alpha_beta_search(state):

    def max_value(state, alpha, beta, depth):
        if cutoff_test(depth):
            return eval_fn_2(state)
        elif state.terminal_test() >= 0:
            return utility(state)
        elif len(find_all_actions(state)) == 0:
            return 0
        v = -np.inf
        for action in find_all_actions(state):
            v = max(v, min_value(result(state, action), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(depth):
            return eval_fn_2(state)
        elif state.terminal_test() >= 0:
            return utility(state)
        elif len(find_all_actions(state)) == 0:
            return 0
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

    def eval_fn_1(state):
        score = 0
        for row in state.board:
            for x in row:
                if x == P1:
                    score -= 1
                if x == P2:
                    score += 1
        return score

    def eval_fn_2(state):
        score = 0
        if state.board[0][0] == P2:
            score += 5
        elif state.board[0][0] == P1:
            score -= 5
        if state.board[0][7] == P2:
            score += 5
        elif state.board[0][7] == P1:
            score -= 5
        if state.board[7][0] == P2:
            score += 5
        elif state.board[7][0] == P1:
            score -= 5
        if state.board[7][7] == P2:
            score += 5
        elif state.board[7][7] == P1:
            score -= 5

        for x in state.board[0][:]:
            if x == P2:
                score += 1
            elif x == P1:
                score -= 1
        for x in state.board[7][:]:
            if x == P2:
                score += 1
            elif x == P1:
                score -= 1
        for x in state.board[:][0]:
            if x == P2:
                score += 1
            elif x == P1:
                score -= 1
        for x in state.board[:][7]:
            if x == P2:
                score += 1
            elif x == P1:
                score -= 1

        return score

    def utility(state):
        if state.terminal_test() == P2:
            return 1
        elif state.terminal_test() == P1:
            return -1
        else:
            return 0

    best_score = -np.inf
    beta = np.inf
    best_action = None
    actions = find_all_actions(state)
    for a in actions:
        v = min_value(result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    if best_action is None:
        print("ERROR in alphabeta generating move")
        exit()
    return best_action


def take_action(state):
    actions = find_all_actions(state)
    if len(actions) == 0:
        if state.to_move == P1:
            print("User cannot play.")
        else:
            print("CPU cannot play.")
        return result(state, None)
    if state.to_move == P1:
        print("USER TURN")
        # action = user_play(state)
        action = random_play(state)
        print("USER plays " + str(action.x) + " " + str(action.y))
    else:
        print("CPU TURN")
        action = computer_play(state)
        print("CPU plays " + str(action.x) + " " + str(action.y))
    print("Result:")
    ret = result(state, action)
    print_with_actions(ret.board, find_all_actions(ret))
    return ret


def play():
    state = State(init_board(), P1)
    print_board(state.board)
    while True:
        state = take_action(state)
        print("Result:")
        # print_with_actions(state.board, actions)
        winner = state.terminal_test()
        if winner >= 0:
            break
    if winner == P1:
        print("User wins!")
    elif winner == P2:
        print("CPU wins!")
    else:
        print("Tie!")
    print("Final board:")
    print_board(state.board)
    return winner


def test():
    state = State(alt_init_board(), P2)
    print_board(state.board)
    while True:
        state = take_action(state)
        # print("Result:")
        # print_with_actions(state.board, actions)
        winner = state.terminal_test()
        if winner >= 0:
            break
    print_board(state.board)
    if winner == P1:
        print("User wins!")
    elif winner == P2:
        print("CPU wins!")
    else:
        print("Tie!")


def batch():
    iters = int(input("Please enter a number of times play against random opponent\n"))
    cpu_wins = 0
    user_wins = 0
    for i in range(iters):
        winner = play()
        if winner == P1:
            user_wins += 1
        elif winner == P2:
            cpu_wins += 1
    print("USER won " + str(user_wins))
    print("CPU won " + str(cpu_wins))


max_depth = int(input("Please enter a maximum depth for alpha-beta cutoff search. Enter -1 for maximum depth\n"))
if max_depth < 0:
    max_depth = np.inf
# play()
# test()
batch()
