class tile_class():
    def __init__ (self, hasbomb): # hasbomb is whether or not a bomb is at the given tile
        self.hasbomb = hasbomb
        self.clicked = False # whether or not the tile has been clicked on - default is False
        self.flagged = False # whether or not the tile has been flagged - default is False
        
        
    def gethasbomb(self): # tells us if theres a bomb there
        return self.hasbomb
    
    def getclicked(self): # tells us if tile has been clicked on
        return self.clicked
    
    def getflagged(self): # tells us if tile has been flagged
        return self.flagged
    
    def setneighbors(self, neighbors):
        self.neighbors = neighbors
        self.setnumaround()
    
    # counts number of bombs around tile
    def setnumaround(self):
        self.numaround = 0
        for tile in self.neighbors: # iterators through list of neighbors
            if (tile.gethasbomb()): # if it has a bomb
                self.numaround = self.numaround + 1 
                
    
    # gets number of bombs around clicked tile
    def getnumaround(self):
        return self.numaround
            
    def toggleflag(self):
            if (self.flagged):
                self.flagged = False
            else:
                self.flagged = True
                
    def click(self):
        self.clicked = True
        
    def getneighbors(self):
        return self.neighbors # list of neighbors
    
    def chord(self):
        flagsaround = 0 #find out how many flagged neighbors
        for neighbor in self.neighbors: 
            if neighbor.getflagged():
                flagsaround += 1
        numclicked = 0
        if flagsaround == self.numaround: # if the number of flagged neighbors = clue number...
            for neighbor in self.neighbors: # click on all unflagged and unclicked neighbors
                if not (neighbor.getflagged() or neighbor.getclicked()):
                    neighbor.click()
                    numclicked += 1
        return numclicked # return number clicked
