import tkinter as tk
import time

SIZE = 100
FIELD = 800

WHITE = "#FFD39B"
BLACK = "#CD661D"

root = tk.Tk()
fr = tk.Frame(root)
canv = tk.Canvas(root, width=FIELD, height=FIELD)
canv.pack()

wh_img = tk.PhotoImage(file="white.png")
bl_img = tk.PhotoImage(file="black.png")


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = BLACK if (x + y) / SIZE % 2 != 0 else WHITE
        canv.create_rectangle((x, y, x + SIZE, y + SIZE), fill=self.color)


game_field = [[Cell(i, j) for i in range(0, FIELD, SIZE)] for j in range(0, FIELD, SIZE)]

# grip = False

while True:
    canv.update()
    time.sleep(0.03)
