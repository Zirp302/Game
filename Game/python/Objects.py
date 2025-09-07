import pyglet
import time
from pyglet import shapes as sh
from pyglet.window.key import *
from random import randint as r
import random
class OutOfXpError(Exception):
    pass
zombies={}
spawnSpeed=1/2
zombiBat=pyglet.graphics.Batch()

#Если объекты для прорисовки не добавить во что то глобальное то они не прорисуются
"""
Файл для создания обектов и их вывода пряма тут 
"""

class Pl:
    # Характеристеки самого игрока
    x=360,
    y=360,
    width=50,
    height=100,
    color=(54, 136, 181),
    pl = pyglet.graphics.Batch(),
    xp=pyglet.text.Label()
    def playr(self): #Создание и отображение игрока
        self.playr = sh.Rectangle(Pl.x, Pl.y, Pl.width, Pl.height, Pl.color, batch=Pl.pl)
        return self.playr

    # HP игрока
    def HP(self):
        self.HP_playr = 5
        self.HP_One = Pl.width / self.HP_playr
        self.Polosa = self.HP_playr * self.HP_One # Полоска HP
        self.HP = sh.Rectangle(Pl.x, Pl.y + Pl.height, self.Polosa, 15, color=(255,0,0), batch=Pl.pl)
        return self.HP

    def draw(): # Отрисовка пакета данных с игроком и его полоской так как они должны передвигаться одновременно и одинаково
        Pl.pl.draw() 


class Stena: # Характеристики стен для их отображения
    wind_width, wind_height = (720, 720)
    LeftNiz_X = wind_width / 2 - 120
    LeftNiz_Y =  wind_height / 2 - 120
    LeftVerh_X = wind_width / 2 - 120
    LeftVerh_Y =  wind_height / 2 + 120

    RightNiz_X = wind_width / 2 + 120
    RightNiz_Y =  wind_height / 2 - 120
    RightVerh_X = wind_width / 2 + 120
    RightVerh_Y =  wind_height / 2 + 120

    Shir_S = 20
    left_S = (
        LeftNiz_X, 
        LeftNiz_Y - Shir_S / 2,
        LeftVerh_X,
        LeftVerh_Y + Shir_S / 2
    )
    right_S = (
        RightNiz_X, 
        RightNiz_Y - Shir_S / 2,
        RightVerh_X, 
        RightVerh_Y + Shir_S / 2
    )
    verh_S = (
        LeftVerh_X - Shir_S / 2, 
        LeftVerh_Y, 
        RightVerh_X + Shir_S / 2,
        RightVerh_Y
    )
    niz_S = (
        LeftNiz_X + 120 - Shir_S / 2,
        LeftNiz_Y, 
        RightNiz_X + Shir_S / 2,
        RightNiz_Y
    )
    
    dom = pyglet.graphics.Batch() # Пакет данных со всеми стенами

    def __init__(self): # Отображение стен (смотри на названия какая это стена)
        self.wall_left = sh.Line(Stena.left_S[0], Stena.left_S[1], 
                                Stena.left_S[2], Stena.left_S[3], 
                                thickness=Stena.Shir_S, batch=Stena.dom)

        self.wall_right = sh.Line(Stena.right_S[0], Stena.right_S[1], 
                                Stena.right_S[2], Stena.right_S[3], 
                                thickness=Stena.Shir_S, batch=Stena.dom)

        self.wall_verh = sh.Line(Stena.verh_S[0], Stena.verh_S[1], 
                                Stena.verh_S[2], Stena.verh_S[3],
                                thickness=Stena.Shir_S, batch=Stena.dom)

        self.wall_niz = sh.Line(Stena.niz_S[0], Stena.niz_S[1], 
                                Stena.niz_S[2], Stena.niz_S[3], 
                                thickness=Stena.Shir_S, batch=Stena.dom) 
        self.shipi = sh.Rectangle(200, 200, 20, 20, color=(111,111,111), batch=Stena.dom)

    def draw(self): # Пакет для отображения стен
        Stena.dom.draw()

    #Прорисовка происходит ТОЛЬКО в функции с названием on_draw 


class Zombi:
    def __init__(self,playr, batch=zombiBat, w=10, h=10, col = {21, 110, 100}, type=None, xp=100, speed=1, spawnSpeed=1/2,damage=10):
        #Мне лень писать self
        #Но я напишу
        #type это тип зомби
        self.w=w
        self.h=h
        self.col=col
        self.xp=xp
        self.batch=batch
        self.speed=speed
        self.spawSpeed=spawnSpeed
        self.damage=damage
        self.playr=playr

    def spawn(dt=2,isSpawn=True):
        if isSpawn:
            global zombiBat
            #зомби спавнятся на краю карты значит одна из координат должна быть равна нулю или 720
            coord=r(0,720)
            coord1=random.choice((0,720))
            global zombies
            if r(0,1) == 0:
                #print(1,coord,coord1)
                zombies[(sh.Rectangle(coord, coord1, 25, 25, (21,110,100), batch=zombiBat))] = 100
            else:
                #print(2,coord1,coord)
                #зомбей справа  и сверху видно не было поэтому я думал что спaвн почему то не работает
                zombies[(sh.Rectangle(coord1,coord, 25, 25, (21, 110, 100), batch=zombiBat))] = 100
            #значение в хэш таблице это хр зомби

    def moving(self,dt=1/60):
            if zombies:
        #зачем я создаю функции подо все что происходит? Так надо
                for zombis in zombies.keys():
                    if self.playr.x > zombis.x:
                        zombis.x+=self.speed
                    elif self.playr.x < zombis.x:
                        zombis.x=zombis.x-self.speed
                    else:
                        pass
                    if self.playr.y > zombis.y:
                        zombis.y+=self.speed
                    elif self.playr.y < zombis.y:
                        zombis.y=zombis.y-self.speed

    def attack(self,dt=1/2,trash=None):
        #это можно было сделать и в функции zombMoving но нет надо ведь нагрузить комп кучей бесполезных функций
        if zombies:
            for i in zombies:
                #minpx,minpy,maxpx,maxpy=self.playr.x,self.playr.y,self.playr.x+self.playr.w,self.playr.y+self.playr.h
                #minzx,maxzx,minzy,maxzy=i.x,i.y,i.x+self.w,i.y+self.h
                #if (minpx<=maxzx and (minpy>=minzy or maxpy<=maxzy)) or (maxpx>=minzx and (minpy>=minzy or maxpy<=maxzy)) or (minpy<=maxzy and (minpx>=minzx or maxpx<=maxzx)) or (minpy>=maxzy and (minpx>=minzx or maxpx<=maxzx)):
                        #print(minpx,maxpx,minpy,maxpy)
                        #print(minzx,maxzx,minpy,maxzy)
                    if self.playr.x==i.x and self.playr.y==i.y:
                        self.playr.xp.text = str(int(self.playr.xp.text)-self.damage)
                        if int(self.playr.xp.text)==0:
                            raise OutOfXpError