import pyglet
from pyglet import shapes as sh
import time
import random
zombies={} # значение в хэш таблице это хр зомби

class Player:
    def __init__(self, x=100, y=100, width=30, height=30, color={54,136,181}, xp=100, harXp=5, speed=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.xp=pyglet.text.Label(str(xp),20,690,color=(255,0,0))
        self.pl=pyglet.graphics.Batch()
        self.harXp=harXp
        self.playr = sh.Rectangle(self.x, self.y, self.width, self.height, self.color, batch=self.pl)
        self.HP_playr = harXp
        self.HP_One = self.width / self.harXp
        self.Polosa = self.HP_playr * self.HP_One # Полоска HP
        self.HP = sh.Rectangle(self.x, self.y + self.height, self.Polosa, 15, color=(255,0,0), batch=self.pl)
        self.speed = speed
        self.items = {
            "rock" : 7000
        }
        self.itemsCheck = pyglet.text.Label()
    #В таком формате гораздо удобнее работать
    def draw(self):
        self.pl.draw()


class Damag:
    time = 0
    def __init__(self, playr, HP):  # значение по умолчанию
        self.playr = playr
        self.HP = HP
        self.HP_One = playr.width / playr.HP_playr
        
    # Функция для определения получаемого урона   
    def damag(self, uron, x1, y1, x2, y2):
        #X = x1 - self.playr.width < self.playr.x + x < x2
        #Y = y1 - self.playr.height < self.playr.y + y < y2
        kd = 0.75
        time1 = time.time()
        # Миханника получение урона
        if time1 - Damag.time > kd: 
            Damag.time = time1
            #print(uron, self.HP_One)
            self.HP.width -= self.HP_One * uron
            # Механника смерти
            if self.HP.width <= 0:
                self.HP.width = self.playr.width
                self.playr.x = self.playr.x
                self.playr.y = self.playr.y
                self.HP.x = self.playr.x
                self.HP.y = self.playr.y + self.playr.height
    
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
    def damag_rectangle(self, object, uron=1, x=0, y=0):
        """x2 = x1 + width
        y2 = y1 + height
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        self.damag(uron, x1, y1, x2, y2, x, y)"""
        x, y, x1, y1 = self.playr.x, self.playr.y, self.playr.x + self.playr.width, self.playr.y + self.playr.height
        ox, oy, ox1, oy1 = object.x, object.y, object.x + object.width, object.y + object.height
        if ((oy1 >= y1 > oy) or (oy1 >= y > oy)) and ((ox1 >= x1 > ox) or (ox1 >= x > ox)):
            self.damag(uron, x, y, x1, y1)
            #Потом накидаю комментариев

class Zombi:
    def __init__(self, playr, HP, plrUprv, width=35, height=35, color={21, 110, 100}, type=None, xp=100, speed=1, spawnSpeed=1/2, damage=10):
        #Мне лень писать self
        #Но я напишу
        #type это тип зомби
        self.zombiBat = pyglet.graphics.Batch()
        self.width = width
        self.height = height
        self.color = color
        self.xp = xp
        self.speed = speed
        self.spawSpeed = spawnSpeed
        self.damage = damage
        self.playr = playr
        self.HP = HP
        self.plrUpr = plrUprv

    def spawn(self, isSpawn=True):  
        if isSpawn:
            x = random.choice((0,720))
            y = random.randint(0,720)
            #Карта это прямоугольник 720 на 720 значит на краю карты одна из координат гарантированно 720 или 0
            #Вот этот случайный выбор которой ниже этого текста выбирает какая из координат будет являться иксом а какая игреком (ты почему то кстати удалил тот комментарий который описывал работу этого кода)
            if random.choice((0,1)):
                pass
            else:
                x1 = y
                y1 = x
                x = x1
                y = y1
            zomb = (sh.Rectangle(x, y, self.width, self.height, (21, 110, 100), batch=self.zombiBat))
            #Ключ это сам зомби а значение это прямоугольник хп зомби и значение одной единицы хп у них
            zombies[zomb] = (sh.Rectangle(x, y + self.height, self.width, 4, batch=self.zombiBat, color=(255, 0, 0)), (self.width / self.xp))

    def moving(self):
            #зачем я создаю функции подо все что происходит? Так надо
            if zombies:
                for zombis in zombies:

                    if self.playr.x > zombis.x:
                        zombis.x += self.speed
                        zombies[zombis][0].x += self.speed
                    elif self.playr.x < zombis.x:
                        zombis.x = zombis.x - self.speed
                        zombies[zombis][0].x -= self.speed
                    else:
                        pass
                    if self.playr.y > zombis.y:
                        zombis.y += self.speed
                        zombies[zombis][0].y += self.speed
                    elif self.playr.y < zombis.y:
                        zombis.y = zombis.y - self.speed
                        zombies[zombis][0].y -= self.speed
    def test(self, x, y, width, height):
        zombies[sh.Rectangle(x, y, width, height, color=self.color, batch=self.zombiBat)] = (sh.Rectangle(x, y + height, width, 3, color=(255,0,0), batch=self.zombiBat), self.width / 100)

    def attack(self, trash=None):
        #это можно было сделать и в функции zombMoving но нет надо ведь нагрузить комп кучей бесполезных функций
        if zombies:
            for i in zombies:
                x, y, x1, y1 = self.playr.x, self.playr.y, self.playr.x + self.playr.width, self.playr.y + self.playr.height
                zomb_x, zomb_y, zomb_x1, zomb_y1 = i.x, i.y, i.x + i.width, i.y + i.height
                Damag(self.playr).damag_rectangle(i)



    def draw(self):
        self.zombiBat.draw()


class Stena: 
    # Характеристики стен для отображения 
    left_S = (240, 230, 240, 490)
    right_S = (480, 230, 480, 490)
    niz_S = (350, 240, 490, 240)
    verh_S = (230, 480, 490, 480)
    # Ширина стен
    Shir_S = 20
    # Пакет данных со всеми стенами
    dom = pyglet.graphics.Batch() 

    #   Отображение стен (смотри на названия)
    def __init__(self, width): 
        """self.playr = playr
        self.HP = HP"""
        #пока что нам это не надо ну и никогда надо не будет
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
    def line(x1, y1, x2, y2, x, y, speed=5): 
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
    def ogran_line(object, x1, y1, x2, y2, x=0, y=0):
        x1, y1, x2, y2 = Stena.line(x1, y1, x2, y2, x, y) # Переназначение переменных через функцию line
        X = x1 - object.width < object.x + x < x2
        Y = y1 - object.height < object.y + y < y2
        if X and Y:
            return False
        return True

    #   Ограничение прохаждение через прямоуглоьники
    def ogran_rectangl(object, x1, y1, width, height, x=0, y=0):
        x2, y2 = Stena.rectangle(x1, y1, width, height, x, y) # Переназначение переменных через функцию rectangle
        X = x1 - object.width < object.x + x < x2
        Y = y1 - object.height < object.y + y < y2
        if X and Y:
            return False
        return True
    def avanpost(playr, x_moving, y_moving):
    #во первых передавая в качестве первых четырех аргументов распакованный список это легче читается чем твои гроомоздкие куски кода а во вторых это быстрее И лучше
        stena_l = Stena.ogran_line(playr,
                                *Stena.left_S,
                                x_moving, y_moving)
        stena_r = Stena.ogran_line(playr,
                                *Stena.right_S, 
                                x_moving, y_moving)
        stena_v = Stena.ogran_line(playr,
                                *Stena.verh_S,
                                x_moving, y_moving)
        stena_n = Stena.ogran_line(playr,
                                *Stena.niz_S,
                                x_moving, y_moving)

        return stena_v and stena_n and stena_l and stena_r

    #   Функция для отображения стен
    def draw(self): 
        Stena.dom.draw()



