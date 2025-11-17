import pyglet
from pyglet import shapes as sh
from time import time
from random import choice, randint




class Entitie:
    def __init__(self):
        # Параметры сущности
        self.color_body = (54, 136, 181)
        self.x = 320
        self.y = 320
        self.width = 100
        self.height = 100
        
        # Параметры полоски HP 
        self.color_hp = (255, 0, 0)
        self.width_hp = self.width
        self.height_hp = 15
        self.x_hp = self.x
        self.y_hp = self.y + self.height
        
        # Игровые параметры
        self.x_spawn = 320
        self.y_spawn = 320
        self.time = 0
        self.kd = 0.75
        self.pak = pyglet.graphics.Batch()

    def hp(self, hp_quantity=15):
        self.hp_quantity = hp_quantity
        self.width_one_hp = self.width / hp_quantity
        self.hp_entitie = sh.Rectangle(
            self.x_hp, self.y_hp, 
            self.width_hp, self.height_hp, 
            self.color_hp, batch=self.pak
            )

    def body(self): # Создание существа
        self.body_entitie = sh.Rectangle(
            self.x, self.y, 
            self.width, self.height, 
            self.color_body, batch=self.pak
            )

    def damage(self, x1, y1, width_threat, height_threat, uron=1):
        # Распределение крайних точек атакующего обекта
        x2 = x1 + width_threat
        y2 = y1 + height_threat
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        X = x1 - self.width < self.x < x2
        Y = y1 - self.height < self.y < y2
        time0 = time()
        time_kd = time0 - self.time > self.kd

        # Миханника получение урона
        if X and Y and time_kd: 
            self.time = time0
            self.hp_entitie.width -= self.width_one_hp * uron
            if self.hp_entitie.width <= 0:
                self.death()

    def death(self): # Механника смерти
        # Возраждение игрока
        self.x = self.x_spawn
        self.y = self.x_spawn
        # Возполнение hp
        self.hp_entitie.width = self.width_hp
        self.hp_entitie.x = self.x_spawn
        self.hp_entitie.y = self.y_spawn + self.height
            

    def draw(self):
        self.pak.draw()

