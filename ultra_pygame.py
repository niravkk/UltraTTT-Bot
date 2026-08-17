import math
import copy
import pygame
X = "X"
O = "O"     
current = None
board = []
play = None

def initial_state():
    """
    Returns starting state of the board.
    """
    base = [[None, None, None],
            [None, None, None],
            [None, None, None]]
    goof = [[None, None, None],
            [None, None, None],
            [None, None, None]]
    for i in range(3):
        for j in range(3):
            goof[i][j] = [[None, None, None],
            [None, None, None],
            [None, None, None]]
    return goof

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    #number of Xs and Os
    numX = 0
    numO = 0
    for i in range(3):
        for q in range(3):
            for x in range(3):
                for y in range(3):
                    if board[i][q][x][y]== X:
                        numX += 1
                    elif board[i][q][x][y] == O:
                        numO += 1
    if numX == numO:
        return X
    elif numX > numO:
        return O
    
def bigToSmall(Oldboard):
    """
    converts 3x3x3x3 board to 3x3 by check each inner board
    """
    board = Oldboard
    conv = [[None, None, None], [None, None, None], [None, None, None]]
    for i in range(3):
        for q in range(3):
            conv[i][q]=winner(board[i][q])
    return conv

def actions(board, prev=None):
    """
    Returns set of all possible actions (i, q, x, y) available on the board.
    """
    board = board
    possible_actions = []
    # if there is no previous move then free move
    if prev == None:
        for i in range(3):
            for q in range(3):
                for x in range(3):
                    for y in range(3):
                        if board[i][q][x][y] == None:
                            possible_actions.append((i, q, x, y))
    else:
        # free move check
        if(terminal(board[prev[2]][prev[3]])):
            return actions(board)
        # the valid moves in the inner board 
        for x in range(3):
            for y in range(3):
                if board[prev[2]][prev[3]][x][y] == None:
                    possible_actions.append((prev[2], prev[3], x, y))
    return possible_actions
                
def result(board, action):  
    """
    Returns the board that results from making move (i, j) on the board.
    """
    r_board = board
    r_action = action
    if r_board[r_action[0]][r_action[1]][r_action[2]][r_action[3]]!= None:
        #I hate this I hate this I hate this
        raise ValueError("git gud")
    else:
        turn = player(r_board)
        r_board[r_action[0]][r_action[1]][r_action[2]][r_action[3]]= turn
    return r_board

def winner(Oboard, big= False):
    """
    Returns the winner of the game, if there is one.
    """
    board = Oboard
    if big == True:
        board = bigToSmall(board)
    for w in [X, O]:
        #diagonally
        if ((board[0][0] == w and board[1][1] == w and board[2][2] == w) or
            (board[0][2] == w and board[1][1] == w and board[2][0] == w)):
            return w
        #vertical
        for j in range(3):
            if board[0][j] == w and board[1][j] == w and board[2][j] == w:
                return w
        #horizontal
        for i in range(3):
            if board[i][0] == w and board[i][1] == w and board[i][2] == w:
                return w
    return None
        
def terminal(board, big = False):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board, big) == None:
        if big:
            sum = 0
            for i in range(3):
                for q in range(3):
                    for x in range(3):
                        for y in range(3):
                            if board[i][q][x][y] != None:
                                sum += 1
            #if all squares are filled then game over
            if sum == 81:
                return True
            else:
                return False
        else:
            sum = 0
            for i in range(3):
                for q in range(3):   
                    if board[i][q] != None:
                                sum += 1
            if sum == 9:
                return True
            else:
                return False
    else:
        return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner = winner(board, True)
    if winner == X:
        return 1
    elif winner == O:
        return -1
    else:
        return 0

class Button:
    def __init__(self, x, y, side, text=None):
        self.rect = pygame.Rect(x, y, side, side)
        self.text = text
        self.font = pygame.font.SysFont("Arial", 24)
    def draw(self, screen):
        pygame.draw.rect(screen,(0,0,0), self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, text_surface.get_rect(center=self.rect.center))
    def click(self, mousePos):
        return self.rect.collidepoint(mousePos)