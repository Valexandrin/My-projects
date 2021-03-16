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

book = {}
player = 1
selected = []
available = []


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = 0
        self.color = BLACK if (x + y) % 2 != 0 else WHITE
        self.id = canv.create_rectangle((x * SIZE, y * SIZE, (x + 1) * SIZE, (y + 1) * SIZE),
                                        fill=self.color)

    def set_checker(self):
        if self.status == 2:
            canv.create_image(self.x * SIZE, self.y * SIZE, image=bl_img, anchor=tk.NW)
        elif self.status == 1:
            canv.create_image(self.x * SIZE, self.y * SIZE, image=wh_img, anchor=tk.NW)

    def select(self, color):
        canv.itemconfig(self.id, outline=color, width=7)

    def released(self):
        canv.itemconfig(self.id, outline="black", width=1)

    def move(self, finish_cell):
        self.x = finish_cell.x
        self.y = finish_cell.y
        self.status = 0
        finish_cell.status = 1
        finish_cell.set_checker()  # TODO: add removing checker from old position
        self.released()
        [available.pop().released() for _ in range(len(available))]


field = [[Cell(j, i) for j in range(0, 8)] for i in range(0, 8)]

for row in field:
    for cell in row:
        if cell.y < 3 and cell.color == BLACK:
            cell.status = 2
            cell.set_checker()
        if cell.y > 4 and cell.color == BLACK:
            cell.status = 1
            cell.set_checker()

# dict of neighbors of all black cells
for i in range(8):
    for j in range(8):
        if field[i][j].color == BLACK:
            if i == 0:
                book[i, j] = [None, None]
            if j == 0:
                book[i, j] = [None, field[i - 1][j + 1]]
            elif j == 7:
                book[i, j] = [field[i - 1][j - 1], None]
            else:
                book[i, j] = [field[i - 1][j - 1], field[i - 1][j + 1]]


def check_action(event):
    if field[event.y // SIZE][event.x // SIZE] in available:
        finish_cell = available[available.index(field[event.y // SIZE][event.x // SIZE])]
        selected.pop().move(finish_cell)
    # TODO: add actions if clicking to cells outside of "available"

def grip(event):
    for cell in book[event.y // SIZE, event.x // SIZE]:
        if cell.status == 0:
            cell.select("yellow")
            available.append(cell)
    if available:
        field[event.y // SIZE][event.x // SIZE].select("green")
    selected.append(field[event.y // SIZE][event.x // SIZE])


while True:
    if player == 1:
        if not selected:
            canv.bind("<Button-1>", grip)
        else:
            canv.bind("<Button-1>", check_action)
    else:
        pass

    canv.update()
    time.sleep(0.03)
