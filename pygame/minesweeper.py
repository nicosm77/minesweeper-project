import pygame
from tkinter import *
from tkinter import messagebox
from board import *
from leaderboard import *
import time
import os

class minesweeper():
    
    # initializer
    def __init__(self, board, screensize, leaderboard):
        self.board = board
        self.screensize = screensize
        self.leaderboard = leaderboard
        
        difficulty = board.difficulty
        
        if (difficulty == "very easy"):
            self.tilesize = screensize[0]//5 , screensize[1]//5
        elif (difficulty == "easy"):
            self.tilesize = screensize[0]//10 , screensize[1]//10  
        elif (difficulty == "medium"):
            self.tilesize = screensize[0]//15 , screensize[1]//15
        elif (difficulty == "hard"):
            self.tilesize = screensize[0]//20 , screensize[1]//20
            
        self.loadimages()

        # runs minesweeper
    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screensize)
        starttime = time.time()
            
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
            
            if (self.board.getwon()): #if the game has ended
                self.finaltime = round(time.time() - starttime,1)
                self.endscreen = Tk()
                self.endscreen.geometry("225x100")
                Label(self.endscreen, text=f"You won! Time taken: {self.finaltime} seconds\n\nEnter your username for the leaderboard:").pack(side=TOP)
                entry = Entry(self.endscreen, width=30)
                entry.pack(side=TOP)
                Button(self.endscreen, text = "Submit", command = lambda: self.submit(entry.get())).pack(side=TOP)
                self.endscreen.mainloop()
                running = False

            if (self.board.getlost()):
                self.finaltime = round(time.time() - starttime,1)
                for row in range(self.board.size[0]):
                    for col in range(self.board.size[1]):
                        tile = self.board.get_tile((row, col))
                        if not tile.getclicked():
                            tile.click()
                self.createboard()
                pygame.display.flip()
                messagebox.showinfo(message=f"Oops! You lost! Time taken: {self.finaltime} seconds")
                running = False
            
        pygame.quit() # quits pygame



         # creates board   
    def createboard(self):
        topleft = (0,0)
        for row in range(self.board.getsize()[0]): # gets number of rows in board
            for col in range(self.board.getsize()[1]): # blit puts on image onto another
                # gets the empty block image ( so we are filling the entire board with the empty block image )
                tile  = self.board.get_tile((row, col))
                image = minesweeper.getimage(self,tile)
                
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
                string = str(tile.getnumaround()) # if there is no a bomb, sees how many neighboring bombs tile has
                                        # then sets the corresponding numbered image to the tile
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

    def submit(self, name): #submit score to the leaderboard database
        self.leaderboard.add_score(self.board.size[0], self.finaltime, name)
        self.endscreen.destroy()