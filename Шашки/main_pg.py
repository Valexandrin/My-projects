import pygame as pg

SIZE = 100
FIELD = 800
FPS = 25

WHITE = (255, 211, 155)
BLACK = (205, 102, 29)

pg.init()
sc = pg.display.set_mode([FIELD, FIELD])
timer = pg.time.Clock()


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = BLACK if (x + y) / SIZE % 2 != 0 else WHITE
        pg.draw.rect(sc, self.color, (x, y, SIZE, SIZE))


class Checker:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class WhChecker(Checker):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.wh_img = pg.image.load('white.png')
        self.wh_img_rect = self.wh_img.get_rect()
        sc.blit(self.wh_img, (self.x, self.y))


class BlChecker(Checker):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.wh_img = pg.image.load('black.png')
        self.wh_img_rect = self.wh_img.get_rect()
        sc.blit(self.wh_img, (self.x, self.y))


grip_checker = False

while True:
    cells = [[Cell(i, j) for i in range(0, FIELD, SIZE)] for j in range(0, FIELD, SIZE)]
    for row in cells[0:3]:
        for cell in row:
            checkers = WhChecker(cell.x, cell.y) if cell.color == BLACK else None
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

    pg.display.flip()
    timer.tick(FPS)
