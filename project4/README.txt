Sudoku solver using Constraint Satisfaction algorithms - AC3 and Backtracking

Submission score: 95%

I. Introduction

Consider the Sudoku puzzle. There are 81 variables in total, i.e. the tiles to be filled with digits. Each variable is named by its row and its column, and must be assigned a value from 1 to 9, subject to the constraint that no two cells in the same row, column, or box may contain the same value.

In designing your classes, you may find it helpful to represent a Sudoku board with a Python dictionary. The keys of the dictionary will be the variable names, each of which corresponds directly to a location on the board. In other words, we use the variable names Al through A9 for the top row (left to right), down to I1 through I9 for the bottom row. For example, in the example board above, we would have sudoku["B1"] = 9, and sudoku["E9"] = 8. This is the highly suggested representation, since it is easiest to frame the problem in terms of variables, domains, and constraints if you start this way. However, you can choose other data structures if you prefer. 
