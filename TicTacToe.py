from json.encoder import INFINITY
import pygame
import random
import copy

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def equal3(a, b, c):
    return (a == b and b == c and c == a and a != '.')

class Player:
    def __init__(self, isAI):
        self.isAI = isAI

class Game:
    def __init__(self):
        self.player = {'O':Player(isAI=False), 'X':Player(isAI=True)}
        self.turn = 'O'

        self.rows = 3
        self.cols = 3
        self.board = [['.' for i in range(self.cols)] for j in range(self.rows)]    # self.board[rows][cols]
        self.blank_cnt = self.cols * self.rows
        self.blanks = [[i, j] for i in range(self.rows) for j in range(self.cols)]

        self.gameEnd = False
        self.result = ''

        self.screen_size = (600, 600)   # size (width, height)
        self.screen = pygame.display.set_mode(self.screen_size)

        self.box_size = (self.screen_size[0] / self.cols, self.screen_size[1] / self.rows)  #size (width, height)

        self.radius = min(self.box_size) * (9 / 10) / 2
        self.line_width = 2 

    def nextTurn(self):
        if self.turn == 'O':
            self.turn = 'X'
        else:
            self.turn = 'O'
    
    def checkResult(self):
        winner = None
        for i in range(self.rows):
            if equal3(self.board[i][0], self.board[i][1], self.board[i][2]):
                winner = self.board[i][0]
                return winner
        
        for i in range(self.cols):
            if equal3(self.board[0][i], self.board[1][i], self.board[2][i]):
                winner = self.board[0][i]
                return winner

        if equal3(self.board[0][0], self.board[1][1], self.board[2][2]):
            winner = self.board[0][0]
            return winner

        elif equal3(self.board[0][2], self.board[1][1], self.board[2][0]):
            winner = self.board[0][2]
            return winner

        else:
            if self.blank_cnt == 0:
                return 'Game Tie'

        return winner
    
    def getScore(self, board, agent, enemy):
        winner = None
        for i in range(self.rows):
            if equal3(board[i][0], board[i][1], board[i][2]):
                winner = board[i][0]
        
        if winner == None:
            for i in range(self.cols):
                if equal3(board[0][i], board[1][i], board[2][i]):
                    winner = board[0][i]

        if winner == None:
            if equal3(board[0][0], board[1][1], board[2][2]):
                winner = board[0][0]

            elif equal3(board[0][2], board[1][1], board[2][0]):
                winner = board[0][2]

            else:
                if self.blank_cnt == 0:
                    winner = 'Tie'

        if winner == agent:
            return 100
        elif winner == enemy:
            return -100
        elif winner == 'Tie':
            return 0
        else:
            return None
    
    def putdown(self, spot):
        r, c = spot
        if self.board[r][c] == '.':
            self.board[r][c] = self.turn
            self.draw(spot, self.turn)
            self.blank_cnt -= 1
            return True
        else:
            print("Cannot putdown at", spot)
            return False

    def maxAgent(self, board, agent, enemy, depth, maxdepth):
        if depth >= maxdepth:
            return 0
        else:
            score = self.getScore(board, agent, enemy)
            if score != None:
                return score
        
        # not game end
        maxscore = -INFINITY
        for i in range(self.rows):
            for j in range(self.cols):
                if board[i][j] == '.':
                    newboard = copy.deepcopy(board)
                    newboard[i][j] = agent
                    score = self.minAgent(newboard, agent, enemy, depth + 1, maxdepth)
                    if score > maxscore:
                        maxscore = score
        
        return maxscore

    def minAgent(self, board, agent, enemy, depth, maxdepth):
        if depth >= maxdepth:
            return 0
        else:
            score = self.getScore(board, agent, enemy)
            if score != None:
                return score
        
        # not game end
        minscore = INFINITY
        for i in range(self.rows):
            for j in range(self.cols):
                if board[i][j] == '.':
                    newboard = copy.deepcopy(board)
                    newboard[i][j] = enemy
                    score = self.maxAgent(newboard, agent, enemy, depth + 1, maxdepth)
                    if score < minscore:
                        minscore = score
        
        return minscore

    def get_spot(self):
        if self.player[self.turn].isAI:
            blanks = []
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.board[i][j] == '.':
                        blanks.append([i, j])
            """
            # use AI algorithm - random pick
            idx = random.randrange(0, len(blanks))
            return blanks[idx]
            """

            # use AI algorithm - Minimax Algorithm
            maxdepth = 3
            maxscore = -INFINITY
            maxspot = None
            if self.turn == 'O':
                enemy = 'X'
            else:
                enemy = 'O'
            for spot in blanks:
                newboard = copy.deepcopy(self.board)
                newboard[spot[0]][spot[1]] = self.turn
                score = self.minAgent(newboard, self.turn, enemy, 0, maxdepth)
                if score > maxscore:
                    maxspot = spot
                    maxscore = score

            return maxspot
            
        else:
            # Human Player
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        point = pygame.mouse.get_pos()
                        board_point = (int(point[1] / self.box_size[1]), int(point[0] / self.box_size[0]))
                        return board_point
                    
                    elif event.type == pygame.QUIT:
                        self.gameEnd = True
                        return None
    
    def drawBoard(self):
        # Draw Horizontal
        for i in range(self.rows):
            start_point = (0, self.box_size[1] * (i + 1))
            end_point = (self.screen_size[0], self.box_size[1] * (i + 1))
            pygame.draw.line(self.screen, BLACK, start_point, end_point)
        # Draw Vertical
        for i in range(self.cols):
            start_point = (self.box_size[0] * (i + 1), 0)
            end_point = (self.box_size[0] * (i + 1), self.screen_size[1])
            pygame.draw.line(self.screen, BLACK, start_point, end_point)
    
    def draw(self, spot, shape):
        center = ((spot[1] + 1 / 2) * self.box_size[0], (spot[0] + 1 / 2) * self.box_size[1])
        if shape == 'O':
            pygame.draw.circle(self.screen, BLACK, center, self.radius, self.line_width)
        else:
            start_point = (center[0] - self.radius, center[1] - self.radius)
            end_point = (center[0] + self.radius, center[1] + self.radius)
            pygame.draw.line(self.screen, BLACK, start_point, end_point, self.line_width)
            start_point = (center[0] - self.radius, center[1] + self.radius)
            end_point = (center[0] + self.radius, center[1] - self.radius)
            pygame.draw.line(self.screen, BLACK, start_point, end_point, self.line_width)        
    
    def start(self):
        pygame.init()
        pygame.font.init()

        pygame.display.set_caption("TicTacToe")
        self.screen.fill(WHITE)   # background color: white

        self.drawBoard()
        
        while True:
            pygame.display.flip()
            
            spot = self.get_spot()
            while spot and not self.putdown(spot):
                spot = self.get_spot()

            self.result = self.checkResult()
            if self.result != None:
                break
            self.nextTurn()

        print(self.result)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.start()