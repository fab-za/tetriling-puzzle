# ####################################################
# DE2-COM2 Computing 2
# Individual project
#
# Title: MAIN
# Author: Farzana Zainal Abidin
# CID: 01539750
# ####################################################

def Tetris(target):
    
    # --------------------- defining sub functions of algorithm ----------------------------------
    
    # checks whether coordinate is within bounds of target matrix
    def within(r,c): 
        if r > r_total-1 or r < 0:
            return False                                                             # out of bounds
        if c > c_total-1 or c < 0:
            return False                                                             # out of bounds
        return True                                                                  # within bounds
    
    # creates matrices based on adjacent blocks (neighbours), used to decide which direction to 'walk' when building a shape
    def adjacents():
        rel_coord = [(1, 0),(0, 1),(0, -1),(-1, 0)]                                  # down, right, left, up
        for r in range(r_total):                                                     # row
            for c in range(c_total):                                                 # column
                if target[r][c] == 1:                                                # find every instance of 1 (a shape)
                    coordinates = []                                                 # empty list for coordinates of adjacent blocks at this position (adjacency list)
                    
                    for i in rel_coord:
                        r_adj = r + i[0]                                             # add directions
                        c_adj = c + i[1]
                    
                        if not within(r_adj,c_adj):                                  # if it is not within the bounds of the matrix
                            continue
                        
                        if target[r_adj][c_adj] == 1:                                # if there is an adjacent block
                            coordinates.append((r_adj,c_adj))                        # append coordinates of adjacent into list
                            num_adj[r][c] += 1                                       # add one to number of adjacents at this position
                    
                    coord_adj[r][c] = coordinates                                    # replace with adjacency list at position
        
        return coord_adj, num_adj                                                    # returns two matrices
    
    # finds shapeID of given shape relative coordinates
    def fetch_shapeID(shape):
        
        for shapeID, val in shape_dict.items():                                      # check if shape exists in dictionary of shapes
            if val == shape: 
                return shapeID                                                       # returns integer
    
    # updates values in solution matrix for solution (ie places shape in solution matrix)
    # updates values in target matrix as a shape has been placed (therefore a shape does not need to be found at this position again)
    def place_shape(shape_pos,solution,pieceID):
        
        okay = 0                                                                     # initialise check whether it is 'okay' to place a shape
        shape_coord = sorted(shape_pos)                                              # sort in order bc shape positions may not have been appended in order

        shape = []                                                                   # list of relative coordinates of shape construction to (0,0) starting position
        start_r,start_c = shape_coord[0]
        
        for m in range(4):
            if m != 0:                                                               # ignore the first coordinate because it will always be taken as (0,0)
                shape.append((shape_coord[m][0] - start_r, shape_coord[m][1] - start_c)) # eg [(0,1),(0,2),(1,0)]
            if solution[shape_coord[m][0]][shape_coord[m][1]] == (0,0):              # a shape has not been placed 
                okay += 1                                                            # therefore it is 'okay' to place a new shape there

        shapeID = fetch_shapeID(shape)                                               # call function to find shapeID
        
        if shapeID > 3 and okay == 4:                                                # disregard forbidden shapes and make sure that all 4 blocks within shape are 'okay' to place
            pieceID += 1                                                             # counter for what number piece is being placed
            for n in range(4):
                solution[shape_coord[n][0]][shape_coord[n][1]] = (shapeID,pieceID)   # place shape in solution matrix
                target[shape_coord[n][0]][shape_coord[n][1]] = 0                     # convert target matrix value at position from 1 into 0
                
        return solution, pieceID # returns solution matrix and pieceID (counter)
    
    # finds a shape by walking a path (traversal by connected component), direction prioritised by *lowest number of adjacent blocks* of adjacent blocks
    # iterates recursively to find four coordinates of blocks to create the shape positions
    # once a path of 4 blocks has been travesed, immediately returns that shape, therefore is a greedy algorithm
    # does not allow for excess blocks but can lead to missing blocks due to incomplete paths or forbidden shape paths
    def find_shape(coord_adj, num_adj, r, c):
        
        pos = (r,c)                                                                  # (coordinate of) position
        shape_pos.append(pos)                                                        # append coordinate into list of shape positions
        
        for coord in coord_adj[r][c]:                                                # for every coordinate in list of adjacent coordinates at position
            r_c,c_c = coord                                                          # unpack rows,columns
            
            if pos in coord_adj[r_c][c_c]:
                coord_adj[r_c][c_c].remove(pos)                                      # remove coordinate of position from list of adjacent coordinates
                num_adj[r_c][c_c] -= 1                                               # number of adjacents at position decreases by 1
        
        while len(shape_pos) < 4:                                                    # while all 4 blocks of a shape have yet to be found
            r_best = None                                                            # set as None every time a position is tested
            prev_n_adj = None

            for coord in coord_adj[r][c]:
                r_c,c_c = coord

                if coord not in shape_pos:                                           # if coordinate has not been chosen before
                    
                    if prev_n_adj is None or num_adj[r_c][c_c] < prev_n_adj:         # if this is the first iteration of a coordinate of an adjacent at this position
                                                                                     # or if the number of adjacents at this position is less than the number of adjacents of the previous iteration
                        r_best = r_c                                                 # best suited row index
                        c_best = c_c                                                 # best suited column index
                        prev_n_adj = num_adj[r_c][c_c]                               # update number of adjacents of previous iteration
            
            if r_best is not None:                                                   # if the best suited coordinate has been found
                find_shape(coord_adj, num_adj, r_best, c_best)                       # recurse back to find the next block
            
            else:                                                                    # for cases where less than four adjacent blocks are left
                break
        
        return coord_adj, num_adj, shape_pos                                         # return updated matrices for next call, return positions of shape for placing
    
    # ------------------- initialising initial global variables, those that only need to be initialised once -------------------------
    
    r_total = len(target)                                                            # number of rows
    c_total = len(target[0])                                                         # number of columns
    solution = [[(0,0) for c in range(c_total)] for r in range(r_total)]             # empty solution matrix
    coord_adj = [[0 for c in range(c_total)] for r in range(r_total)]                # empty matrix for adjacency lists
    num_adj = [[0 for c in range(c_total)] for r in range(r_total)]                  # empty matrix for number of adjacent blocks
    pieceID = 0                                                                      # counter for pieces
    
    shape_dict = {                                                                   # dictionary of shapes
    1: [(0, 1), (1, 0), (1, 1)],
    2: [(1, 0),(2, 0),(3, 0)],
    3: [(0, 1),(0, 2),(0, 3)],
    4: [(1, 0), (2, 0), (2, 1)],
    5: [(1, -2), (1, -1), (1, 0)],
    6: [(0, 1), (1, 1), (2, 1)],
    7: [(0, 1), (0, 2), (1, 0)],
    8: [(1, 0), (2, -1), (2, 0)],
    9: [(0, 1), (0, 2), (1, 2)],
    10: [(0, 1), (1, 0), (2, 0)],
    11: [(1, 0), (1, 1), (1, 2)],
    12: [(1, 0), (1, 1), (2, 0)],
    13: [(1, -1), (1, 0), (1, 1)],
    14: [(1, -1), (1, 0), (2, 0)],
    15: [(0, 1), (0, 2), (1, 1)],
    16: [(0, 1), (1, -1), (1, 0)],
    17: [(1, 0), (1, 1), (2, 1)],
    18: [(0, 1), (1, 1), (1, 2)],
    19: [(1, -1), (1, 0), (2, -1)]
    }
        
    # -------------------- main code where sub functions are called -----------------------------
    
    coord_adj, num_adj = adjacents()                                                # create matrices of adjacents

    for r in range(r_total):
        for c in range(c_total):
            
            if target[r][c] == 1:                                                   # find the topmost leftmost instance of 1 as starting position
                
                shape_pos = []                                                      # initialise empty list for shape positions
                
                coord_adj, num_adj, to_place = find_shape(coord_adj, num_adj, r, c) # call function to find shape

                if len(to_place) == 4:                                              # if list of shape positions is 4, proceed to place
                    solution, pieceID = place_shape(to_place,solution,pieceID)      # place that shape
    
                                                                                    # run through target a second time for increased accuracy by up to 2%
    coord_adj, num_adj = adjacents()                                                # update adjacency with remaining blocks left
    
    for r in range(r_total):
        for c in range(c_total):
            
            if target[r][c] == 1:                                                   # find the topmost leftmost instance of 1 as starting position
                
                shape_pos = []                                                      # initialise empty list for shape positions
                
                coord_adj, num_adj, to_place = find_shape(coord_adj, num_adj, r, c) # call function to find shape
                
                if len(to_place) == 4:                                              # if list of shape positions is 4, proceed to place
                    solution, pieceID = place_shape(to_place,solution,pieceID)      # place that shape

    return solution                                                                 # returns solution matrix
