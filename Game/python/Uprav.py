import pyglet
import time
from pyglet import shapes as sh
from pyglet.window.key import *
from Objects import Pl, Stena


class playrUprav:
    #   Доделать блокировку cтенам
    def __init__(self, playr, HP):
        self.playr = playr
        self.HP = HP

    #   Передвижеие игрока и его полоски жизни
    def pl_moving(self, x, y, avanpost):
        if (0 < x + self.playr.x < 721 - self.playr.w) and avanpost:
            self.playr.playr.x += x
            self.playr.x = self.playr.playr.x
            self.playr.HP.x += x
        if (0 < y + self.playr.y < 721 - self.playr.w) and avanpost:
            self.playr.playr.y += y
            self.playr.y = self.playr.playr.y
            self.playr.HP.y += y

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
        X = x1 - Pl.width < self.playr.x + x < x2
        Y = y1 - Pl.height < self.playr.y + y < y2
        if X and Y:
            return False
        return True
    
    # Получение урона при прохаждение через линии
    def damag_line(self, x1, y1, width, height, x=0, y=0):
        # Переназначение переменных согласно функции rectangle
        x1, y1, x2, y2 = self.line(x1, y1, x2, y2, x, y) 
        X = x1 - Pl.width < self.playr.x + x < x2
        Y = y1 - Pl.height < self.playr.y + y < y2
        kd = 1.25
        time1 = time.time()
        if X and Y and time1 - self.time > kd:
            self.time = time1
            print(time1, self.time)
            self.HP.width -= Pl.HP_One
            if self.HP.width <= 0:
                self.HP.width = Pl.width
                self.playr.x = Pl.x
                self.playr.y = Pl.y
                self.HP.x = Pl.x
                self.HP.y = Pl.y + Pl.height

    # Проверка прямоугольников
    def rectangle(self, x1, y1, width, height, x, y, speed=5):
        x2 = x1 + width
        y2 = y1 + height
        return x2, y2
    
    # Ограничение прохаждение через прямоуглоьники
    def ogran_rectangle(self, x1, y1, width, height, x=0, y=0):
        # Переназначение переменных согласно функции rectangle
        x2, y2 = self.rectangle(x1, y1, width, height, x, y)
        X = x1 - Pl.width < self.playr.x + x < x2
        Y = y1 - Pl.height < self.playr.y + y < y2
        if X and Y:
            return False
        return True
    
    # Получение урона при прохаждение через прямоуглоьники
    def damag_rectangle(self, x1, y1, width, height, x=0, y=0):
        # Переназначение переменных согласно функции rectangle
        x2, y2 = self.rectangle(x1, y1, width, height, x, y)
        X = x1 - Pl.width < self.playr.x + x < x2
        Y = y1 - Pl.height < self.playr.y + y < y2
        kd = 1.25
        time1 = time.time()
        if X and Y and time1 - self.time > kd:
            self.time = time1
            print(time1, self.time)
            self.HP.width -= Pl.HP_One
            if self.HP.width <= 0:
                self.HP.width = Pl.width
                self.playr.x = Pl.x
                self.playr.y = Pl.y
                self.HP.x = Pl.x
                self.HP.y = Pl.y + Pl.height
