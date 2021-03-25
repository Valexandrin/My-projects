from random import choice
from collections import defaultdict
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

selected_cell = []
avlbl_cells = []
obligatory_cells = defaultdict(list)
pl1_cells_book = {}
pl2_cells_book = {}
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
        gm.player_dict.pop((self.x, self.y)).move(finish_cell.x, finish_cell.y)
        self.status = 0
        finish_cell.status = gm.player
        self.released()
        [avlbl_cells.pop().released() for _ in range(len(avlbl_cells))]
        if finish_cell not in obligatory_cells.keys():
            gm.change_player()
        elif not gm.obligations_check():
            gm.change_player()


class Checker:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = None

    def move(self, *args):
        old_x, old_y = self.x, self.y
        self.x, self.y = args
        step_x = self.x - old_x
        step_y = self.y - old_y
        for i in range(26):
            canv.coords(self.id,
                        (old_x + step_x * i * 0.04) * SIZE,
                        (old_y + step_y * i * 0.04) * SIZE)
            canv.update()
            time.sleep(0.01)
        gm.player_dict[self.x, self.y] = self


class WhChecker(Checker):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = canv.create_image(x * SIZE, y * SIZE, image=wh_img, anchor=tk.NW)


class BlChecker(Checker):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = canv.create_image(x * SIZE, y * SIZE, image=bl_img, anchor=tk.NW)


class GameManager:
    def __init__(self):
        self.player = choice([1, 2])
        self.player_dict = wh_checkers if self.player == 1 else bl_checkers
        self.cells_book = pl1_cells_book if self.player == 1 else pl2_cells_book

    def change_player(self):
        self.player = 1 if self.player == 2 else 2
        self.player_dict = wh_checkers if self.player == 1 else bl_checkers
        self.cells_book = pl1_cells_book if self.player == 1 else pl2_cells_book
        self.obligations_check()

    def list_filling(self, i, j, lst, *args, color=None, status=0):
        for item in self.cells_book[i, j]:
            if item and item.status == status:
                lst.append(field[i][j]) if args else lst.append(item)
                if color:
                    item.select(color)

    def obligations_check(self):
        obligatory_cells.clear()
        count = 0
        for checker in self.player_dict.values():
            neighbor = self.cells_book[checker.x, checker.y]
            for i in range(2):
                if neighbor[i]:
                    if neighbor[i].status != self.player and neighbor[i].status != 0:
                        next_neighbor = self.cells_book[neighbor[i].x, neighbor[i].y]
                        if next_neighbor[i] and next_neighbor[i].status == 0:
                            obligatory_cells[field[checker.x][checker.y]].append(next_neighbor[i])
                            count += 1
        return True if count != 0 else False

    def grip(self, event):
        i = event.x // SIZE
        j = event.y // SIZE
        if field[i][j].status == self.player:
            self.list_filling(i, j, avlbl_cells, color="yellow")
            if avlbl_cells:
                field[i][j].select("green")
                selected_cell.append(field[i][j])

    def cut_down_way(self, i, j):
        pass

    def check_action(self, event):
        i = event.x // SIZE
        j = event.y // SIZE
        if field[i][j] in obligatory_cells.keys() and not selected_cell:
            field[i][j].select("green")
            selected_cell.append(field[i][j])
            for i in obligatory_cells[field[i][j]]:
                i.select("yellow")
                avlbl_cells.append(i)
        elif field[i][j] in avlbl_cells:
            finish_cell = avlbl_cells[avlbl_cells.index(field[i][j])]
            selected_cell.pop().move(finish_cell)
        else:
            selected_cell.pop().released()
            [avlbl_cells.pop().released() for _ in range(len(avlbl_cells))]
            self.check_action(event) if obligatory_cells else self.grip(event)

    def get_path(self, dict):
        dict = dict.keys() if obligatory_cells else dict.values()
        for checker in dict:
            self.list_filling(checker.x, checker.y, selected_cell, True)
        random_cell = choice(selected_cell) if len(selected_cell) > 1 else selected_cell.pop()
        selected_cell.clear()
        if obligatory_cells:
            for i in obligatory_cells[field[random_cell.x][random_cell.y]]:
                avlbl_cells.append(i)
        else:
            self.list_filling(random_cell.x, random_cell.y, avlbl_cells)
        random_cell.move(choice(avlbl_cells))


# Chess board creation
field = [[Cell(i, j) for j in range(0, 8)] for i in range(0, 8)]
for row in field:
    for cell in row:
        if cell.y < 3 and cell.color == BLACK:
            cell.status = 2
            bl_checkers[cell.x, cell.y] = BlChecker(cell.x, cell.y)
        if cell.y > 4 and cell.color == BLACK:
            cell.status = 1
            wh_checkers[cell.x, cell.y] = WhChecker(cell.x, cell.y)

# Player_1 neighbor-cells book dict creation
for i in range(0, 8):
    for j in range(8):
        if field[j][i].color == BLACK:
            if i == 0:
                pl1_cells_book[j, i] = []
            elif j == 0:
                pl1_cells_book[j, i] = [None, field[j + 1][i - 1]]
            elif j == 7:
                pl1_cells_book[j, i] = [field[j - 1][i - 1], None]
            else:
                pl1_cells_book[j, i] = [field[j - 1][i - 1], field[j + 1][i - 1]]

# Player_2 neighbor-cells book dict creation
for i in range(0, 8):
    for j in range(8):
        if field[j][i].color == BLACK:
            if i == 7:
                pl2_cells_book[j, i] = []
            elif j == 0:
                pl2_cells_book[j, i] = [None, field[j + 1][i + 1]]
            elif j == 7:
                pl2_cells_book[j, i] = [field[j - 1][i + 1], None]
            else:
                pl2_cells_book[j, i] = [field[j - 1][i + 1], field[j + 1][i + 1]]

gm = GameManager()

while True:
    if gm.player == 1:
        if selected_cell or obligatory_cells:
            canv.bind("<Button-1>", gm.check_action)
        else:
            canv.bind("<Button-1>", gm.grip)
    else:
        if obligatory_cells:
            gm.get_path(obligatory_cells)
        else:
            gm.get_path(gm.player_dict)

    canv.update()
    time.sleep(0.03)
