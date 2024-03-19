from tile import tile_class
from random import random
            
class board():
    def __init__(self, difficulty):
        
        self.difficulty = difficulty
        
        if difficulty == "very easy": # 5 x 5 with 0.1 probability of bomb
            self.size = (5,5)
            self.prob = 0.1

        if difficulty == "easy": # 10 x 10 with 0.1 probability of bomb
            self.size = (10,10)
            self.prob = 0.1
            
        if difficulty == "medium": # 14 x 14 with 0.14 probability of bomb
            self.size = (15,15)
            self.prob = 0.14
        
        if difficulty == "hard": # 18 x 18 with 0.18 probability of bomb
            self.size = (20,20)
            self.prob = 0.18
        
        
        self.lost = False
        self.won = False
        self.numberclicked = 0
        self.numberofnonbombs = 0
        self.setboard()
        
    def setboard(self):
        self.board = []
        for row in range(self.size[0]):
            row = []
            for col in range(self.size[1]):
                hasbomb = random() < self.prob # of the random number is less than the probability, 
                                            # this will read true and a bomb will be placed there
                                            # otherwise will be false and no bomb will be placed there
                if ( not hasbomb): # if tile doesnt have a bomb
                    self.numberofnonbombs = self.numberofnonbombs + 1
                    
                tile = tile_class(hasbomb) # sets the tile using tile class initiliazer
                row.append(tile)
            self.board.append(row)
        self.setneighbors()
    
    
    def setneighbors(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                tile = self.get_tile((row, col)) # gets the tile at the given row and column - will tell us if bomb or not
                
                neighbors = self.getlistofneighbors((row, col))
                tile.setneighbors(neighbors)
    
    def getlistofneighbors(self, index):
        neighbors = [] # list of neighbors
        for row in range(index[0] - 1, index[0] + 2): # in the 3x3 grid around the tile, the -1 and +2 starts us at the top left
            for col in range(index[1] - 1, index[1] + 2):
                
                # out of bounds checks if part of the 3x3 grid is outside of the minesweeper board
                # this is used for corner tiles and side tiles
                outofbounds = row < 0 or row >= self.size[0] or col < 0 or col >= self.size[1]
                same = (row == index[0] and col == index[1]) # checks if the neighbor tile is the same as the clicked tile
                if (same or outofbounds):
                    continue
                else:
                    neighbors.append(self.get_tile((row, col))) # adds the neighbor to the list of neighbors
        return neighbors
            
    
    # gets board size
    def getsize(self):
        return self.size
    
    def get_tile(self, index):
        return self.board[index[0]][index[1]] # row and column
    
    def userclicked(self, tile, rightclick):
        
        if (rightclick): 
            if tile.getclicked(): # chording feature (see tile.py for info)
                self.numberclicked += tile.chord()
            else:
                tile.toggleflag()
            return
        
        if (tile.getflagged()):
            return
        
       # if (tile.getclicked() == True or tile.getflagged() == True): # makes sure it was a left click on a tile 
                                            # that hasnt been clicked on and one that doesnt have a flag
            #return 
        #if (rightclick): 
         #   tile.toggleflag()
        #    return
        
        # if we arent clicking on a flag or pre clicked square, and we arent rightclicking, then we left click
        
        tile.click() # left click
 
        if (tile.gethasbomb()):
            self.lost = True # looses if tile clicked has bimb
            return
        self.numberclicked = self.numberclicked + 1
        
        # this is so auto open all non bomb tiles near the non bomb tile we just hit
        if (tile.getnumaround() != 0):  #if theres a bomb nearby, do nothing
            return
        for neighbor in tile.getneighbors():
            if (neighbor.gethasbomb() == False and neighbor.getclicked() == False): # if neghbor doesnt have bomb, and its not already clicked
                self.userclicked(neighbor, False) # false bc we arent flagging the tile
            
        
    def getwon(self):
        return (self.numberofnonbombs == self.numberclicked) # if we clicked every non bomb tile, then we win
    
    def getlost(self):
        return self.lost