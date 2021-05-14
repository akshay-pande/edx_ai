from random import randint
from BaseAI import BaseAI
import math

import time

damp_factor = 0.3 #damp factor for second part of util. function
damp_factor_mono = 0.2
max_depth = 6
timeLimit = 0.19

class PlayerAI(BaseAI):
    
    def getMove(self, grid):       
        
        self.startTime = time.clock()
        action_val = self.minimax(grid, 0)        
        return action_val[0]    
    
    def getCornerBonus (self,grid, maxTile):
        
        for i in range(0,4):
            if grid.map[3][3] == maxTile:
                return 8.0
            elif grid.map[3][0] == maxTile:
                return 3.0            
            elif grid.map[3][1] == maxTile or grid.map[3][2] == maxTile:
                return 1.0        
        return 0    
    
    def getTileValOccurences(self, grid):
        tile_dict = {}        
        
        for x in range(grid.size):
            for y in range(grid.size):
                tile_val = grid.map[x][y]                
                if tile_val != 0:
                    if tile_val not in tile_dict:
                        tile_dict[tile_val] = 1
                    else:
                        tile_dict[tile_val] += 1

        return tile_dict
    
    def getMonoScore(self, grid):        #monotonicity score
        mono_score = 0
        prev_val = grid.map[0][0]
        tile_val = prev_val
        
        for x in range(grid.size):
            for y in range(grid.size):
                prev_val = tile_val
                tile_val = grid.map[x][y]
                if tile_val >= prev_val and tile_val != 0:
                    mono_score += math.sqrt(tile_val)*((y/2)**4)*((x/2)**3)
                else:
                    break
        return mono_score*damp_factor_mono    

    def utility(self, grid):
        """
        This is based on
        U(grid) = N(empty cells) * (sqrt(max_tile)  + cornerbonus)
                    sum(number of occurences of tile * log2(tile value)*tile value * damp factor)

        the first part gives weight to empty cells or corners having the maxtile,         
        where more weight is given if the max tile value is higher (as empty cells are then more valuable)
        the second part scores each tile on the grid, giving more weight to higher value tiles
        the no. of occurences is important but not important enough hence the sqrt
        """
        tile_dict = self.getTileValOccurences(grid)
        n_empty_cells = len(grid.getAvailableCells())
        max_tile = grid.getMaxTile()  
        corner_bonus = self.getCornerBonus(grid, max_tile)  
        mono_score = self.getMonoScore(grid)
        
        output = math.sqrt(max_tile) * (n_empty_cells + corner_bonus + mono_score)

        for key in tile_dict.keys():        
            output += math.log(key,2)*key*tile_dict[key]*damp_factor

        return output

    def terminalTest(self, grid):
        if len(grid.getAvailableCells()) == 0:
            return True        
        return False

    def minimax(self, grid, depth):              
        return self.maximize(grid, 0, 0, float('-inf'), float('inf'))     
                      
    def maximize(self, grid, depth, action, alpha, beta):

        if(self.terminalTest(grid) or depth > max_depth or (time.clock() - self.startTime) >= timeLimit ):                       
            return(action, self.utility(grid))
        
        max_action = action
        maxval = -1
        depth += 1 
        
        for i in [1,2,3]:                         
            grid_copy = grid.clone()
            grid_copy.move(i)                
            val = self.minimize(grid_copy, depth, i, alpha, beta)
            if(val[1] > maxval) :
                maxval = val[1]
                max_action = i
            alpha = max (maxval, alpha)
            if alpha >= beta:
                break
            
        return (max_action, maxval)
   
    def minimize(self, grid, depth, action, alpha, beta):
        if(self.terminalTest(grid)  or depth > max_depth or (time.clock() - self.startTime) >= timeLimit):                      
            return(action, self.utility(grid))

        available_cells = grid.getAvailableCells()
        depth += 1    
        minval = float('inf')
        
        if beta > alpha:
            grid_copy = grid.clone()        
            grid_copy.setCellValue(available_cells[randint(0,len(available_cells)-1)],2)            
            val_2 = self.maximize(grid_copy, depth, action, alpha, beta)       
            grid_copy = grid.clone()
            grid_copy.setCellValue(available_cells[randint(0,len(available_cells)-1)],4)
            val_4 = self.maximize(grid_copy, depth, action, alpha, beta)       
            
            minval = min(val_2[1], val_4[1], minval)
            beta = min(minval, beta)            

        return (action, minval)
                    






        
        

    
    



        
        



        
        
            
            
