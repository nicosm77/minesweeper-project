from minesweeper import *
from board import *
from tkinter import *

menu = Tk()
menu.geometry("225x100")
Label(menu, text="Select a difficulty!").grid(row=0,columnspan=4)
difficulty = StringVar()
diffs = ["Very Easy", "Easy", "Medium", "Hard"]
for i in range(4):
    Radiobutton(menu, text = diffs[i], variable = difficulty, value = str.lower(diffs[i]), indicator = 0).grid(row=1,column=i,padx=5,pady=5)
Button(menu, text = "Continue", command = menu.destroy).grid(row=2,columnspan=4)
menu.mainloop()

if difficulty.get() == "":
    difficulty.set("very easy")

gameboard = board(difficulty.get())
screensize = (600, 600)

game = minesweeper(gameboard, screensize)
game.start()