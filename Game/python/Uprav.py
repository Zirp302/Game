import pyglet
from pyglet import shapes as sh
from pyglet.window.key import *
from Objekts import Pl, Stena

#   Управление 
class Uprav:
    def __init__(self, playr, HP, width):
        self.playr = playr
        self.HP = HP
        self.width = width

    #   Передвижеие игрока и его полоски жизни
    def pl_moving(self, x, y, avanpost):
        self.x = x
        self.y = y
        if 0 < x + self.playr.x < 721 - self.width and avanpost:
            self.playr.x += x
            self.HP.x += x
        if 0 < y + self.playr.y < 721 - self.width and avanpost:
            self.playr.y += y
            self.HP.y += y
