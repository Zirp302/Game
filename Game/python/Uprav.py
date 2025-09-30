import pyglet
from pyglet import shapes as sh
from pyglet.window import key
from pyglet.window.key import *
from Objeсts import Pl, Stena

#   Управление 
class Playr_uprav:
    def __init__(self, playr, HP, width):
        self.playr = playr
        self.HP = HP
        self.width = width
        self.speed = 3
    #   Передвижеие игрока и его полоски жизни
    def pl_moving(self, keys):
        if keys[W]:
            x_mov, y_mov = 0, self.speed
        if keys[S]:
            x_mov, y_mov = 0, -self.speed
        if keys[A]:
            x_mov, y_mov = -self.speed, 0
        if keys[D]:
            x_mov, y_mov = self.speed, 0
        print(x_mov, y_mov)
        avanpost = Stena.avanpost(self.playr, x_mov, y_mov)
        if 0 < x_mov + self.playr.x < 721 - self.width and avanpost:
            print(self.playr.x)
            self.playr.x += y_mov
            self.HP.x += y_mov
        if 0 < y_mov + self.playr.y < 721 - self.width and avanpost:
            print("y")
            self.playr.y += y_mov
            self.HP.y += y_mov
