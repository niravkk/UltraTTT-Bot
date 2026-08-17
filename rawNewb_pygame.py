from ultra_pygame import initial_state, result, actions, winner, bigToSmall, terminal, player, Button
import random
import ast
import math
import copy
import pygame

X = "X"
O = "O"

nSims = 20000

#screen size
SS=600


pygame.init()
screen = pygame.display.set_mode((SS,SS))
running = True


#standard value(for UCB1)
C = math.sqrt(2)

def main():
    board = list(initial_state())
    current= "X"
    pygame.init()
    screen = pygame.display.set_mode((SS,SS))
    clock = pygame.time.Clock()
    running = True
    #offset so it doesn't look fully like a grid
    width = SS//120

    buttons = initial_state()
    #each square has a button class associated with it stored in array
    for i in range(3):
        for j in range(3):
            for k in range(3):
                buttons[i][j][k][0]=Button(width+j*SS/3+0, k*SS/9+width+i*SS/3, SS/9-width)
                buttons[i][j][k][1]=Button(width+j*SS/3+SS/9, k*SS/9+width+i*SS/3, SS/9-width)
                buttons[i][j][k][2]=Button(width+j*SS/3+2*SS/9,k*SS/9+ width+i*SS/3,SS/9-width)



    while running:
        click = False
        movePre = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click= True
        
        pygame.draw.line(screen, (255,255,255), (SS/3,0), (SS/3,SS), width=width)
        pygame.draw.line(screen, (255,255,255), (2*SS/3,0), (2*SS/3,SS), width=width)
        pygame.draw.line(screen, (255,255,255), (0,SS/3), (SS,SS/3), width=width)
        pygame.draw.line(screen, (255,255,255), (0,2*SS/3), (SS,2*SS/3), width=width)

        for x in range(3):
            for y in range(3):
                pygame.draw.line(screen, (255,255,255),(x*SS/3+SS/9,width+y*SS/3), (x*SS/3+SS/9,SS/3-width+y*SS/3))
                pygame.draw.line(screen, (255,255,255),(x*SS/3+2*SS/9,width+y*SS/3), (x*SS/3+2*SS/9,SS/3-width+y*SS/3))
                pygame.draw.line(screen, (255,255,255),(x*SS/3+width, SS/9+y*SS/3),(x*SS/3+SS/3-width,SS/9+y*SS/3))
                pygame.draw.line(screen, (255,255,255),(x*SS/3+width, 2*SS/9+y*SS/3),(x*SS/3+SS/3-width,2*SS/9+y*SS/3))

        mouse_pos = pygame.mouse.get_pos()
        #if players turn and there has been a mouse click
        if current == X and click:
            for i in range(3):
                    for j in range(3):
                        for k in range(3):
                            for l in range(3):
                                buttons[i][j][k][l].draw(screen)
                                ifClick=(buttons[i][j][k][l].click(mouse_pos))
                                if ifClick and buttons[i][j][k][l].text == None:
                                    #add information where ever necessary
                                    buttons[i][j][k][l].text= X
                                    movePre = [i,j,k,l]
                                    board = result(board, movePre)
                                    current=O
                                    reduced = bigToSmall(board)
                                    if winner(reduced) == X:
                                        print(X)
                                    elif winner(reduced) == O:
                                        print(O)
                                    buttons[i][j][k][l].draw(screen)
                                    pygame.display.flip()

        if current ==O:
            #run the monte carlo to find best move
            move = monteCarlo(board, movePre)
            board = result(board, move)
            movePre = move
            buttons[move[0]][move[1]][move[2]][move[3]].text = O
            current = X
            reduced = bigToSmall(board)
            if winner(reduced) == X:
                print(X)
            elif winner(reduced) == O:
                print(O)
            buttons[move[0]][move[1]][move[2]][move[3]].draw(screen)

        #this needs to happen for new stuff to actually appear(like a refresh)
        pygame.display.flip()
        clock.tick(60)


#p = player
def monteCarlo(board, prev):
    """
    returns an action based on monte carle tree search
    """
    parentExplo = 0
    # store every valid action in 'board' and asigns value [0] = number of wins it led to [1] = total sims
    eval = {}
    # value attached to each action
    UCB1 = -math.inf
    for action in actions(board,prev):
        #assigning every action values of 0
        eval[action] = [0,0]
    for i in range(nSims):
        max = -math.inf
        a = None
        if parentExplo != 0:
            for action, evaL in eval.items():
                #SELECTION
                if evaL[1] != 0:
                    # formula that decides which action is to be chosen
                    UCB1 = evaL[0]/evaL[1] + C*math.sqrt(math.log(parentExplo, math.e)/evaL[1])
                else:
                    #if it is [1] = 0 then assign inf(saw this in some blog dunno if it is correct)
                    UCB1 = math.inf
                if max < UCB1:
                    max = UCB1
                    a = action
        else:
            #if no sims have happened then no info so random
            a = random.choice(actions(board, prev))

        board_copy = [[[cell[:] for cell in micro_row] for micro_row in macro_row] for macro_row in board]
        win_loss = randomSim(result(board_copy, a), a) 
        if win_loss == player(board):
            # if there is a win add 1 to both no. of wins and total sims
            eval[a][0] += 1
            eval[a][1] += 1
        else:
            # if there is a draw or loss then add 1 to only total sims
            eval[a][1] += 1
        parentExplo +=1

    #just to decide which is best
    hAction = None
    hStats = -math.inf
    for i,q in eval.items():
        if q[1] >hStats:
            hAction = i
            hStats = q[1]
    return hAction

        
def randomSim(board, prev):
    """
        runs a simulation from state board till it is terminal/ended
        return 1 if win
                0 if draw
                -1 if loss
    """
    nBoard = copy.deepcopy(board)
    while terminal(nBoard, True) == False:
        A = actions(nBoard, prev)
        totA = A[random.randint(0,len(A)-1)]
        nBoard = result(nBoard, totA)
        
    return winner(nBoard, True)


if __name__ == "__main__":
    main()