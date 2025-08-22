import pyglet
import time
from pyglet import shapes as sh
from pyglet.window.key import *

class Pl:
    def __init__(self, x, y, width, height, color, batch):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.batch = batch 
        self.playr = sh.Rectangle(x, y, width, height, color, batch=batch)
    


    def pl_moving(self, x, y):
        if 0 < x + self.playr.x < 721 - self.width:
            self.playr.x += x
        if 0 < y + self.playr.y < 721 - self.width:
            self.playr.y += y
    #Прорисовка происходит ТОЛЬКО в функции с названием on_draw 


class Zombi:
    def __init__(self, x, y, w, h, col={}):
        