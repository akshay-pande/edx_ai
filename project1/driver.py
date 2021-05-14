import math
import collections
import heapq as h
import sys
import time
import tracemalloc   

class PuzzleBoard:
    """Class to store and work with the puzzle board"""
    
    def __init__ (self, puzzle_list:list, parent:str="", move:str="" ,n:int=-1) -> None:     
        
        if n == -1 :
            n = int(math.sqrt(len(puzzle_list)))

        self.size = n
        self.parent = parent        #parent is the board from which this was created
        self.move_str = move
            
        length = len(puzzle_list)
        self.board = [[0 for i in range (n)] for j in range (n)]
        
        index = 0
        for num in puzzle_list:
            self.board[int(index/n)][int(index % n)] = num
            if num == 0:
                self.row_of_blank = int(index/n)
                self.col_of_blank = int(index % n)
                self.index_of_blank = index                
                                        
            index = index + 1

    def __str__(self) -> None:
        strout = ""        
        for i in range(self.size):
            strout += "" + str(self.board[i]) + '\n'            
        return strout

    def convert_to_list(self) -> list:
        result_list = []
        for i in range(0,self.size):
            for val in self.board[i]:
                result_list.append(val)

        return result_list        
    
    def convert_to_string(self) -> str:
        result_string = ""
        for i in range(0,self.size):
            for val in self.board[i]:
                result_string += str(val)
        return result_string
                        

    def no_of_moves(self) -> int:
        #no. of valid moves for the current blank tile
        
        n = self.size
        if (self.row_of_blank == 0 or self.row_of_blank == (n-1)) and (self.col_of_blank == 0 or self.col_of_blank == (n-1)):
            return 2
        elif (self.row_of_blank == 0 or self.row_of_blank == (n-1)) or (self.col_of_blank == 0 or self.col_of_blank == (n-1)):
            return 3
        else:
            return 4

        return -1

    def valid_index(self, row:int, col:int) -> bool:
        #check if a row,col is valid
        
        if row >= 0 and row < self.size and col >= 0 and col < self.size:
            return True
        else:
            return False

    def swap_tiles(self, x:int, y:int) -> None:
        #swap blank tile with a neighbour
        
        n = self.size

        self.board[self.row_of_blank][self.col_of_blank] = self.board[x][y]
        self.board[x][y] = 0

        self.row_of_blank = x
        self.col_of_blank = y
        self.index_of_blank = n*x+y    

    def move(self, direction:str) -> bool:
        #move's the tile on the class's board, updates the board
        if direction == "up":
            if self.valid_index(self.row_of_blank-1, self.col_of_blank):
                self.swap_tiles(self.row_of_blank-1, self.col_of_blank)
                return True
        elif direction == "down":
            if self.valid_index(self.row_of_blank+1, self.col_of_blank):
                self.swap_tiles(self.row_of_blank+1, self.col_of_blank)
                return True
        elif direction == "left":
            if self.valid_index(self.row_of_blank, self.col_of_blank-1):
                self.swap_tiles(self.row_of_blank, self.col_of_blank-1)
                return True
        elif direction == "right":
            if self.valid_index(self.row_of_blank, self.col_of_blank+1):
                self.swap_tiles(self.row_of_blank, self.col_of_blank+1)
                return True
        
        #not a valid move
        return False

    def generate_move_state(self, direction:str) -> list:
        #returns the possible move state as a list
        if direction == "up":
            if self.valid_index(self.row_of_blank-1, self.col_of_blank):
                self.swap_tiles(self.row_of_blank-1, self.col_of_blank)
                return True
        elif direction == "down":
            if self.valid_index(self.row_of_blank+1, self.col_of_blank):
                self.swap_tiles(self.row_of_blank+1, self.col_of_blank)
                return True
        elif direction == "left":
            if self.valid_index(self.row_of_blank, self.col_of_blank-1):
                self.swap_tiles(self.row_of_blank, self.col_of_blank-1)
                return True
        elif direction == "right":
            if self.valid_index(self.row_of_blank, self.col_of_blank+1):
                self.swap_tiles(self.row_of_blank, self.col_of_blank+1)
                return True
        
        #not a valid move
        return False

    def goal_test(self) -> bool:
        blist = self.convert_to_list()        
        index = 0
        for num in blist:
            if blist[index] != index:
                return False
            index = index + 1
        return True

    def heur_cost(self) -> int:
        n = self.size
        value = 0        
        goal_x = 0
        goal_y = 0
        heur_cost = 0
        for i in range(0,n):
            for j in range(0,n):
                value = self.board[i][j]
                
                if value > 0 :
                    goal_x = value // n
                    goal_y = value % n                    
                    heur_cost += abs(goal_x-i) + abs(goal_y-j)

        return heur_cost
                
    
