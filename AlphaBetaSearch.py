from Connect4 import Connect4
import numpy as np
import random as rand
import copy

#LISTE DES ACTIONS POSSIBLE

#-------------------------------------------------------
def Actions(x: np.array) -> list:
    actions=[]
    for i in range(x.shape[1]):
        if(x[0][i]==0):
            actions.append(i)
    
    return actions
#-------------------------------------------------

#HEURISTIQUE DE NOTATION DE GRILLE

#-------------------------------------------------
def Heuristique(s:np.array, heuristique:list)-> 'int':
    #TODO : Multivariate gaussian (search)
    '''tableauEvaluation = [[3, 4, 5, 7, 7, 7, 7, 7, 7, 5, 4, 3],
                         [4, 6, 8, 10, 10, 10, 10, 10, 10, 8, 6, 4],
                         [5, 8, 11, 13, 13, 13, 13, 13, 13, 11, 8, 5],
                         [5, 8, 11, 13, 13, 13, 13, 13, 13, 11, 8, 5],
                         [4, 6, 8, 10, 10, 10, 10, 10, 10, 8, 6, 4],
                         [3, 4, 5, 7, 7, 7, 7, 7, 7, 5, 4, 3]]'''
    
    evaluation = np.sum(np.multiply(s, heuristique))
    return evaluation

#-------------------------------------------------
#MIN VALUE

#-------------------------------------------------------
def Min_Value(game: Connect4, current_depth: int, min_reward : int, max_reward : int, max_depth : int) -> tuple:
    if(game.terminal_Test()):
        victoire= -1 if game.step % 2 == game.posAi else 1
        if(victoire==1):
            return (1000 - current_depth), (game, min_reward, max_reward) #On prend en compte la profondeur
        elif(victoire==-1):
            return (current_depth - 1000), (game, min_reward, max_reward)
        else:
            return 0, (game, min_reward, max_reward)

        
    elif(current_depth >= max_depth):
        #INSERTION DE L'HEURISTIQUE
        #----------------------------
            return Heuristique(game.state.tolist(), game.heuristique), (game, min_reward, max_reward)
        #----------------------------
    else:

        current_depth += 1
        reward = 10000

        for action in Actions(game.state):
            exp_game = copy.deepcopy(game)
            exp_game.move(action)

            exp_reward, future = Max_Value(exp_game, current_depth, min_reward, max_reward, max_depth)
            reward= min(reward,exp_reward)
            if(reward <= min_reward): 
                return reward, (future[0], min_reward, max_reward)

            max_reward = min(max_reward, reward)

    return reward, (future[0], min_reward, max_reward)
#-------------------------------------------------------
#MAX VALUE

#-------------------------------------------------------
def Max_Value(game: Connect4, current_depth: int, min_reward: int, max_reward: int, max_depth: int) -> tuple:

    if(game.terminal_Test()):
        victoire= -1 if game.step % 2 == game.posAi else 1
        
        if(victoire==1):
            return (1000 - current_depth), (game, min_reward, max_reward) #On prend en compte la profondeur
        elif(victoire==-1):
            return (-1000 + current_depth), (game, min_reward, max_reward)
        else:
            return 0, (game, min_reward, max_reward)

    
    elif(current_depth >= max_depth):
        #INSERTION DE L'HEURISTIQUE
        #----------------------------
        return Heuristique(game.state.tolist(), game.heuristique), (game, min_reward, max_reward)
        #----------------------------
    else:
        current_depth += 1
        reward = -10000
        count = 0
        for action in Actions(game.state):
            exp_game = copy.deepcopy(game)
            exp_game.move(action)

            exp_reward, future = Min_Value(exp_game, current_depth, min_reward, max_reward, max_depth)
            reward = max(reward, exp_reward)
       
            if(reward >= max_reward ): return reward, (future[0], min_reward, max_reward)
            min_reward = max(min_reward, reward)
            
            count+=1
            
        
        return reward, (future[0], min_reward, max_reward)
#-------------------------------------------------------

def Get_best_actions(game : Connect4, possible_actions: list, pred_depth : int = 3):
    min_reward = - np.inf
    max_reward = np.inf

    bestValue= - np.inf

    top_actions = {}

    for action in possible_actions:
        exp_game = copy.deepcopy(game)
        #On regarde avec une profondeur 4
        exp_game.move(action)
        value, futureGame = Min_Value(exp_game, 0, min_reward, max_reward, pred_depth)

        #print("Value :", value," BestValue : ", bestValue)
 
        if(value > bestValue):
            top_actions.clear()
            bestValue = value
            top_actions[action] = futureGame

        elif(value == bestValue):
            top_actions[action] = futureGame
    
    return top_actions

def Get_needed_depth(step : int):
    return int(3 + 1 / (0.15 + np.exp(-0.3*(step - 40))))

def Alpha_Beta_Search(game : Connect4) -> int:
    
    if (game.step == 0):
        return game.board_size[1] // 2 - 1
    pred_depth = Get_needed_depth(game.step)
    top_actions = Get_best_actions(game, Actions(game.state), pred_depth = pred_depth)
     

    if(len(top_actions) > 1):
        #On va a 3 de plus de profondeur sur les top actions
        best_actions = []
        bestValue = - np.inf
        if(len(top_actions)<=6 and game.step >= 10):
            for action in list(top_actions.keys()):
                value, _ = Max_Value(top_actions[action][0], 4, top_actions[action][1], top_actions[action][2], pred_depth + 2)
                #print("Value2 :",value," BestValue2 : ",bestValue)
                
                if(value>bestValue):
                    best_actions.clear()
                    bestValue = value
                    best_actions.append(action)

                elif(value == bestValue):
                    best_actions.append(action)
                    
            top_actions = best_actions
        try:
            bestMove = list(top_actions.keys())[rand.randint(0,abs(len(top_actions)-1))]
        except:
            bestMove = top_actions[rand.randint(0,abs(len(top_actions)-1))]


    else:
        bestMove = list(top_actions.keys())[0]

    print("Best move (",pred_depth," steps) = ",bestMove + 1)
    return bestMove