from Connect4 import Connect4
from Player import Player, Agent
import argparse


import numpy as np

def AIvsAI(board_size):

    myConnect4_AI1 = Connect4(Agent('AI 1'),Player('p1'), posAi = 0, board_size = board_size, max_step = board_size[0]*board_size[1])
    myConnect4_AI2 = Connect4(Player('p1'),Agent('AI 2'), posAi = 1, board_size = board_size, max_step = board_size[0]*board_size[1])

    AIs = [myConnect4_AI1, myConnect4_AI2]
    players = [myConnect4_AI1.players[0],myConnect4_AI2.players[1]]
    winner = None

    while not myConnect4_AI1.terminal_Test():
        n_player = myConnect4_AI1.step % 2
        current_player = players[n_player]
        print(current_player.name," is thinking ...")

        action = current_player.action(AIs[n_player]) - 1
        for AI in AIs:
            AI.move(action) 

        print(myConnect4_AI1)

        winner = current_player.name

    print("Game Over")
    if myConnect4_AI1.step < 72:
        print(f"Congrats to {winner} !!")
    else:
        print("Oops, it is a tie !")
 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--board_size', default=(6,12), help="Give the board size in the shape -- n_lines n_columns)",type = int, required = False, nargs = 2)
    parser.add_argument('--iaVSia', default = False, help = "(bool) To make two IAs play together", type=bool, required= False)
    args = parser.parse_args()

    board_size = tuple(args.board_size)
    if args.iaVSia : 
        AIvsAI(args.board_size)
    else:
        first = ''

        while first.upper() != 'Y' and first.upper() != 'YES' and first.upper() != 'N' and first.upper() != 'NO':
            first = input('Do you want to play first? (Y/N)')

        if first.upper() == 'Y' or "YES":
            myConnect4 = Connect4(Player('p1'), Agent(), posAi = 1, board_size = board_size)
        else :
            myConnect4 = Connect4(Agent(),Player('p1'), posAi = 0, board_size = board_size)


        print(myConnect4)

        myConnect4.start()

    #board_size = (6,12)

    #AIvsAI(board_size)
    #myConnect4 = Connect4(Player('p1'), Agent(), posAi = 1)
    #myConnect4 = Connect4(Agent(),Player('p1'), posAi = 0, board_size = board_size)
    #myConnect4 = Connect4(Player('p1'),Player('p2'), board_size = board_size)