from random import choice
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
obligatory_cells = []
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
        player_dict.pop((self.x, self.y)).move(finish_cell.x, finish_cell.y)
        self.status = 0
        finish_cell.status = player
        self.released()
        [avlbl_cells.pop().released() for _ in range(len(avlbl_cells))]
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
        player_dict[self.x, self.y] = self


class WhChecker(Checker):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = canv.create_image(x * SIZE, y * SIZE, image=wh_img, anchor=tk.NW)


class BlChecker(Checker):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = canv.create_image(x * SIZE, y * SIZE, image=bl_img, anchor=tk.NW)


class GameManager:
    def obligatory_move(self):
        count = 0
        for checker in player_dict.values():
            neighbor = cells_book[checker.x, checker.y]
            for i in range(2):
                if neighbor[i]:
                    if neighbor[i].status != player and neighbor[i].status != 0:
                        next_neighbor = cells_book[neighbor[i].x, neighbor[i].y]
                        if next_neighbor[i] and next_neighbor[i].status == 0:
                            obligatory_cells.append(field[checker.x][checker.y])
                            count += 1
                            print(checker.x, checker.y)
                            print(neighbor[i].x, neighbor[i].y)
                            print(next_neighbor[i].x, next_neighbor[i].y)
        return True if count != 0 else False

    def grip(self, event):
        i = event.x
        j = event.y
        if field[i // SIZE][j // SIZE].status == player:
            for cell in cells_book[i // SIZE, j // SIZE]:
                if cell and cell.status == 0:
                    cell.select("yellow")
                    avlbl_cells.append(cell)
            if avlbl_cells:
                field[i // SIZE][j // SIZE].select("green")
                selected_cell.append(field[i // SIZE][j // SIZE])

    def check_action(self, event):
        i = event.x
        j = event.y
        if field[i // SIZE][j // SIZE] in obligatory_cells:
            pass
        elif field[i // SIZE][j // SIZE] in avlbl_cells:
            finish_cell = avlbl_cells[avlbl_cells.index(field[i // SIZE][j // SIZE])]
            selected_cell.pop().move(finish_cell)
        else:
            selected_cell.pop().released()
            [avlbl_cells.pop().released() for _ in range(len(avlbl_cells))]
            self.grip(event)

    def get_path(self):
        for checker in player_dict.values():
            for cell in cells_book[checker.x, checker.y]:
                if cell and cell.status == 0:
                    selected_cell.append(field[checker.x][checker.y])
        random_cell = choice(selected_cell)
        selected_cell.clear()
        for cell in cells_book[random_cell.x, random_cell.y]:
            if cell and cell.status == 0:
                avlbl_cells.append(cell)
        random_cell.move(choice(avlbl_cells))

    def change_player(self):
        global player
        player = 1 if player == 2 else 2
        print(player)


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
player = choice([1, 2])

while True:
    if player == 1:
        player_dict = wh_checkers
        cells_book = pl1_cells_book
        if selected_cell or gm.obligatory_move():
            canv.bind("<Button-1>", gm.check_action)
        else:
            canv.bind("<Button-1>", gm.grip)

    else:
        player_dict = bl_checkers
        cells_book = pl2_cells_book
        if gm.obligatory_move():
            # make move
            pass
        else:
            gm.get_path()

    canv.update()
    time.sleep(0.03)
