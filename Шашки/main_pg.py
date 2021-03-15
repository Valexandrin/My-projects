import pygame as pg

SIZE = 100
FIELD = 800
FPS = 25

WHITE = (255, 211, 155)
BLACK = (205, 102, 29)

pg.init()
sc = pg.display.set_mode([FIELD, FIELD])
timer = pg.time.Clock()
wh_img = pg.image.load('white.png')
bl_img = pg.image.load('black.png')
wh_img_rect = wh_img.get_rect()


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = BLACK if (x + y) / SIZE % 2 != 0 else WHITE
        pg.draw.rect(sc, self.color, (x, y, SIZE, SIZE))


grip_checker = False
x, y = 150, 50

while True:
    cells = [[Cell(i, j) for i in range(0, FIELD, SIZE)] for j in range(0, FIELD, SIZE)]
    checker = sc.blit(wh_img, (x-SIZE//2, y-SIZE//2))


    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            grip_checker = True
        if event.type == pg.MOUSEMOTION and grip_checker and checker.collidepoint(pg.mouse.get_pos()):
            x, y = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONUP:
            grip_checker = False

    pg.display.flip()
    timer.tick(FPS)