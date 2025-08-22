import pyglet
import time
from pyglet import shapes as sh
from pyglet.window.key import *

class Uprav:
    def __init__(self, x, y, playr, HP, width):
        self.x = x
        self.y = y
        self.playr = playr
        self.HP = HP
        self.width = width
        if 0 < x + playr.x < 721 - width:
            playr.x += x
            HP.x += x
        if 0 < y + playr.y < 721 - width:
            playr.y += y
            HP.y += y