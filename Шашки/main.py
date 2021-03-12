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

obj_1 = tk.Canvas(root, width=SIZE, height=SIZE)
obj_1.place(x=250, y=250)
obj_1.create_image(0, 0, image=bl_img, anchor = tk.NW)


def grip(event):
    x = root.winfo_pointerx() - root.winfo_rootx()
    y = root.winfo_pointery() - root.winfo_rooty()
    event.widget.place(x =x, y =y, anchor = tk.CENTER)

obj_1.bind("<B1-Motion>", grip)



while True:
    canv.update()
    time.sleep(0.03)