class Solver:   
        
    def __init__ (self, pb_list:list) -> None:
        self.initial_board = PuzzleBoard(pb_list)        
         

    def initialise(self) -> None:
        print("running...")
        tracemalloc.start()
        self.start_time = time.time()
        self.frontier_deq = collections.deque([self.initial_board.convert_to_string()])             #for dfs
        self.frontier_dict = {self.initial_board.convert_to_string():self.initial_board}            #for bfs        
        self.heap_dict =  {self.initial_board.heur_cost():self.initial_board.convert_to_string()}   #for ast
        self.heap_list = list(self.heap_dict.items())                                               #for ast
        h.heapify(self.heap_list)                                                                        #for ast

        self.explored_dict = {}
        self.result_moves = []
        self.max_search_depth = 0
        

    def solved_stats(self, nodestring:str) -> None:
        print("solved")        
        search_depth = 0
        moves_list = []
        moves_list.append(self.frontier_dict[nodestring].move_str)
        self.result_moves.append(nodestring)
        parentstring = self.frontier_dict[nodestring].parent
     
        while parentstring is not "":
            self.result_moves.append(parentstring)
            search_depth += 1
            parent_node = self.explored_dict[parentstring]
            parentstring = parent_node.parent            
            if parent_node.move_str != '' :
                moves_list.append(parent_node.move_str)            
        
        last_node = self.dict_local_states[list(self.dict_local_states)[0]]        
        tree_dict = {**self.explored_dict, **self.frontier_dict}   #combine all the nodes to get the full tree       
        parentstring = last_node.parent

        while parentstring is not "":
            self.max_search_depth += 1            
            parentstring = tree_dict[parentstring].parent

        moves_list.reverse()
        moves_string = '['
        for item in moves_list:
            moves_string += "\'" + item + "\'," 

        moves_string = moves_string[:-1] + ']'
        current, peak = tracemalloc.get_traced_memory()     
        file = open("output.txt", "w")
        file.write("path_to_goal: " + moves_string)
        file.write("\ncost_of_path: " + str(search_depth))
        file.write("\nnodes_expanded: " + str(len(self.explored_dict)))
        file.write("\nsearch_depth: " + str(search_depth))
        file.write("\nmax_search_depth: " + str(self.max_search_depth))
        file.write("\nrunning_time: %s" % str((time.time() - self.start_time)))
        file.write(f"\nmax_ram_usage: {peak/10**6}")
        file.close()
        tracemalloc.stop()

    def bfs(self) -> None:        
        
        self.initialise()
        index_first_in_frontier = next(iter(self.frontier_dict))        

        while not self.frontier_dict[index_first_in_frontier].goal_test():          
            
            current_node = self.frontier_dict[index_first_in_frontier]
            current_node_puzzlelist = current_node.convert_to_list()            
            
            self.dict_local_states = {"up": PuzzleBoard(current_node_puzzlelist, index_first_in_frontier, 'Up'),
                                 "down": PuzzleBoard(current_node_puzzlelist, index_first_in_frontier, 'Down'),
                                 "left": PuzzleBoard(current_node_puzzlelist, index_first_in_frontier, 'Left'),
                                 "right": PuzzleBoard(current_node_puzzlelist, index_first_in_frontier, 'Right')}
            
            for key, board in self.dict_local_states.items():
                board.move(key)
                boardstring = board.convert_to_string()
                
                if boardstring not in self.frontier_dict and boardstring not in self.explored_dict:
                    self.frontier_dict[boardstring] = board       #add node to the frontier
                   
            
            #remove current node from frontier            
            
            self.explored_dict[index_first_in_frontier] = current_node
            self.frontier_dict.pop(index_first_in_frontier)            
            index_first_in_frontier = next(iter(self.frontier_dict))

        #solution is found
        self.solved_stats(index_first_in_frontier)
        
        
    def dfs(self) -> None:        
        
        self.initialise()        
        current_nodestring = self.frontier_deq.popleft()
        
        while not self.frontier_dict[current_nodestring].goal_test():            
            
            #expand node and add children to frontier
            
            current_node = self.frontier_dict[current_nodestring]
            current_node_puzzlelist = current_node.convert_to_list()            
            
            self.dict_local_states = {"right": PuzzleBoard(current_node_puzzlelist, current_nodestring, 'Right'),
                                 "left": PuzzleBoard(current_node_puzzlelist, current_nodestring,'Left'),
                                 "down": PuzzleBoard(current_node_puzzlelist, current_nodestring,'Down'),
                                 "up": PuzzleBoard(current_node_puzzlelist, current_nodestring,'Up')}
            
            for key, board in self.dict_local_states.items():
                board.move(key)
                boardstring = board.convert_to_string()
                
                if boardstring not in self.explored_dict and boardstring not in self.frontier_dict:
                    self.frontier_deq.appendleft(boardstring)
                    self.frontier_dict[boardstring] = board       #add node to the unordered frontier, for storage and retrieval
                    
            #remove current node from frontier                        
            self.explored_dict[current_nodestring] = current_node
            self.frontier_dict.pop(current_nodestring)                        
            current_nodestring = self.frontier_deq.popleft()

        #solution is found        
        self.solved_stats(current_nodestring)

    def ast(self) -> None:
        
        self.initialise()  
        min_in_frontier = h.heappop(self.heap_list)        

        while not self.frontier_dict[min_in_frontier[1]].goal_test():            
            
            #expand node and add children to frontier                
            
            curr_cost = min_in_frontier[0]
            current_node = self.frontier_dict[min_in_frontier[1]]
            current_node_puzzlelist = current_node.convert_to_list()            
            
            self.dict_local_states = {"up": PuzzleBoard(current_node_puzzlelist, min_in_frontier[1],'Up'),
                                 "down": PuzzleBoard(current_node_puzzlelist, min_in_frontier[1],'Down'),
                                 "left": PuzzleBoard(current_node_puzzlelist, min_in_frontier[1], 'Left'),
                                 "right": PuzzleBoard(current_node_puzzlelist, min_in_frontier[1],'Right')}
            
            for key, board in self.dict_local_states.items():
                step_cost = 1
                board.move(key)
                boardstring = board.convert_to_string()
                
                if boardstring not in self.frontier_dict and boardstring not in self.explored_dict:
                    #add node to frontier
                    curr_path_cost = min_in_frontier[0] - current_node.heur_cost()
                    self.frontier_dict[boardstring] = board                             
                    h.heappush(self.heap_list, (curr_path_cost+board.heur_cost()+step_cost,boardstring))
            
            #remove current node from frontier            
            
            self.explored_dict[min_in_frontier[1]] = current_node
            self.frontier_dict.pop(min_in_frontier[1])            
            min_in_frontier = h.heappop(self.heap_list)
            

        #solution is found
       
        self.solved_stats(min_in_frontier[1])
    
    
def main(argv):
    func_name = argv[1]
    input_list_str = argv[2].split(',')
    input_list = [int(i) for i in input_list_str]
    s = Solver(input_list)

    if(func_name=='bfs'):
        s.bfs();
    elif(func_name == 'dfs') :
        s.dfs();
    else:
        s.ast();        

if __name__ == "__main__":
    main(sys.argv)
        
