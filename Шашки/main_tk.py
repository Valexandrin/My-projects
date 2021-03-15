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
        self.id = canv.create_rectangle((x * SIZE, y * SIZE, (x + 1) * SIZE, (y + 1) * SIZE),
                                        fill=self.color)

    def clicked(self):
        canv.itemconfig(self.id, outline="green", width=7)


for cell_row in range(0, 8):
    for cell_col in range(0, 8):
        cell = Cell(cell_col, cell_row)
        if cell_row < 3 and cell.color == BLACK:
            cell.figure = 2
        if cell_row > 4 and cell.color == BLACK:
            cell.figure = 1
        field += [cell]

for cell in field:
    if cell.figure == 2:
        checker = canv.create_image(cell.x * SIZE, cell.y * SIZE, image=bl_img, anchor=tk.NW)
    elif cell.figure == 1:
        checker = canv.create_image(cell.x * SIZE, cell.y * SIZE, image=wh_img, anchor=tk.NW)


def grip(event):
    for cell in field:
        if cell.x == event.x // 100 and cell.y == event.y // 100 and cell.figure == 1:
            print(cell.x, cell.y)
            cell.clicked()


while True:
    canv.bind("<Button-1>", grip)
    canv.update()
    time.sleep(0.03)
