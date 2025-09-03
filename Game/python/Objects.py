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

#Если объекты для прорисовки не добавить во что то глобальное то они не прорисуются
class Pl:
    def __init__(self, x=100, y=100, width=25, height=25, color={54,136,181}, xp=100):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.color = color
        self.playr = sh.Rectangle(x, y, width, height, color)
        self.xp=pyglet.text.Label(str(xp),20,690,color=(255,0,0))


    def pl_moving(self, x, y):
        if 0 < x + self.playr.x < 721 - self.w:
            self.playr.x += x
            self.x += x
        if 0 < y + self.playr.y < 721 - self.w:
            self.playr.y += y
            self.y += y
    #Прорисовка происходит ТОЛЬКО в функции с названием on_draw 
bat=pyglet.graphics.Batch()
class Zombi:
    def __init__(self,playr, batch=bat, w=10, h=10, col = {21, 110, 100}, type=None, xp=100, speed=1, spawnSpeed=1/2, damage=10, attackSpeed=1/2):
        #Мне лень писать self
        #Но я напишу
        #type это тип зомби
        self.w=w
        self.h=h
        self.col=col
        self.xp=xp
        self.batch=batch
        self.speed=speed
        self.spawnSpeed=spawnSpeed
        self.damage=damage
        self.playr=playr
        self.attackSpeed=attackSpeed
    def spawn(self,dt=2,isSpawn=True):
        if isSpawn:
            #зомби спавнятся на краю карты значит одна из координат должна быть равна нулю или 720
            coord=r(0,720)
            coord1=random.choice((0,720))
            global zombies
            if not r(0,1):
                #print(1,coord,coord1)
                zombies[(sh.Rectangle(coord,coord1,self.w,self.h,self.col,self.batch))] = 100
                print(coord,coord1,self.col)
            else:
                #print(2,coord1,coord)
                #зомбей справа  и сверху видно не было поэтому я думал что спaвн почему то не работает
                zombies[(sh.Rectangle(coord1,coord,self.w,self.h,self.col,self.batch))] = 100
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
                    if self.playr.x == i.x and self.playr.y == i.y:
                        self.playr.xp.text = str(int(self.playr.xp.text) - self.damage)
                        if int(self.playr.xp.text) <= 0:
                            raise OutOfXpError