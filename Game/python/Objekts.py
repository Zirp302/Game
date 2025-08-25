from pyglet import shapes as sh
from pyglet.window.key import *
from Uprav import Uprav


class Pl:
    # Создание самого игрока
    playr = None
    def __init__(self, x, y, width, height, color, batch):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.batch = batch
        Pl.playr = sh.Rectangle(x, y, width, height, color, batch=batch)
        

    # HP игрока
    def HP(self):
        playr = Pl.playr
        HP_playr = 5
        HP_One = self.width / HP_playr
        HP = sh.Rectangle(self.playr.x, self.playr.y + self.height, HP_playr * HP_One, 15, color=(255,0,0), batch=self.batch)
        key = Uprav(x_speed, y_speed, self.playr, HP, self.width)

    def pl_moving(self, x, y):
        if 0 < x + self.playr.x < 721 - self.width:
            self.playr.x += x
        if 0 < y + self.playr.y < 721 - self.width:
            self.playr.y += y

        Polosa = HP_playr * HP_One # Полоска HP
        return sh.Rectangle(playr.x, playr.y + self.height, Polosa, 15, color=(255,0,0), batch=self.batch)

    def draw(self):
        Pl.playr.draw()

