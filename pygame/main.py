from minesweeper import *
from board import *
from tkinter import *
from leaderboard import Leaderboard

#initialize leaderboard
leaderboard = Leaderboard()

running = True

def playgame():
    mainmenu.destroy()
    #make difficulty selection menu
    diffmenu = Tk()
    diffmenu.geometry("225x100")
    Label(diffmenu, text="Select a difficulty!").grid(row=0,columnspan=4)
    difficulty = StringVar()
    diffs = ["Very Easy", "Easy", "Medium", "Hard"]
    for i in range(4):
        Radiobutton(diffmenu, text = diffs[i], variable = difficulty, value = str.lower(diffs[i]), indicator = 0).grid(row=1,column=i,padx=5,pady=5)
    Button(diffmenu, text = "Continue", command = diffmenu.destroy).grid(row=2,columnspan=4)
    diffmenu.mainloop()

    if difficulty.get() == "": #default to very easy difficulty
        difficulty.set("very easy")

    gameboard = board(difficulty.get())
    screensize = (600, 600)
    game = minesweeper(gameboard, screensize, leaderboard)
    game.start()

def kill():
    global running
    running = False
    mainmenu.destroy()

def view_leaderboard():
    mainmenu.destroy()
    viewlb = Tk()
    viewlb.geometry("100x100")
    Label(viewlb, text=leaderboard.get_leaderboard(10)) #need to figure out how to display dataframes
    viewlb.mainloop()

while(running):
    mainmenu = Tk()
    mainmenu.geometry("250x75")
    Label(mainmenu, text="Welcome! Click a button to begin.").grid(row=0,columnspan=3,pady=5)
    Button(mainmenu, text = "New Game", command = playgame).grid(row=1,column=0,padx=7)
    Button(mainmenu, text = "View Leaderboard", command = view_leaderboard).grid(row=1,column=1,padx=7)
    Button(mainmenu, text = "Quit", command = kill).grid(row=1,column=2,padx=7)
    mainmenu.mainloop()