import pygame



class minesweeper():
    
    # initializer
    def __init__(self, board, screensize):
        self.board = board
        self.screensize = screensize
        
        difficulty = board.difficulty
        
        # based off a 600 x 600 screen easy has 10 tiles, medium 15, hard 20
        if (difficulty == "easy"):
            self.tilesize = 60, 60
            
        if (difficulty == "medium"):
            self.tilesize = 40, 40
        if (difficulty == "hard"):
            self.tilesize = 30, 30
            
        

        self.loadimages()
        
        
    
        
        # runs minesweeper
    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screensize)
            
        # while minesweeper is running
        running = True
        while running:
            for event in pygame.event.get():
                    
                # if we quit game
                if(event.type == pygame.QUIT):
                    running = False # stops running
                    
                if(event.type ==pygame.MOUSEBUTTONDOWN): # click
                    clickposition = pygame.mouse.get_pos()
                    rightclick = pygame.mouse.get_pressed()[2]  # true if right clicked, false if not
                    self.userclicked(clickposition, rightclick)
                    
                
                        
                self.createboard() # creates board based on the click - so if we left click it will automatically re-creates the board
                            # to reflect our left clicked item
                        
            pygame.display.flip()
            
            if (self.board.getwon()): # win situation
                #usermessage("You Won! Quit the game to play again!", "You Won!")
                
                running = False
            
            if (self.board.getlost()):
                #message = "Oops! You lost! Click around on the board to reveal all the tiles, then quit the game to try again!"
                #usermessage("oops!" , "You Lost!")
                
               
                
                
                # NEED A POPUP SAYING YOU LOST - 
                # THEN, USER CAN CLICK AROUND THE BOARD TO REVEAL ALL TILES AND QUIT OUT OF PYGAME WHEN DONE
                running = False
            
        pygame.quit() # quits pygame



         # creates board   
    def createboard(self):
        topleft = (0,0)
        for row in range(self.board.getsize()[0]): # gets number of rows in board
            for col in range(self.board.getsize()[1]): # blit puts on image onto another
                # gets the empty block image ( so we are filling the entire board with the empty block image )
                tile  = self.board.get_tile((row, col))
                image = minesweeper.getimage(tile)
                
                # starts by filling at the top left, then moving down and across
                self.screen.blit(image, topleft)
                #increases width by size of each individual tile , height stays the same
                topleft = topleft[0] + self.tilesize[0], topleft[1]
            # sets width to be zero, increses height by size of each tile
            topleft = 0, topleft[1] + self.tilesize[1]  
                        
                    
        
    def loadimages(self):
        #dictionary links name of the png images to 
        self.images = {}
        for name in os.listdir("images"):
                
            if (not name.endswith(".png")):
                continue
                    
            image = pygame.image.load(r"images/" + name)
            image = pygame.transform.scale(image, self.tilesize) # scales the images to fit the tile sizes
            self.images[name.split(".")[0]] = image
            
    def getimage(self, tile):
        
        string = None
        
        if(tile.getclicked()): # if tile is clicked
            if (tile.gethasbomb()): # if it has a bomb
                string = "bomb-at-clicked-block"
            else:
                bombs = tile.getnumaround() # if there is no a bomb, sees how many neighboring bombs tile has
                                        # then sets the corresponding numbered image to the tile
            
                if bombs == 0:
                    #string = "0"
                    string = "0"
                if bombs == 1:
                    string = "1" 
                if bombs == 2:
                    string = "2"
                if bombs == 3:
                    string = "3"
                if bombs == 4:
                    string = "4"
                if bombs == 5:
                    string = "5"
                if bombs == 6:
                    string = "6"
                if bombs == 7:
                    string = "7"
                if bombs == 8:
                    string = "8"
                
        else:
            if tile.getflagged():
                string = "flag"
            else:
                string = "empty-block"
        return self.images[string]
        
        
    
    
    def userclicked(self, clickposition, rightclick): # rightclick is true or false depending on if there was a right click or not
        #if (self.board.getlost()): # if we lose
            #return
        index = clickposition[1] // self.tilesize[1], clickposition[0] // self.tilesize[0]
        # y positon is 1, x clickposition is zero
        # this divides the position pixel coordinates by the size of each peice - since the board is completly full of tiles
        # dividning by tile size will give us the coordiante of the click in number form
        # if we hit the 3rd row 4th colum (3,4)
        
        tile = self.board.get_tile(index) # gets the tile user clicked
        self.board.userclicked(tile, rightclick) # passes to board

              
        

                
from random import random
            
class board():
    def __init__(self, difficulty):
        
        self.difficulty = difficulty
        
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

         







        