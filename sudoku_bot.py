import pygame
import time

#global constants
BG_COLOR = (230, 231, 232)
SELECT_COLOR = (73, 214, 87)
LOCKED_TEXT_COLOR = (34, 127, 181)
GUESS_TEXT_COLOR = (0,0,0)
WIDTH = 550
HEIGHT = 650
BUFFER = 5

board = [
        [7,8,0,4,0,0,1,2,0],
        [6,0,0,0,7,5,0,0,9],
        [0,0,0,6,0,1,0,7,8],
        [0,0,7,0,4,0,2,6,0],
        [0,0,1,0,5,0,9,3,0],
        [9,0,4,0,6,0,0,0,5],
        [0,7,0,3,0,0,0,1,2],
        [1,2,0,0,0,7,4,0,0],
        [0,4,9,2,0,6,0,0,7]
    ]
   
initial_board = board.copy()
for i in range(len(board)):
    initial_board[i] = board[i].copy()

class Game:
    # function for user inserting a number in a tile
    def insert(self, position):
        i, j = position[1], position[0]
        font = pygame.font.SysFont('Comic Sans MS', 35)
        while True:
            if initial_board[i-1][j-1] != 0:
                return

            pygame.draw.rect(self.scrn, SELECT_COLOR, (position[0]*50 + BUFFER, position[1]*50 + BUFFER, 50 - BUFFER*2, 50 - BUFFER*2))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if(event.key == 8):
                        board[i-1][j-1] = 0
                        pygame.draw.rect(self.scrn, BG_COLOR, (position[0]*50 + BUFFER, position[1]*50 + BUFFER, 50 - BUFFER*2, 50 - BUFFER*2))
                        pygame.display.update()
                        return
                    if(0 < event.key - 48 < 10):
                        pygame.draw.rect(self.scrn, BG_COLOR, (position[0]*50 + BUFFER, position[1]*50 + BUFFER, 50 - BUFFER*2, 50 - BUFFER*2))
                        value = font.render(str(event.key-48), True, GUESS_TEXT_COLOR)
                        self.scrn.blit(value, (position[0]*50 + 15, position[1]*50))
                        pygame.display.update()
                        return
                    return

    # function for visualizing the steps of the solving algorithm in solve()
    def update_board(self):
        font = pygame.font.SysFont('Comic Sans MS', 35)
        
        for i in range(0, len(board[0])):
            for j in range(0, len(board[0])):
                if(0<board[i][j]<10) and (initial_board[i][j] == 0):
                    value = font.render(str(board[i][j]), True, GUESS_TEXT_COLOR)
                    self.scrn.blit(value, ((j+1)*50 + 15, (i+1)*50 ))
                if(board[i][j] != 0) and (initial_board[i][j] == 0):
                    pygame.draw.rect(self.scrn, BG_COLOR, ((j+1)*50 + BUFFER, (i+1)*50 + BUFFER, 50 - BUFFER*2, 50 - BUFFER*2))
                    value = font.render(str(board[i][j]), True, GUESS_TEXT_COLOR)
                    self.scrn.blit(value, ((j+1)*50 + 15, (i+1)*50))
                    pygame.display.update()
        pygame.display.update()
        return

    # main function for pygame GUI
    def main(self):
        pygame.init()
        self.scrn = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Play Sudoku")
        self.scrn.fill(BG_COLOR)
        font = pygame.font.SysFont('Comic Sans MS', 35)

        for i in range(0,10):
            if i % 3 == 0:
                pygame.draw.line(self.scrn, (0,0,0), (50 + 50*i, 50), (50 + 50*i, 500), 5)
                pygame.draw.line(self.scrn, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 5)
            else:
                pygame.draw.line(self.scrn, (0,0,0), (50 + 50*i, 50), (50 + 50*i, 500), 2)
                pygame.draw.line(self.scrn, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 2)
        pygame.display.update()

        for i in range(0, len(board[0])):
            for j in range(0, len(board[0])):
                if(0<board[i][j]<10):
                    value = font.render(str(board[i][j]), True, LOCKED_TEXT_COLOR)
                    self.scrn.blit(value, ((j+1)*50 + 15, (i+1)*50 ))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    self.insert((pos[0]//50, pos[1]//50))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.solve(board)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

    # attempts to solve the board through recursion,
    #   if every possible number in a tile is invalid, 
    #   backtracks to a previous tile
    def solve(self, b):
        find = self.find_empty(b)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.valid(b, i, (row,col)):
                b[row][col] = i
                pygame.draw.rect(self.scrn, SELECT_COLOR, ((col+1)*50 + BUFFER, (row+1)*50 + BUFFER, 50 - BUFFER*2, 50 - BUFFER*2))
                pygame.display.update()

                time.sleep(0.25)
                self.update_board()
                if self.solve(b):
                    return True
            
                b[row][col] = 0

        return False  

    # checks if a number in a tile on the board is valid following sudoku rules
    def valid(self, b, num, pos):
        for i in range(len(b[0])):
            if (b[pos[0]][i] == num) and (pos[1] != i):
                return False

        for i in range(len(b[0])):
            if (b[i][pos[1]] == num) and (pos[0] != i):
                return False

        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if (b[i][j] == num) and ((i, j) != pos):
                    return False
        return True

    # finds the next empty tile (going from left to right, then top to bottom)
    def find_empty(self, b):
        for i in range(len(b)):
            for j in range(len(b[0])):
                if (b[i][j] == 0):
                    return (i, j)
        return None

    # used for debugging and early stages
    def print_board(self, b):
        for i in range(len(b)):
            if (i % 3 == 0) and (i != 0):
                print("=======================")

            for j in range(len(b[0])):
                if (j % 3 == 0) and (j != 0):
                    print(" | ", end = "")

                if( j == 8):
                    print(b[i][j])
                else:
                    print(str(b[i][j]) + " ", end="")

game = Game()
game.main()