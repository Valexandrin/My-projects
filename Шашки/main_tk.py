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

player = 1
player_dict = 0
pl1_cells_book = {}
selected_cell = []
available_cells = []
bl_checkers = {}
wh_checkers = {}


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = 0
        self.color = BLACK if (x + y) % 2 != 0 else WHITE
        self.id = canv.create_rectangle((x * SIZE, y * SIZE, (x + 1) * SIZE, (y + 1) * SIZE),
                                        fill=self.color)

    def select(self, color):
        canv.itemconfig(self.id, outline=color, width=7)

    def released(self):
        canv.itemconfig(self.id, outline="black", width=1)

    def move(self, finish_cell):
        player_dict.pop((self.x, self.y)).move(finish_cell.x, finish_cell.y)

        self.status = 0
        finish_cell.status = 1
        self.released()
        [available_cells.pop().released() for _ in range(len(available_cells))]


class Checker:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = 0

    def move(self, *args):
        self.x, self.y = args
        canv.coords(self.id, self.x * SIZE, self.y * SIZE)
        player_dict[self.x, self.y] = self


class WhChecker(Checker):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = canv.create_image(x * SIZE, y * SIZE, image=wh_img, anchor=tk.NW)


class BlChecker(Checker):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = canv.create_image(x * SIZE, y * SIZE, image=bl_img, anchor=tk.NW)


field = [[Cell(j, i) for j in range(0, 8)] for i in range(0, 8)]

for row in field:
    for cell in row:
        if cell.y < 3 and cell.color == BLACK:
            cell.status = 2
            bl_checkers[cell.x, cell.y] = BlChecker(cell.x, cell.y)
        if cell.y > 4 and cell.color == BLACK:
            cell.status = 1
            wh_checkers[cell.x, cell.y] = WhChecker(cell.x, cell.y)

# dict of neighbors of all black cells
for i in range(1, 8):
    for j in range(8):
        if field[i][j].color == BLACK:
            if j == 0:
                pl1_cells_book[i, j] = [field[i - 1][j + 1]]
            elif j == 7:
                pl1_cells_book[i, j] = [field[i - 1][j - 1]]
            else:
                pl1_cells_book[i, j] = [field[i - 1][j - 1], field[i - 1][j + 1]]


def check_action(event):
    if field[event.y // SIZE][event.x // SIZE] in available_cells:
        finish_cell = available_cells[available_cells.index(field[event.y // SIZE][event.x // SIZE])]
        selected_cell.pop().move(finish_cell)
        print("Ход")
    else:
        selected_cell.pop().released()
        [available_cells.pop().released() for _ in range(len(available_cells))]
        grip(event)
        print("Перезахват")


def grip(event):
    #TODO: add a check of a checker on clicked cell
    print("Захват")
    for cell in pl1_cells_book[event.y // SIZE, event.x // SIZE]:
        if cell.status == 0:
            cell.select("yellow")
            available_cells.append(cell)
    if available_cells:
        field[event.y // SIZE][event.x // SIZE].select("green")
        selected_cell.append(field[event.y // SIZE][event.x // SIZE])


while True:
    if player == 1:
        player_dict = wh_checkers
        if not selected_cell:
            canv.bind("<Button-1>", grip)
        else:
            canv.bind("<Button-1>", check_action)
    else:
        player_dict = bl_checkers
        pass

    canv.update()
    time.sleep(0.03)
