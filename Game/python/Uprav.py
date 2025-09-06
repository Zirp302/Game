import pyglet
import time
from pyglet import shapes as sh
from pyglet.window.key import *
from Objekts import Pl, Stena


class Uprav:
    #   Доделать блокировку cтенам
    def __init__(self, playr, HP, width):
        self.playr = playr
        self.HP = HP
        self.width = width

    #   Передвижеие игрока и его полоски жизни
    def pl_moving(self, x, y, avanpost):
        self.x = x
        self.y = y
        self.playr = self.playr
        self.HP = self.HP
        self.width = self.width
        if 0 < x + self.playr.x < 721 - self.width and avanpost:
            self.playr.x += x
            self.HP.x += x
        if 0 < y + self.playr.y < 721 - self.width and avanpost:
            self.playr.y += y
            self.HP.y += y

    #   Даёт стенам возможность останавливать тела
    def ogran(self, x1, y1, x2, y2, x=0, y=0, speed=5): 
        if x1 == x2:
            x1 -= 10
            x2 += 10
            y1, y2 = min(y1, y2), max(y1, y2)
        else:
            y1 -= 10
            y2 += 10
            x1, x2 = min(x1, x2), max(x1, x2)
        if x1 - Pl.width < self.playr.x + x < x2 and y1 - Pl.height < self.playr.y + y < y2:
            return False
        return True
    
