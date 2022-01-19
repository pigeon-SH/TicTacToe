import pygame
from AI import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def equal3(a, b, c):
    return (a == b and b == c and c == a and a != '.')

class Player:
    def __init__(self, key, isAI):
        self.isAI = isAI
        if isAI:
            # Choose AI Algorithm
            #self.AI = Minimax(3, 3, key)
            self.AI = AlphaBeta(3, 3, key)
            
class Game:
    def __init__(self):
        self.player = {'O':Player('O', isAI=True), 'X':Player('X', isAI=False)}
        self.turn = 'X'

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

    def get_spot(self):
        if self.player[self.turn].isAI:

            """
            # use AI algorithm - random pick
            blanks = []
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.board[i][j] == '.':
                        blanks.append([i, j])
            idx = random.randrange(0, len(blanks))
            return blanks[idx]
            """
            # use AI algorithm
            spot = self.player[self.turn].AI.get_spot(self.board)
            return spot
            
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
        
        while not self.gameEnd:
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