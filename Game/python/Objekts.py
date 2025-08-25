import pyglet
import time
from pyglet import shapes as sh
from pyglet.window.key import *
import Uprav
class Pl:
    def __init__(self,batch, x=100, y=100, width=10, height=10, color={125,254,88}):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.batch = batch 
        self.playr = sh.Rectangle(x, y, width, height, color, batch=batch)

    
    def pl_moving(self, x_speed, y_speed, speed=5):
        HP_playr = 5
        HP_One = self.width / HP_playr
        HP = sh.Rectangle(self.playr.x, self.playr.y + self.height, HP_playr * HP_One, 15, color=(255,0,0), batch=self.batch)
        key = Uprav(x_speed, y_speed, self.playr, HP, self.width)

    def pl_moving(self, x, y):
        if 0 < x + self.playr.x < 721 - self.width:
            self.playr.x += x
        if 0 < y + self.playr.y < 721 - self.width:
            self.playr.y += y


    def draw(self):
        self.playr.draw()
    


