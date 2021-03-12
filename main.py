import pygame as pg

SIZE = 100
FIELD = 800
FPS = 3

WHITE = (255, 211, 155)
BLACK = (205, 102, 29)

pg.init()
sc = pg.display.set_mode([FIELD, FIELD])
timer = pg.time.Clock()
wh_img = pg.image.load('white.png')
bl_img = pg.image.load('black.png')


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = BLACK if (x + y) / SIZE % 2 != 0 else WHITE
        pg.draw.rect(sc, self.color, (x, y, SIZE, SIZE))


cells = [[Cell(i, j) for i in range(0, FIELD, SIZE)] for j in range(0, FIELD, SIZE)]
# white_checkers =

while True:

    pg.display.flip()
    timer.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
