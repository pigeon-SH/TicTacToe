import copy
import torch
import torch.nn as nn

INFINITY = 1000000000

def equal3(a, b, c):
    return (a == b and b == c and c == a and a != '.')

class Minimax:
    def __init__(self, rows, cols, my):
        self.rows = rows
        self.cols = cols

        self.__blank = '.'

        self.win_score = 100
        self.lose_score = -100

        self.my = my

    def actions(self, state):
        actions = []
        for i in range(self.rows):
            for j in range(self.cols):
                if state[i][j] == self.__blank:
                    actions.append((i, j))
        
        return actions
    
    def player(self, state):
        cnt = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if state[i][j] != self.__blank:
                    cnt += 1
        
        if cnt % 2 == 0:
            return 'X'
        else:
            return 'O'
    
    def blankcnt(self, state):
        cnt = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if state[i][j] == self.__blank:
                    cnt += 1
        return cnt

    def result(self, state, action):    # return the new state after do action
        newstate = copy.deepcopy(state)
        newstate[action[0]][action[1]] = self.player(state)
        return newstate
    
    def terminate(self, state):
        actions = self.actions(state)
        if len(actions) == 0:
            return True
        for i in range(self.rows):
            if equal3(state[i][0], state[i][1], state[i][2]):
                return True
        for i in range(self.cols):
            if equal3(state[0][i], state[1][i], state[2][i]):
                return True
        if equal3(state[0][0], state[1][1], state[2][2]):
            return True
        if equal3(state[0][2], state[1][1], state[2][0]):
            return True
    
    def utility(self, state):
        blanks = self.blankcnt(state)
        for i in range(self.rows):
            if equal3(state[i][0], state[i][1], state[i][2]):
                if state[i][0] == self.my:
                    return self.win_score + blanks
                else:
                    return self.lose_score - blanks
                
        for i in range(self.cols):
            if equal3(state[0][i], state[1][i], state[2][i]):
                if state[0][i] == self.my:
                    return self.win_score + blanks
                else:
                    return self.lose_score - blanks

        if equal3(state[0][0], state[1][1], state[2][2]):
            if state[0][0] == self.my:
                return self.win_score + blanks
            else:
                return self.lose_score - blanks

        if equal3(state[0][2], state[1][1], state[2][0]):
            if state[0][2] == self.my:
                return self.win_score + blanks
            else:
                return self.lose_score - blanks
        
        return 0

    def maxAgent(self, state):
        if self.terminate(state):
            return self.utility(state)

        v = -INFINITY
        for act in self.actions(state):
            v = max(v, self.minAgent(self.result(state, act)))
        return v

    def minAgent(self, state):
        if self.terminate(state):
            return self.utility(state)
        
        v = INFINITY
        for act in self.actions(state):
            v = min(v, self.maxAgent(self.result(state, act)))
        return v
    
    def get_spot(self, state):
        v = -INFINITY
        spot = None
        for act in self.actions(state):
            score = self.minAgent(self.result(state, act))
            if score > v:
                v = score
                spot = act

        return spot

class AlphaBeta:
    def __init__(self, rows, cols, my):
        self.rows = rows
        self.cols = cols

        self.__blank = '.'

        self.win_score = 10
        self.lose_score = -10

        self.my = my

    def actions(self, state):
        actions = []
        for i in range(self.rows):
            for j in range(self.cols):
                if state[i][j] == self.__blank:
                    actions.append((i, j))
        
        return actions
    
    def player(self, state):
        cnt = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if state[i][j] != self.__blank:
                    cnt += 1
        
        if cnt % 2 == 0:
            return 'X'
        else:
            return 'O'
    
    def blankcnt(self, state):
        cnt = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if state[i][j] == self.__blank:
                    cnt += 1
        return cnt

    def result(self, state, action):    # return the new state after do action
        newstate = copy.deepcopy(state)
        newstate[action[0]][action[1]] = self.player(state)
        return newstate
    
    def terminate(self, state):
        actions = self.actions(state)
        if len(actions) == 0:
            return True
        for i in range(self.rows):
            if equal3(state[i][0], state[i][1], state[i][2]):
                return True
        for i in range(self.cols):
            if equal3(state[0][i], state[1][i], state[2][i]):
                return True
        if equal3(state[0][0], state[1][1], state[2][2]):
            return True
        if equal3(state[0][2], state[1][1], state[2][0]):
            return True
    
    def utility(self, state):
        blanks = self.blankcnt(state)
        for i in range(self.rows):
            if equal3(state[i][0], state[i][1], state[i][2]):
                if state[i][0] == self.my:
                    return self.win_score + blanks
                else:
                    return self.lose_score - blanks
                
        for i in range(self.cols):
            if equal3(state[0][i], state[1][i], state[2][i]):
                if state[0][i] == self.my:
                    return self.win_score + blanks
                else:
                    return self.lose_score - blanks

        if equal3(state[0][0], state[1][1], state[2][2]):
            if state[0][0] == self.my:
                return self.win_score + blanks
            else:
                return self.lose_score - blanks

        if equal3(state[0][2], state[1][1], state[2][0]):
            if state[0][2] == self.my:
                return self.win_score + blanks
            else:
                return self.lose_score - blanks
        
        return 0

    def maxAgent(self, state, alpha, beta):
        if self.terminate(state):
            return self.utility(state)

        v = -INFINITY
        for act in self.actions(state):
            v = max(v, self.minAgent(self.result(state, act), alpha, beta))
            if v > alpha:
                alpha = v
                if alpha >= beta:
                    break
        return v

    def minAgent(self, state, alpha, beta):
        if self.terminate(state):
            return self.utility(state)
        
        v = INFINITY
        for act in self.actions(state):
            v = min(v, self.maxAgent(self.result(state, act), alpha, beta))
            if v < beta:
                beta = v
                if beta <= alpha:
                    break 
        return v
    
    def get_spot(self, state):
        v = -INFINITY
        alpha = -INFINITY
        beta = INFINITY
        spot = None
        for act in self.actions(state):
            score = self.minAgent(self.result(state, act), alpha, beta)
            if score > v:
                v = score
                spot = act
            if v > alpha:
                alpha = v
                if alpha >= beta:
                    break

        return spot

class MCTS:
    #########################################################
    #   TODO: need to study MCTS and apply it to TicTacToe  #
    #########################################################
    def __init__(self):
        pass

    def terminal(self, state):
        actions = self.actions(state)
        if len(actions) == 0:
            return True
        for i in range(self.rows):
            if equal3(state[i][0], state[i][1], state[i][2]):
                return True
        for i in range(self.cols):
            if equal3(state[0][i], state[1][i], state[2][i]):
                return True
        if equal3(state[0][0], state[1][1], state[2][2]):
            return True
        if equal3(state[0][2], state[1][1], state[2][0]):
            return True
    
    def fully_expanded(self, v):
        pass        
    
    def BestChild(v, c):    # By UCB1
        #v: node, c: hyperparameter
        
        return np.argmax()
    
    def TreePolicy(self, v):
        #v: node
        while not self.terminal(v):
            if not fully_expanded(v):
                return expand(v)
            else:
                v = bestchild(v, Cp)
        
        return v