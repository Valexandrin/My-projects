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
player_dict = None
pl1_cells_book = {}
pl2_cells_book = {}
selected_cell = []
avlbl_cells = []
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
        global player
        player_dict.pop((self.x, self.y)).move(finish_cell.x, finish_cell.y)
        self.status = 0
        finish_cell.status = player
        self.released()
        [avlbl_cells.pop().released() for _ in range(len(avlbl_cells))]
        player = 1 if player == 2 else 2


class Checker:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = None

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


# Chess board creation
field = [[Cell(j, i) for j in range(0, 8)] for i in range(0, 8)]
for row in field:
    for cell in row:
        if cell.y < 3 and cell.color == BLACK:
            cell.status = 2
            bl_checkers[cell.x, cell.y] = BlChecker(cell.x, cell.y)
        if cell.y > 4 and cell.color == BLACK:
            cell.status = 1
            wh_checkers[cell.x, cell.y] = WhChecker(cell.x, cell.y)

# Player_1 dict of neighbors of all black cells
for i in range(0, 8):
    for j in range(8):
        if field[i][j].color == BLACK:
            if i == 0:
                pl1_cells_book[i, j] = []
            elif j == 0:
                pl1_cells_book[i, j] = [field[i - 1][j + 1]]
            elif j == 7:
                pl1_cells_book[i, j] = [field[i - 1][j - 1]]
            else:
                pl1_cells_book[i, j] = [field[i - 1][j - 1], field[i - 1][j + 1]]

# Player_2 dict of neighbors of all black cells
for i in range(0, 8):
    for j in range(8):
        if field[i][j].color == BLACK:
            if i == 7:
                pl2_cells_book[i, j] = []
            elif j == 0:
                pl2_cells_book[i, j] = [field[i + 1][j + 1]]
            elif j == 7:
                pl2_cells_book[i, j] = [field[i + 1][j - 1]]
            else:
                pl2_cells_book[i, j] = [field[i + 1][j - 1], field[i + 1][j + 1]]


def check_action(event):
    i = event.y
    j = event.x
    if field[i // SIZE][j // SIZE] in avlbl_cells:
        finish_cell = avlbl_cells[avlbl_cells.index(field[i // SIZE][j // SIZE])]
        selected_cell.pop().move(finish_cell)
    else:
        selected_cell.pop().released()
        [avlbl_cells.pop().released() for _ in range(len(avlbl_cells))]
        grip(event)


def grip(event):
    i = event.y
    j = event.x
    if field[i // SIZE][j // SIZE].status == player:
        for cell in cells_book[i // SIZE, j // SIZE]:
            if cell.status == 0:
                cell.select("yellow")
                avlbl_cells.append(cell)
        if avlbl_cells:
            field[i // SIZE][j // SIZE].select("green")
            selected_cell.append(field[i // SIZE][j // SIZE])


def get_path():
    pass


while True:
    if player == 1:
        player_dict = wh_checkers
        cells_book = pl1_cells_book
        if not selected_cell:
            canv.bind("<Button-1>", grip)
        else:
            canv.bind("<Button-1>", check_action)
    else:
        player_dict = bl_checkers
        cells_book = pl2_cells_book
        if not selected_cell:
            canv.bind("<Button-1>", grip)
        else:
            canv.bind("<Button-1>", check_action)

    canv.update()
    time.sleep(0.03)
