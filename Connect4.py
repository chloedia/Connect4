# Connect4 class
# Setting the Environment for the Game

#Coded by Chloé Daems & Bruce Dakin

import numpy as np
from scipy.stats import multivariate_normal
from colorama import Fore, Back, Style

class Connect4:
    def __init__(self, player1 : object, player2: object , posAi = None, board_size : tuple = (6,12), state: np.array = None, step = 0, max_step = 42) -> None:

        self.players = [player1, player2]
        self.posAi = posAi
        self.max_step = max_step

        if board_size[0] < 4:
            raise Exception("The height of the board needs to be at least 4")
        if board_size[1] < 4:
            raise Exception("The width of the board needs to be at least 4")
        
        if state is not None :
            self.board_size = state.shape
            self.state = state

        else: 
            self.board_size = board_size
            self.state = np.zeros(self.board_size)

        self.step = step
        self.heuristique = self.create_heuristique()

    def create_heuristique(self):
        mean = [0, 0]
        cov = [[2, 0], [0, 5]]
        x, y= np.random.multivariate_normal(mean, cov, 10000).T

        hist, _, _= np.histogram2d(x, y, bins=[self.board_size[0],self.board_size[1]], range = [[-self.board_size[0]//2,self.board_size[0]//2],[-self.board_size[1]//2,self.board_size[1]//2]])
        hist = (hist - hist.min())/(hist.max() - hist.min())
        return (hist * 15 + 3).astype(int)


    def move(self, action) -> bool:
        for i in reversed(range(self.board_size[0])):
            if(self.state[i,action] == 0):
                if self.posAi is not None:
                    self.state[i,action] = 1 if self.step % 2 == self.posAi else -1
                else: 
                    self.state[i,action] = -1 if self.step % 2 == 0 else 1
                self.step += 1
                return True

        #If the move could not be done
        print("You cannot play this, column #",action," is already full ...")
        return False
    
    def diagonal(self, T = False):
        state = self.state

        if T:
            state = state.T

        diags = [state[::-1,:].diagonal(i) for i in range(-state.shape[0]+1,state.shape[1])]
        diags.extend(state.diagonal(i) for i in range(state.shape[1]-1,-state.shape[0],-1))
        diags = [n.tolist() for n in diags if len(n)>3]
        return diags

    def terminal_Test(self) -> bool:
        # Check if all the coin were played      
        if (self.step == self.max_step):
            return True
        
        #Check if there is a vertical win
        v_stack = []
        for i in range(self.state.shape[0]):
            for j in range(self.state.shape[1]):
                if self.state[i,j] != 0:
                    v_stack.append(self.state[i,j])
                else:
                    v_stack.clear()
                if len(v_stack)>4:
                    v_stack.pop(0)
                if sum(v_stack) == -4 or sum(v_stack) == 4:
                    return True
            v_stack.clear()
        
        #Check if there is an horizontal win
        h_stack = []
        for j in range(self.state.shape[1]):
            for i in range(self.state.shape[0]):
                if self.state[i,j] != 0:
                    h_stack.append(self.state[i,j])
                else:
                    h_stack.clear()

                if len(h_stack)>4:
                    h_stack.pop(0)
                if sum(h_stack) == -4 or sum(h_stack) == 4:
                    return True
            h_stack.clear()
        
        # test d'une succession diagonale vers la droite
        i=j=0
        while(i<=self.state.shape[0] - 4 and j<=self.state.shape[1] - 4):
            if (self.state[i][j]==self.state[i+1][j+1] and self.state[i][j]==self.state[i+2][j+2] and self.state[i][j]==self.state[i+3][j+3]and self.state[i][j]!=0):
                return True
            if (j==self.state.shape[1] - 4):
                i=i+1
                j=0
            else:
                j=j+1
    
        # test d'une succession diagonale vers la gauche 
        
        i=0
        j=self.state.shape[1]-1
        while(i<=self.state.shape[0] - 4 and j>=3):
            if (self.state[i][j]==self.state[i+1][j-1] and self.state[i][j]==self.state[i+2][j-2] and self.state[i][j]==self.state[i+3][j-3] and self.state[i][j]!=0):
                return True
            if (j==3):
                i=i+1
                j= self.state.shape[1]-1
            else:
                j=j-1
        
        return False

    def start(self):
        winner = None
        while not self.terminal_Test():
            current_player = self.players[self.step % 2]
            action = current_player.action(self) - 1
            self.move(action)
            print(self)
            winner = current_player.name
        
        print("Game Over")
        if self.step < self.max_step:
            print(f"Congrats to {winner} !!")
        else:
            print("Oops, it is a tie !")

    def __str__(self) -> str:

        affect = {
            -1 : Back.RED + Fore.RED + "X" + Back.BLACK + Fore.WHITE,
            1 : Back.BLUE + Fore.BLUE + "Y" + Back.BLACK + Fore.WHITE,
            0 : Back.BLACK + Fore.WHITE + "."}
        str_state = str("\n|" + '{:^3}|'*self.board_size[1] +"\n").format(*np.arange(1,self.board_size[1]+1))

        for line in self.state:
            str_state += str("\n| " + Back.BLACK + Fore.WHITE + '{} | '*self.board_size[1] +"\n").format(*[affect[elmt] for elmt in line])
        return str_state
                 

    
