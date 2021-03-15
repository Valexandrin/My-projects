import tkinter as tk
import time

SIZE = 100

WHITE = "#FFD39B"
BLACK = "#CD661D"

root = tk.Tk()
root.title("Шашки")
root.resizable(0, 0)
canv = tk.Canvas(root, width=SIZE * 8, height=SIZE * 8, highlightthickness=0)
canv.pack()

wh_img = tk.PhotoImage(file="white.png")
bl_img = tk.PhotoImage(file="black.png")

field = []


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.figure = 0
        self.color = BLACK if (x + y) % 2 != 0 else WHITE
        canv.create_rectangle((x * SIZE, y * SIZE, (x + 1) * SIZE, (y + 1) * SIZE), fill=self.color)


for cell_row in range(0, 8):
    for cell_col in range(0, 8):
        cell = Cell(cell_col, cell_row)
        if cell_row < 3 and cell.color == BLACK:
            cell.figure = 2
        if cell_row > 4 and cell.color == BLACK:
            cell.figure = 1
        field += [cell]

for cell in field:
    print(cell.figure)
    if cell.figure == 2:
        checker = canv.create_image(cell.x * SIZE, cell.y * SIZE, image=bl_img, anchor=tk.NW)
    elif cell.figure == 1:
        checker = canv.create_image(cell.x * SIZE, cell.y * SIZE, image=wh_img, anchor=tk.NW)


def grip(event):
    x = root.winfo_pointerx() - root.winfo_rootx()
    y = root.winfo_pointery() - root.winfo_rooty()
    event.widget.place(x=x, y=y, anchor=tk.CENTER)


# obj_1.bind("<B1-Motion>", grip)

while True:
    canv.update()
    time.sleep(0.03)
