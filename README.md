<h1 align="center">Connect 4</h1>
<p align="center">Program using Game theory (MinMax algorithm) on Connect4, try to beat it if you dare 🤓 </p>
<div align="center">
<img width = 200 alt="Connect4" src="https://www.pinclipart.com/picdir/big/196-1966405_a-rare-disease-as-defined-by-the-european.png">
</div>

## Environment 🌎
  Our Connect 4 game is using the mainstream rules of a Connect 4, this is a two players games where each player can place one coin in the column of their choice in turn. The goal is to **align four** of your coins along the **horizontal axis**, **the vertical axis** or on **any diagonal** of the grid. The little twist of our project is that it is **adaptable to any grid size** with the constraint of the number of columns and lines being at least 4.

<div align="center">
<img title = "UI of the Connect4" width = 400 alt="Connect4" src="Connect4.png">
</div>

This projet was realized for the 1st year course **"Introduction to AI and data science"** of *Ecole Superieur Léonard de Vinci (ESILV)*.

## Implementation 🧠
**AI Rules**
Possible actions : $A = {1,2, ..., n_columns}$
Rewards : **Win** = + 1000 - depth ; **Loss** = - 1000 + depth

**MinMax algorithm**

  The MinMax algorithm is well know in **Game theory**, to describe it rapidly we can stick it to the Connect 4 which is a sequential game meaning that at each step (the player plays a coin) there is a new state. Hence, the goal of the minmax algorithm is simply to find the move that will **maximize your possible reward and next step maximize the possible reward of the oppenent** (So minimize yours). To do so, it will iterate threw all your possible actions and go on on multiple steps that we wll call depth until reaching eather a final reward or a maximum depth.
To optimize the algorithm, we also use the alpha beta pruning method to stop predicting for actions that are considered too bad.
To know more about minimax algorithm and alpha beta pruning don't hesitate to check this <a href= https://medium.com/swlh/optimizing-decision-making-with-the-minimax-ai-algorithm-69cce500c6d6>article</a>.

**Heuristic**

As the board can provide too many possibilities of actions, the time complexity for the MiniMax algorithm is too high and we are forced to use an **heuristic**. An heuristic is simply a score that you give to a given state of the game, this is what the minimax will compute after diving on a defined depth. We chose quite a simple to compute heuristic a we use an evaluation grid which is fixed at the begining of the game and depends on the size of the grid. Each cell is assigned a value which corresponds to the number of possible alignments it is oppened to, for exemple :







