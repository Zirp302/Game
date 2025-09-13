from pyglet import shapes as sh
import time
import pyglet
"""
Файл для создания обектов и их вывода пряма тут 
"""

class Pl:
    # Характеристеки игрока
    x = 340
    y = 330
    width = 50
    height = 100
    color = (54, 136, 181)

    # Характеристики здаровья
    HP_playr = 5               # Количество здоровья
    HP_One = width / HP_playr  # Длина одной еденице здаровья
    Polosa = HP_playr * HP_One # Полоска HP

    # Пакет для обединения HP и playr
    pl = pyglet.graphics.Batch()
    def playr(self): #Создание и отображение игрока
        self.playr = sh.Rectangle(Pl.x, Pl.y, Pl.width, Pl.height, Pl.color, batch=Pl.pl)
        return self.playr

    # HP игрока
    def HP(self):
        self.HP = sh.Rectangle(Pl.x, Pl.y + Pl.height, Pl.Polosa, 15, color=(255,0,0), batch=Pl.pl)
        return self.HP

    def draw(): # Отрисовка пакета данных с игроком и его полоской так как они должны передвигаться одновременно и одинаково
        Pl.pl.draw() 


class Stena: 
    # Характеристики стен для их отображения 
    left_S = (240, 230, 240, 490)
    right_S = (480, 230, 480, 490)
    niz_S = (350, 240, 490, 240)
    verh_S = (230, 480, 490, 480)
    # Ширина стен
    Shir_S = 20
    # Пакет данных со всеми стенами
    dom = pyglet.graphics.Batch() 

    #   Отображение стен (смотри на названия)
    def __init__(self, playr, HP, width): 
        self.playr = playr
        self.time = 0
        self.HP = HP
        self.width = width
        self.left_wall = sh.Line(Stena.left_S[0], Stena.left_S[1], 
                                Stena.left_S[2], Stena.left_S[3], 
                                thickness=Stena.Shir_S, batch=Stena.dom
        )
        self.right_wall = sh.Line(Stena.right_S[0], Stena.right_S[1], 
                                Stena.right_S[2], Stena.right_S[3], 
                                thickness=Stena.Shir_S, batch=Stena.dom
        )
        self.verh_wall = sh.Line(Stena.verh_S[0], Stena.verh_S[1], 
                                Stena.verh_S[2], Stena.verh_S[3],
                                thickness=Stena.Shir_S, batch=Stena.dom
        )
        self.niz_wall = sh.Line(Stena.niz_S[0], Stena.niz_S[1], 
                                Stena.niz_S[2], Stena.niz_S[3], 
                                thickness=Stena.Shir_S, batch=Stena.dom
        ) 
        self.shipi = sh.Rectangle(200, 200, 20, 20, color=(111,111,111), batch=Stena.dom)

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

    #   Проверка прямоугольников
    def rectangle(self, x1, y1, width, height, x, y, speed=5):
        x2 = x1 + width
        y2 = y1 + height
        return x2, y2

    #   Ограничение прохаждение через линии
    def ogran_line(self, x1, y1, x2, y2, x=0, y=0):
        x1, y1, x2, y2 = self.line(x1, y1, x2, y2, x, y) # Переназначение переменных через функцию line
        X = x1 - Pl.width < self.playr.x + x < x2
        Y = y1 - Pl.height < self.playr.y + y < y2
        if X and Y:
            return False
        return True

    #   Ограничение прохаждение через прямоуглоьники
    def ogran_rectangle(self, x1, y1, width, height, x=0, y=0):
        x2, y2 = self.rectangle(x1, y1, width, height, x, y) # Переназначение переменных через функцию rectangle
        X = x1 - Pl.width < self.playr.x + x < x2
        Y = y1 - Pl.height < self.playr.y + y < y2
        if X and Y:
            return False
        return True
    
    #   Получение урона при нахождении в линии
    def damag_line(self, x1, y1, width, height, x=0, y=0):
        x1, y1, x2, y2 = self.line(x1, y1, x2, y2, x, y)  # Переназначение переменных через функцию line
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

    #   Получение урона при нахождении в прямоуглоьнике
    def damag_rectangle(self, x1, y1, width, height, x=0, y=0):
        x2, y2 = self.rectangle(x1, y1, width, height, x, y) # Переназначение переменных через функцию rectangle
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

    #   Функция для отображения стен
    def draw(self): 
        Stena.dom.draw()


class Damag:
    def __init__(self, playr, HP, width): 
        self.playr = playr
        self.time = 0
        self.HP = HP
        self.width = width

