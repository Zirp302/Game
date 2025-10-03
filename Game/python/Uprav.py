import pyglet
from pyglet import shapes as sh
from pyglet.window import key
from pyglet.window.key import *
from Objeсts import Player, Stena, Damag

#   Управление 
class Playr_uprav:
    def __init__(self, playr,speed=5):
        self.playr = playr
        self.HP = playr.HP
        self.speed = speed
        self.damag = Damag(playr)
        self.stena = Stena(playr.width)
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
        avanpost = Stena.avanpost(self.playr, x_mov, y_mov)
        if 0 < x_mov + self.playr.x < 721 - self.playr.width and avanpost:
            self.playr.x += x_mov
            self.HP.x += x_mov
        if 0 < y_mov + self.playr.y < 721 - self.playr.width and avanpost:
            self.playr.y += y_mov
            self.HP.y += y_mov
            
