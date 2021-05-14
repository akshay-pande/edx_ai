import sys
sys.setrecursionlimit(100000)

limits = [[0,3],[3,6],[6,9]]
default_domain = set([1,2,3,4,5,6,7,8,9])
file_out = open("output.txt","w")


class SudokuGrid:    

    def __init__(self, numlist:str) : 
        self.str = numlist
        self.grid = [[0*i for i in range(0,9)] for i in range(0,9)]
        self.domains = dict()
        cellval = 0
        if len(numlist) >= 81 :
            for i in range (0,9):                
                for j in range(0,9):
                    cellval = int(numlist[9*i+j])
                    
                    self.grid[i][j] = cellval
                    if cellval != 0 :
                        self.domains['x'+str(i)+str(j)] = set([cellval])
                    else:
                        self.domains['x'+str(i)+str(j)] = set([1,2,3,4,5,6,7,8,9])
        return

    def __str__(self):
        outputstr = "|"
        for i in range(0,9):
            if i > 0:
                outputstr+= "\n|"
            for j in range(0,9):
                outputstr += str(self.grid[i][j])+"|"
        return outputstr
    
    def getString(self):
        outputstr = ""
        for i in range(0,9):            
            for j in range(0,9):
                outputstr += str(self.grid[i][j])
        return outputstr
    
    def getBoxLimits(self, box_id:int=0, cell=None):
        row_limit = []
        col_limit = []
        if box_id > 0 and box_id < 10:
            row_limit = limits[(box_id-1)//3]
            col_limit = limits[(box_id-1)%3]
        elif cell is not None:
            for limit in limits:
                if cell[0] >= limit[0] and cell[0] <= limit[1] :
                    row_limit = limit                    
                if cell[1] >= limit[0] and cell[1] <= limit[1] :
                    col_limit = limit                    
        
        box_limits = {'row': row_limit, 'col':col_limit}
        
        return box_limits

    
    def getBox(self, box_id:int=0, cell=None):        
        
        rc_limits = self.getBoxLimits(box_id=box_id, cell=cell)
        row_limit = rc_limits['row']
        col_limit = rc_limits['col']
        
        output_box = self.grid
        
        output_box = output_box[row_limit[0]:row_limit[1]]

        for row in range(0,len(output_box)):
            output_box[row] = output_box[row][col_limit[0]:col_limit[1]]

        return output_box

    def getCellVal(self, cell=None, cell_id=None):
        if cell is not None:
            return self.grid[cell[0]][cell[1]]
        else:
            return self.grid[int(cell_id[1])][int(cell_id[2])]
    
    def getDomain(self, cell_id):
        return self.domains[cell_id]
    
    def createArcSet(self):
        """ by default every pair in the arc signifies a *not equal to* relation"""
        arcset = set()
        for row in range(0,9):
            for col in range(0,9):
                if self.grid[row][col] == 0:      #current empty cell
                    for cur_col in range(0,9):
                        if cur_col != col:
                            arcval = ("x"+str(row)+str(col), "x"+str(row)+str(cur_col))
                            arcval_mirror = ("x"+str(row)+str(cur_col), "x"+str(row)+str(col))
                            arcset.add(arcval)     #add row constraint
                            arcset.add(arcval_mirror)
                            
                    for cur_row in range(0,9):
                        if cur_row != row:
                            arcval = ("x"+str(row)+str(col), "x"+str(cur_row)+str(col))
                            arcval_mirror = ("x"+str(cur_row)+str(col), "x"+str(row)+str(col))
                            arcset.add(arcval)     #add column constraint
                            arcset.add(arcval_mirror)
                    box_limits = self.getBoxLimits(cell=(row,col))
                    for box_row in range(box_limits['row'][0],box_limits['row'][1]):
                        for box_col in range(box_limits['col'][0],box_limits['col'][1]):
                            if box_col!=col and box_row!=row:
                                arcval = ("x"+str(row)+str(col), "x"+str(box_row)+str(box_col))
                                arcval_mirror = ("x"+str(box_row)+str(box_col), "x"+str(row)+str(col))
                                arcset.add(arcval)     #add box constraint    
                                arcset.add(arcval_mirror)                
        return arcset
    
    def getCellsForArc(self, arc):
        """an arc is a tuple in the form (x##, x##)"""
        cell1 = self.convertIDtoTuple(arc[0])
        cell2 = self.convertIDtoTuple(arc[1])
        return (cell1),(cell2)
    
    def checkSolved(self):
        solved = True
        for key in self.domains.keys():
            
            if len(self.domains[key]) > 1 :
                solved = False
            elif len(self.domains[key]) == 1:
                (row,col) = self.convertIDtoCell(key)
                self.grid[row][col] = next(iter(self.domains[key]))
            else:
                return -1              
                    
        return solved         
    
    def printSolution(self):
        output = ""
        
        if(self.checkSolved):
        
            for row in range(0,9):
                for col in range(0,9):
                    output += str(self.grid[row][col])

        return output

    def goalTest(self):
        rowset = set()
        colset = set()
        boxset = set()
        box = []
        
        #check rows 
        for row in range(0,9):            
            if row > 0:
                if len(rowset) < 9:
                    return False
            rowset.clear()
            for col in range(0,9):
                if self.grid[row][col] != 0:
                    rowset.add(self.grid[row][col])
        
        #check columns
        for col in range(0,9):            
            if col > 0:
                if len(colset) < 9:
                    return False
            colset.clear()
            for row in range(0,9):
                if self.grid[row][col] != 0:
                    colset.add(self.grid[row][col])
        
        #check box
        for i in range(1,10):
            if i > 1 :
                if len(boxset) < 9:
                    return False
            box = self.getBox(i)
            boxset.clear()

            for full_row in box:
                for val in full_row:
                    if val != 0:
                        boxset.add(val)
        
        return True

    def getNextEmptyCell(self):
        empty_cell_ids = []
        min_dom_length = 9
        min_id = ""
        for row in range(0,9):
            for col in range(0,9):
                if self.grid[row][col] == 0:
                    id = 'x'+str(row)+str(col)
                    domain_length = len(self.domains[id])
                    if domain_length < min_dom_length:
                        min_dom_length = domain_length
                        min_id = id
        if min_id != "":
            return min_id
        
        return False
    
    def checkConsistency(self, cell, val):
        cell_row = cell[0]
        cell_col = cell[1]

        for row in range(0,9):
            if self.grid[row][cell_col] == val:
                return False

        for col in range(0,9):
            if self.grid[cell_row][col] == val:
                return False
        
        box = self.getBox(cell=cell)
        for full_row in box:
            for curr_val in full_row:
                if curr_val==val:
                    return False
        
        return True

    def convertIDtoCell(self, cell_id):
        return (int(cell_id[1]), int(cell_id[2]))
    
   
class Solver:

    def __init__(self):
        return 
    
    def checkConstraint(self, val, Dj):
        for val_j in Dj:
            if val_j != val:        #at least 1 value in Dj satisfies the constraint that x != y
                return True
        return False
    
    def revise(self,sgrid:SudokuGrid, Xi, Xj):
       
        revised = False

        Di = set()
        Dj = set()
        Di = sgrid.getDomain(Xi)
        Dj = sgrid.getDomain(Xj)
        
        cellval1 = sgrid.getCellVal(cell_id=Xi)
        cellval2 = sgrid.getCellVal(cell_id=Xj)
        remove_these = []
        
        for val in Di:
            if not(self.checkConstraint(val, Dj)):      #contraint failed
                remove_these.append(val)
                revised=True
        for val in remove_these:
            Di.remove(val)
              
        sgrid.domains[Xi] = Di
        new_domain = str(sgrid.getDomain(Xi))
       
        return revised

    def getNeighbours(self, arcset, cur_arc):
        neighbour_cells = []
        Xi = cur_arc[0]
        for arc in arcset:
            if Xi in arc:
                nbr = ""
                if Xi != arc[0]:
                    nbr = arc[0]
                else:
                    nbr = arc[1]
                if nbr != cur_arc[1]:
                    neighbour_cells.append(nbr)
        return_set = set()
        for nbr in neighbour_cells:
            new_arc = (nbr, Xi)
            return_set.add(new_arc)
            new_arc = (Xi, nbr)
            return_set.add(new_arc)
        return return_set


    def ac3(self, sgrid:SudokuGrid):
        
        rval = False
        arcset = sgrid.createArcSet()             
      
        while len(arcset) > 0 :

            cur_arc = arcset.pop()            

            if self.revise(sgrid, cur_arc[0], cur_arc[1]):
                
                if len(sgrid.getDomain(cell_id=cur_arc[0])) == 0 :                    
                    return False
                neighbours = self.getNeighbours(arcset, cur_arc)                
                arcset.update(neighbours)
                
        return True

    def backtracking(self, sgrid:SudokuGrid):
        self.ac3(sgrid) 
        if sgrid.checkSolved():     #if not solved, this function fills the cells where single values were found
            return sgrid        
        
        return self.backtrack(sgrid)
    
    def backtrack(self, sgrid:SudokuGrid):

        if sgrid.goalTest():
            return sgrid
        
        cell_id = sgrid.getNextEmptyCell()                        
            
        grid_copy = SudokuGrid(sgrid.getString())        
            
        if cell_id != False:     #empty cells still exist
            cell = sgrid.convertIDtoCell(cell_id)

            for val in sgrid.domains[cell_id]:                                                            
                    
                #check basic consistency                          
                if grid_copy.checkConsistency(cell,val):
                    grid_copy.grid[cell[0]][cell[1]] = val  #add value to grid                        
                    self.ac3(grid_copy)                        
                    grid_copy.checkSolved()        
                    result = self.backtrack(grid_copy)
                    if result != False:
                        return result                        
            
        return False


def main():    

    s = Solver()      
    grid = SudokuGrid(sys.argv[1])          
   
    s.ac3(grid)
    if grid.checkSolved() == True:
        file_out.writelines(grid.printSolution()+" AC3")
    
    output_grid = s.backtracking(grid)    
    
    file_out.writelines(output_grid.printSolution()+" BTS")        
    
    file_out.close() 
    

if __name__ == "__main__":
    main()

