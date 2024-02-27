from minesweeper import *
from board import *

difficulty = "test"

#difficulty = "easy"

#difficulty = "medium"

#difficulty = "hard"

gameboard = board(difficulty)
screensize = (600, 600)

game = minesweeper(gameboard, screensize)
game.start()