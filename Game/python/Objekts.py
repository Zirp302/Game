import pyglet
import time
from pyglet import shapes as sh
from pyglet.window.key import *
from random import randint as r
import random
from B import OutOfXpError
zombies={}
xpB=100
#Если объекты для прорисовки не добавить во что то глобальное то они не прорисуются
class Pl:
    def __init__(self,batch, x=100, y=100, width=10, height=10, color={125,254,88}):
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

playr=Pl()
class Zombi:
    def __init__(self, x, y, batch, w=10, h=10, col = {21, 110, 100}, type=None, xp=100, speed=1):
        #Мне лень писать self
        #Но я напишу
        #type это тип зомби
        self.x=x
        self.y=y
        self.w=w
        self.col=col
        self.xp=xp
        self.batch=batch
        self.speed=speed
    def spawn(self,isSpawn):
        if isSpawn:
            #зомби спавнятся на краю карты значит одна из координат должна быть равна нулю или 720
            coord=r(0,720)
            coord1=random.choice((0,720))
            global zombies
            if r(0,1) == 0:
                #print(1,coord,coord1)
                zombies[(sh.Rectangle(coord,coord1,25,25,(21,110,100),batch=self.batch))] = 100
            else:
                #print(2,coord1,coord)
                #зомбей справа  и сверху видно не было поэтому я думал что спaвн почему то не работает
                zombies[(sh.Rectangle(coord1,coord,25,25,(21,110,100),batch=self.batch))] = 100
            #значение в хэш таблице это хр зомби
    def zombMoving(self,dt):
            if zombies:
                global playr
        #зачем я создаю функции подо все что происходит? Так надо
                for zombis in zombies.keys():
                    if playr.x > zombis.x:
                        zombis.x+=self.speed
                    elif playr.x < zombis.x:
                        zombis.x=zombis.x-self.speed
                    else:
                        pass
                    if playr.y > zombis.y:
                        zombis.y+=self.speed
                    elif playr.y < zombis.y:
                        zombis.y=zombis.y-self.speed
    def zombAttack(dt):
        #это можно было сделать и в функции zombMoving но нет надо ведь нагрузить комп кучей бесполезных функций
        if zombies:
            for i in zombies:
                if i.x in list(range(playr.x-10,playr.x+10)) and i.y in list(range(playr.y-10,playr.y+10)):
                        xpB.text = str(int(xpB.text)-10)
                        if int(xpB.text)==0:
                            raise OutOfXpError
        