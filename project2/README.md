Creating an intelligent playing agent for the 2048 game using minimax algorithm and alpha-beta pruning

The algorithm reached 2048 in 40% of the trials, 1024 in 50% 

The PlayerAI.py file was created by me, the remaining files were provided as skeleton code in the assignment

I. Introduction

An instance of the 2048-puzzle game is played on a 4×4 grid, with numbered tiles that slide in all four directions when a player moves them. Every turn, a new tile will randomly appear in an empty spot on the board, with a value of either 2 or 4. Per the input direction given by the player, all tiles on the grid slide as far as possible in that direction, until they either (1) collide with another tile, or (2) collide with the edge of the grid. If two tiles of the same number collide while moving, they will merge into a single tile, valued at the sum of the two original tiles that collided. The resulting tile cannot merge with another tile again in the same move.

  
The focus was strictly on the ground-level details of the algorithms. All the skeleton code necessary to get started, was provided.

With typical board games like chess, the two players in the game (i.e. the "Computer AI" and the "Player") take similar actions in their turn, and have similar objectives to achieve in the game. In the 2048-puzzle game, the setup is inherently asymmetric; that is, the computer and player take drastically different actions in their turns. Specifically, the computer is responsible for placing random tiles of 2 or 4 on the board, while the player is responsible for moving the pieces. However, adversarial search can be applied to this game just the same.
