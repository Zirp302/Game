import pyglet
import time
from pyglet import shapes as sh
from pyglet.window.key import *
from Objects import Pl, Stena


class playrUprav:
    #   Доделать блокировку cтенам
    def __init__(self, playr, HP, oruzhie):
        self.playr = playr
        self.HP = HP
        self.oruzhie = oruzhie

    #   Передвижеие игрока и его полоски жизни
    def pl_moving(self, x, y, avanpost):
        if (0 < x + self.playr.x < 721 - self.playr.width) and avanpost:
            self.playr.playr.x += x
            self.playr.x = self.playr.playr.x
            self.playr.HP.x += x
            if self.oruzhie.isPist == True:
                self.oruzhie.pist.x += x
                self.oruzhie.x += x
                self.oruzhie.x2 += x
        if (0 < y + self.playr.y < 721 - self.playr.width) and avanpost:
            self.playr.playr.y += y
            self.playr.y = self.playr.playr.y
            self.playr.HP.y += y
            if self.oruzhie.isPist == True:
                self.oruzhie.pist.y += y
                self.oruzhie.y += y
                self.oruzhie.y2 += y
        #   Проверка линий
    def line(self, x1, y1, x2, y2, x, y, speed=5): 
        if x1 == x2:
            x1 -= 10
            x2 += 10
            y1, y2 = min(y1, y2), max(y1, y2)
            return x1, y1, x2, y2
        else:
            y1 -= 10
            y2 += 10
            x1, x2 = min(x1, x2), max(x1, x2)
            return x1, y1, x2, y2
        
    # Ограничение прохаждение через линии
    def ogran_line(self, x1, y1, x2, y2, x=0, y=0):
        # Переназначение переменных согласно функции line
        x1, y1, x2, y2 = self.line(x1, y1, x2, y2, x, y) 
        X = x1 - self.playr.width < self.playr.x + x < x2
        Y = y1 - self.playr.height < self.playr.y + y < y2
        if X and Y:
            return False
        return True
    
    # Получение урона при прохаждение через линии
    def damag_line(self, x1, y1, width, height, x=0, y=0):
        # Переназначение переменных согласно функции rectangle
        x1, y1, x2, y2 = self.line(x1, y1, x2, y2, x, y) 
        X = x1 - self.playr.width < self.playr.x + x < x2
        Y = y1 - self.playr.height < self.playr.y + y < y2
        kd = 1.25
        time1 = time.time()
        if X and Y and time1 - self.time > kd:
            self.time = time1
            print(time1, self.time)
            self.HP.width -= self.playr.HP_One
            if self.HP.width <= 0:
                self.HP.width = self.playr.width
                self.playr.x = self.playr.x
                self.playr.y = self.playr.y
                self.HP.x = self.playr.x
                self.HP.y = self.playr.y + self.playr.height

    # Проверка прямоугольников
    def rectangle(self, x1, y1, width, height, x, y, speed=5):
        x2 = x1 + width
        y2 = y1 + height
        return x2, y2
    
    # Ограничение прохаждение через прямоуглоьники
    def ogran_rectangle(self, x1, y1, width, height, x=0, y=0):
        # Переназначение переменных согласно функции rectangle
        x2, y2 = self.rectangle(x1, y1, width, height, x, y)
        X = x1 - self.playr.width < self.playr.x + x < x2
        Y = y1 - self.playr.height < self.playr.y + y < y2
        if X and Y:
            return False
        return True
    
    # Получение урона при прохаждение через прямоуглоьники
    def damag_rectangle(self, x1, y1, width, height, x=0, y=0):
        # Переназначение переменных согласно функции rectangle
        x2, y2 = self.rectangle(x1, y1, width, height, x, y)
        X = x1 - self.playr.width < self.playr.x + x < x2
        Y = y1 - self.playr.height < self.playr.y + y < y2
        kd = 1.25
        time1 = time.time()
        if X and Y and time1 - self.time > kd:
            self.time = time1
            print(time1, self.time)
            self.HP.width -= self.playr.HP_One
            if self.HP.width <= 0:
                self.HP.width = self.playr.width
                self.playr.x = self.playr.x
                self.playr.y = self.playr.y
                self.HP.x = self.playr.x
                self.HP.y = self.playr.y + self.playr.height
