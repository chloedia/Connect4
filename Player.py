import numpy as np
from AlphaBetaSearch import Alpha_Beta_Search
import time
class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        pass

    def isAi(self) -> bool:
        return False

    def action(self, game: object) -> int:
        return int(input(f'{self.name} which column do you want to play ? '))

class Agent(Player):
    def __init__(self, name:str = 'Super AI') -> None:
        super().__init__(name)

    def isAi(self) -> bool:
        return True
    
    def action(self, game: object) -> int:
        time_start = time.time()
        action = Alpha_Beta_Search(game)

        print("Temps d'execution : ", time.time() - time_start," secondes")
        return action + 1
