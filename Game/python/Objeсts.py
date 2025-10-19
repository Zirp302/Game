import pyglet
from pyglet import shapes as sh
from time import time
import random
zombies={} # значение в хэш таблице это хр зомби
"""
Файл для создания обектов и их вывода пряма тут 
"""

class Pl:
    # Характеристеки игрока
    x, y = 340, 340 # Координаты спавна
    width = 50   # Длинна персонажа и полосы здоровья
    height = 100 # Ширина персонажа
    color = (54, 136, 181)
    time = 0

    # Характеристики здаровья
    HP_playr = 15          # Количество здоровья
    HP_One = width / HP_playr  # Длина одной еденице здаровья

    # Пакет для обединения HP и playr
    pl = pyglet.graphics.Batch()
    def playr(self): #Создание и отображение игрока
        self.playr = sh.Rectangle(Pl.x, Pl.y, Pl.width, Pl.height, Pl.color, batch=Pl.pl)
        return self.playr

    # HP игрока
    def HP(self):
        self.HP = sh.Rectangle(Pl.x, Pl.y + Pl.height, Pl.width, 15, color=(255,0,0), batch=Pl.pl)
        return self.HP
    
    def draw(self):
        self.pl.draw()


class Damag:
    time = 0
    def __init__(self, playr, HP):  # значение по умолчанию
        self.playr = playr
        self.HP = HP
        self.HP_One = Pl.width / Pl.HP_playr
        
    # Функция для определения получаемого урона   
    def damag(self, uron, x1, y1, x2, y2, x, y):
        X = x1 - Pl.width < self.playr.x + x < x2
        Y = y1 - Pl.height < self.playr.y + y < y2
        kd = 0.75
        time1 = time()
        # Миханника получение урона
        if X and Y and time1 - Damag.time > kd: 
            Damag.time = time1
            self.HP.width -= self.HP_One * uron
            # Механника смерти
            if self.HP.width <= 0:
                self.HP.width = Pl.width
                self.playr.x = Pl.x
                self.playr.y = Pl.y
                self.HP.x = Pl.x
                self.HP.y = Pl.y + Pl.height
    
    #   Получение урона при нахождении в линии
    def damag_line(self, x1, y1, x2, y2, uron=1, x=0, y=0):
        if x1 == x2:
            x1 -= 10
            x2 += 10
            y1, y2 = min(y1, y2), max(y1, y2)
        else:
            y1 -= 10
            y2 += 10
            x1, x2 = min(x1, x2), max(x1, x2)
        self.damag(uron, x1, y1, x2, y2, x, y)

    #   Получение урона при нахождении в прямоуглоьнике
    def damag_rectangle(self, x1, y1, width, height, uron=1, x=0, y=0):
        x2 = x1 + width
        y2 = y1 + height
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        self.damag(uron, x1, y1, x2, y2, x, y)



class Zombi:
    def __init__(self, playr, HP, screens):
        #Мне лень писать self
        #Но я напишу
        #type это тип зомби
        self.zombiBat = pyglet.graphics.Batch()
        self.width = 35
        self.height = 35
        self.color = (21, 110, 100)
        self.xp = 100
        self.speed = 1
        self.playr = playr
        self.HP = HP
        self.screens = screens

    def spawn(self, isSpawn=True):  
        if isSpawn:
            if random.choice((0, 1)):
                y = random.randint(0, self.screens.height)
                x = random.choice((0, self.screens.width))
            else:
                x = random.randint(0, self.screens.width)
                y = random.choice((0, self.screens.height))

            zombi_key = sh.Rectangle(
                x, y, self.width, self.height, 
                (21, 110, 100), batch=self.zombiBat
                )
                
            zombies[zombi_key] = (sh.Rectangle(
                x, y + self.height, 
                self.width, 4, 
                batch=self.zombiBat, color=(255, 0, 0)
                ), self.width / self.xp)
            print(len(zombies))

    def moving(self):
            for zombis in zombies:
                if self.playr.x > zombis.x:
                    zombis.x += self.speed
                    zombies[zombis][0].x += self.speed
                elif self.playr.x < zombis.x:
                    zombis.x = zombis.x - self.speed
                    zombies[zombis][0].x -= self.speed

                if self.playr.y > zombis.y:
                    zombis.y += self.speed
                    zombies[zombis][0].y += self.speed
                elif self.playr.y < zombis.y:
                    zombis.y = zombis.y - self.speed
                    zombies[zombis][0].y -= self.speed
                
    def test(self, x, y, width, height):
        zombies[sh.Rectangle(x, y, width, height, color=self.color, batch=self.zombiBat)] = (sh.Rectangle(x, y + height, width, 3, color=(255,0,0), batch=self.zombiBat), self.width / 100)

    def attack(self):
        for zomby in zombies:
            Damag(self.playr, self.HP).damag_rectangle(zomby.x, zomby.y, zomby.width, zomby.height)




    def draw(self):
        self.zombiBat.draw()


class Wall: 
    # Координаты стен для отображения 
    left_wall = (240, 230, 240, 490, (255, 255, 255))
    right_wall = (480, 230, 480, 490, (255, 255, 255))
    niz_wall = (350, 240, 490, 240, (255, 255, 255))
    verh_wall = (230, 480, 490, 480, (255, 255, 255))
    # Координаты чегото наносящего урон
    shipi = (200, 200, 20, 20, (111,111,111))
    # Ширина стен
    width_wall = 20
    # Пакет данных со всеми стенами
    dom = pyglet.graphics.Batch() 
    all_line_walls = {
        left_wall: None, 
        right_wall: None, 
        niz_wall: None, 
        verh_wall: None
        }
    all_recta_walls = {
        shipi: None
        }

    #   Отображение стен (смотри на названия)
    def __init__(self, playr, HP): 
        self.playr = playr   
        self.HP = HP
        self.width = playr.width

        for line_wall in self.all_line_walls:
            self.all_line_walls[line_wall] = sh.Line(
                line_wall[0], line_wall[1], 
                line_wall[2], line_wall[3], 
                color=line_wall[4], thickness=self.width_wall, 
                batch=self.dom
                )
        
        for recta_wall in self.all_recta_walls:
            self.all_recta_walls[recta_wall] = sh.Rectangle(
                recta_wall[0], recta_wall[1], 
                recta_wall[2], recta_wall[3], 
                color=recta_wall[4], batch=self.dom
                )
            

    #   Проверка линий
    def line(self, x1, y1, x2, y2, x, y, speed=5): 
        if x1 == x2:
            x1 -= 10
            x2 += 10
            y1, y2 = min(y1, y2), max(y1, y2)
            return x1, y1, x2, y2
        
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
    
    # Аванпост
    def avanpost(self, x_moving, y_moving): 
        for walls in Wall.all_line_walls:
            ogran = self.ogran_line( 
                walls[0], walls[1], 
                walls[2], walls[3], 
                x_moving, y_moving
                )
            if ogran == False:
                return False
        return True

    #   Функция для отображения стен
    def draw(): 
        Wall.dom.draw()
        



