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
    def __init__(self, x=100, y=100, width=30, height=30, color={54,136,181}, xp=100, harXp=5, speed=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.xp = pyglet.text.Label(str(xp),20,690,color=(255,0,0))
        self.pl = pyglet.graphics.Batch()
        self.harXp = harXp
        self.playr = sh.Rectangle(self.x, self.y, self.width, self.height, self.color, batch=self.pl)
        self.HP_playr = harXp
        self.HP_One = self.width / self.harXp
        self.Polosa = self.HP_playr * self.HP_One # Полоска HP
        self.HP = sh.Rectangle(self.x, self.y + self.height, self.Polosa, 15, color=(255,0,0), batch=self.pl)
        self.speed = speed
        self.phys = Physics()
        self.items = {
            "rock" : 7000
        }
        self.itemsCheck = pyglet.text.Label()
    # Характеристеки самого игрока
    def player(self): #Создание и отображение игрока
        return self.playr

    # HP игрока
    def HarXp(self):
        self.HP_playr = 5
        self.HP_One = self.width / self.harXp
        self.Polosa = self.HP_playr * self.HP_One # Полоска HP
        self.HP = sh.Rectangle(self.x, self.y + self.height, self.Polosa, 15, color=(255,0,0), batch=self.pl)
        return self.HP

    def draw(self): # Отрисовка пакета данных с игроком и его полоской так как они должны передвигаться одновременно и одинаково
        self.pl.draw() 


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

    def __init__(self, playr, uprav): # Отображение стен (смотри на названиe какая это стена)
        self.widthall_left = sh.Line(Stena.left_S[0], Stena.left_S[1], 
                                Stena.left_S[2], Stena.left_S[3], 
                                thickness=Stena.Shir_S, batch=Stena.dom)

        self.widthall_right = sh.Line(Stena.right_S[0], Stena.right_S[1], 
                                Stena.right_S[2], Stena.right_S[3], 
                                thickness=Stena.Shir_S, batch=Stena.dom)

        self.widthall_verh = sh.Line(Stena.verh_S[0], Stena.verh_S[1], 
                                Stena.verh_S[2], Stena.verh_S[3],
                                thickness=Stena.Shir_S, batch=Stena.dom)

        self.widthall_niz = sh.Line(Stena.niz_S[0], Stena.niz_S[1], 
                                Stena.niz_S[2], Stena.niz_S[3], 
                                thickness=Stena.Shir_S, batch=Stena.dom) 
        self.shipi = sh.Rectangle(200, 200, 20, 20, color=(111, 111, 111), batch=Stena.dom)
        #Только руки дошли до твоих стен это что такое вообще
        #Типы стен будем дописывать
        self.height, self.width = 50, 60
        self.walls_types = {
            "dirtWall" : {
                "xp" : 125,
                "cost" : {
                    "dirt" : 50
                },
                "color" : (80, 40, 50)
            },
            "sandWall" : {
                "xp" : 75,
                "cost" : {
                    "water" : 20,
                    "sand" : 50
                },
                "color" : (210, 183, 115)
            },
            "rockWall" : {
                "xp" : 250,
                "cost" : {
                    "rock" : 75
                },
                "color" :  (192, 192, 192)
            }
        }

        self.playr = playr
        self.uprav = uprav
        self.walls = [(self.widthall_left, "rockWall", 250), (self.widthall_right, "rockWall", 250), (self.widthall_niz, "rockWall", 250), (self.widthall_verh, "rockWall", 250)]
        self.wallTypeNow = "rockWall"
    def draw(self): # Пакет для отображения стен
        Stena.dom.draw()

    def walls_creating(self):
        for i in self.walls_types[self.wallTypeNow]["cost"]:
            for ii in self.playr.items:
                if ii == i and self.playr.items[ii] >= self.walls_types[self.wallTypeNow]["cost"]:
                    self.playr.items[ii] - self.walls_types[self.wallTypeNow]["cost"][i]
                    #Ну хотя бы не 5 вложенных циклов
                    self.walls.append(sh.Rectangle(self.playr.x + self.playr.width, self.playr.y, self.walls_types[self.wallTypeNow]["width"] if "width" in self.walls_types[self.wallTypeNow].keys() else self.width, self.walls_types[self.wallTypeNow]["height"] if "height" in self.walls_types[self.wallTypeNow].keys() else self.height, self.walls_types[self.wallTypeNow]["color"], batch=self.dom))
                    #Вот это я конечно УДОБНО сделал да?
    def return_walls(self):
        return self.walls

    #Прорисовка происходит ТОЛЬКО в функции с названием on_draw 
class Walls:
    #Зачем еще один класс для стен? ЗАЧЕМ?!
    def __init__(self, type, playr, uprav, w=10, h=10):
        self.types = {
            "dirtWall" : {
                "xp" : 50,
                "cost" : {
                    "dirt" : 5
                }
            },
            "sandWall" : {
                "xp" : 25,
                "cost" : {
                    "water" : 2,
                    "sand" : 5
                }
            }
        }
        self.width = w
        self.height = h
        self.playr = playr
        self.uprav = uprav

class Zombi:
    def __init__(self, playr, plrUprv, batch=zombiBat, width=35, height=35, col={21, 110, 100}, type=None, xp=100, speed=1, spawnSpeed=2, damage=10):
        #Мне лень писать self
        #Но я напишу
        #type это тип зомби
        self.width = width
        self.height = height
        self.col = col
        self.xp = xp
        self.batch = batch
        self.speed = speed
        self.spawSpeed = spawnSpeed
        self.damage = damage
        self.playr = playr
        self.plrUpr = plrUprv
        self.phys = Physics()

    def spawn(self, dt=2, isSpawn=True):      # перенеси функцию спавн в update не делай её отдельно без надобности
        if isSpawn:
            #зомби спавнятся на краю карты значит одна из координат должна быть равна нулю или 720
            coord = r(0,720)
            coord1 = random.choice((0,720))
            if r(0,1) == 0:
                #print(1,coord,coord1)
                zombies[(sh.Rectangle(coord, coord1, self.width, self.height, (21, 110, 100), batch=zombiBat))] = (sh.Rectangle(coord, coord1 + self.height, self.width, 4, batch=zombiBat, color=(255, 0, 0)), self.width / self.xp)
            else:
                #print(2,coord1,coord)
                #зомбей справа  и сверху видно не было поэтому я думал что спaвн почему то не работает
                zombies[(sh.Rectangle(coord1, coord, self.width, self.height, (21, 110, 100), batch=zombiBat))] = (sh.Rectangle(coord1, coord + self.height, self.width, 4, batch=zombiBat, color=(255, 0, 0)), self.width / self.xp)
            #значение в хэш таблице это хр зомби

    def moving(self, dt=1/60):
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
        zombies[sh.Rectangle(x, y, width, height, color=self.col, batch=zombiBat)] = (sh.Rectangle(x, y + height, width, 3, color=(255,0,0), batch=zombiBat), self.width / 100)


                        
    def attack(self, dt=1/2, trash=None):
        #это можно было сделать и в функции zombMoving но нет надо ведь нагрузить комп кучей бесполезных функций
        if zombies:
            for i in zombies:
                x, y, x1, y1 = self.playr.x, self.playr.y, self.playr.x + self.playr.width, self.playr.y + self.playr.height
                zx, zy, zx1, zy1 = i.x, i.y, i.x + i.width, i.y + i.height
                #print((zy1 , y1 , zy), (zy1 , y , zy), (zx1 , x1 , zx), (zx1 , x , zx))
                #print(((zy1 >= y1 > zy), (zy1 >= y > zy)), ((zx1 >= x1 > zx), (zx1 >= x > zx)))
                #print(x,y,x1,y1)
                #print(zx,zy,zx1,zy1)
                #if (minpx<=maxzx and (minpy>=minzy or maxpy<=maxzy)) or (maxpx>=minzx and (minpy>=minzy or maxpy<=maxzy)) or (minpy<=maxzy and (minpx>=minzx or maxpx<=maxzx)) or (minpy>=maxzy and (minpx>=minzx or maxpx<=maxzx)):
                        #print(minpx,maxpx,minpy,maxpy)
                        #print(minzx,maxzx,minpy,maxzy)
                    #if self.playr.x==i.x and self.playr.y==i.y:
                        #self.playr.xp.text = str(int(self.playr.xp.text)-self.damage)
                if ((zy1 >= y1 > zy) or (zy1 >= y > zy)) and ((zx1 >= x1 > zx) or (zx1 >= x > zx)):
                        print("yes we gonna think about two chairs")
                        self.playr.HP.width -= self.playr.HP_One
                        #if int(self.playr.xp.text)==0:
                        if self.playr.HP.width <= 0:
                            """self.HP.width = self.playr.width
                            self.playr.x = self.playr.x
                            self.playr.y = self.playr.y
                            self.HP.x = self.playr.x
                            self.HP.y = self.playr.y + self.playr.height"""
                            raise OutOfXpError
                            
                    



bat = pyglet.graphics.Batch()
mugs = {}
class Ognestrel:
    def __init__(self, playr, phot="ognestrel.png", damag=10, MaxMugsNum=10, mugsType="common", type=None, isPist=True, bat=bat, mugsNow=100, kd=0.2, mugSpeed=15):
        self.ognTypes={}
        if not type or type not in self.ognTypes:
            self.damag = damag
            self.MaxMugsNum = MaxMugsNum
            self.mugsType = mugsType
            self.playr = playr
            #photo = pyglet.image.load(phot, open(phot, "br"))
            self.pist = pyglet.shapes.Line(playr.x, playr.y + self.playr.height / 3, playr.x - 10, playr.y + self.playr.height / 3)
            #pyglet.sprite.Sprite(photo, playr.x, playr.y+3)
            self.x = playr.x
            self.y = playr.y + self.playr.height / 3
            self.x2 = playr.x - 10
            self.y2 = self.y
            self.isPist = isPist
            self.bat = bat
            self.mugsNum = MaxMugsNum
            self.AllmugsLab = pyglet.text.Label(str(mugsNow - MaxMugsNum), 650, 650, color=(255, 255, 0))
            self.kd = kd
            self.mugsInLab = pyglet.text.Label(str(MaxMugsNum) + "/" + str(MaxMugsNum), 650, 690, color=(255, 255, 0))
            self.time = 0
            self.mugSpeed = mugSpeed
            
    def shot(self):
        global mugs
        global bat
        if self.time <= time.time() and self.mugsNum !=0:
            now, space = self.mugsInLab.text.split("/")
            self.mugsInLab.text = str(int(now) - 1) + "/" + space
            self.mugsNum -= 1
            self.time = time.time() + self.kd
            mx, my = self.x2, self.y2
            #print(self.x, self.x2, self.y, self.y2)
            if self.y == self.y2:
                if self.x < self.x2:
                    x, y = self.mugSpeed, 0
                else:
                    x, y = -self.mugSpeed, 0
            else:
                if self.y < self.y2:
                    x, y = 0, self.mugSpeed
                else:
                    x, y = 0, -self.mugSpeed
            mug = pyglet.shapes.Rectangle(mx, my, 4, 2, color = [250, 250, 0], batch = bat)
            mugs[mug] = (x, y)
            return mug

    def pulaMoving(self, dt):
        self.toDel=[]
        for i in mugs:
            try:
                if not i.x in [720, 0] and not i.y in [720, 0]:
                    i.x += mugs[i][0]
                    i.y += mugs[i][1]
                else:
                    self.toDel.append(i)
                    break
            except AttributeError:
                continue
        for i in self.toDel:
            mugs.pop(i)
            i.delete()
    def recharge(self):
        if self.MaxMugsNum <= int(self.AllmugsLab.text):
            now = int(self.mugsInLab.text.split("/")[0])
            self.AllmugsLab.text = str(int(self.AllmugsLab.text) - (self.MaxMugsNum - int(now)))
            self.mugsNum = self.MaxMugsNum
            self.mugsInLab.text = str(str(self.mugsNum) + "/" + self.mugsInLab.text.split("/")[1])
    def damage(self, dt):
        mugsToDel = []
        for i in mugs:
            zombToDel = []
            for ii in zombies:
                try:
                    x, y, x1, y1 = i.x, i.y, i.x + i.width, i.y + i.height
                    zx, zy, zx1, zy1 = ii.x, ii.y, ii.x + ii.width, ii.y + ii.height
                    if ((zy1 >= y1 > zy) or (zy1 >= y > zy)) and ((zx1 >= x1 > zx) or (zx1 >= x > zx)):
                        mugsToDel.append(i)
                        rest, xp = zombies[ii]
                        rest.width -= xp * self.damag
                        #self.toDel.append(i)
                        if rest.width <= 0:
                            zombToDel.append(ii)
                        break
                except AttributeError:
                    break
            for ii in zombToDel:
                zombies.pop(ii)
                ii.delete()
        for i in mugsToDel:
            i.delete()
            mugs.pop(i)
    def Rotat(self, keys):
        if keys[RIGHT]:
            self.pist.x = self.playr.x + self.playr.width
            self.pist.y = self.playr.y + self.playr.height / 3
            self.pist.x2 = self.pist.x + 10
            self.pist.y2 = self.pist.y
        if keys[LEFT]:
            self.pist = pyglet.shapes.Line(self.playr.x, self.playr.y + self.playr.height / 3, self.playr.x - 10, self.playr.y + self.playr.height / 3)
        if keys[UP]:
            self.pist = sh.Line(self.playr.x + self.playr.width / 3, self.playr.y + self.playr.height, self.playr.x + self.playr.width / 3, self.playr.y + self.playr.height + self.playr.HP.height + 3)
        if keys[DOWN]:
            self.pist = sh.Line(self.playr.x + self.playr.width / 3, self.playr.y, self.playr.x + self.playr.width / 3, self.playr.y - 10)
        self.x = self.pist.x
        self.y = self.pist.y
        self.x2 = self.pist.x2
        self.y2 = self.pist.y2
        """if self.pist.x != self.x or self.pist.y != self.y or self.pist.x2 != self.x2 or self.pist.y2 != self.y2:
            print("jjj")"""

        """if keys[RIGHT]:
            if self.playr.x <= self.x <= self.playr.x + self.playr.hseeight:
                if self.playr.x == self.x:
                    self.x += 1
                    self.pist.x += 1
                elif self.playr.x + self.playr.width == self.x:
                    self.x -= 1
                    self.pist.x -= 1

        if keys[LEFT]:
            if self.playr.x <= self.x <= self.playr.x + self.playr.height:
                if self.playr.x == self.x:
                    self.x -= 1
                    self.pist.x -= 1
                elif self.playr.x + self.playr.width == self.x:
                    self.x += 1
                    self.pist.x += 1"""           
class Physics():
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
        
    # Ограничение прохаждение через линии
    def ogran_line(self, playr, x1, y1, x2, y2, x=0, y=0):
        # Переназначение переменных согласно функции line
        x1, y1, x2, y2 = self.line(x1, y1, x2, y2, x, y) 
        X = x1 - playr.w < playr.x + x < x2
        Y = y1 - playr.height < playr.y + y < y2
        if X and Y:
            return False
        return True
    
    # Получение урона при прохаждение через линии
    def damag_line(self, playr, x1, y1, width, height, x=0, y=0):
        # Переназначение переменных согласно функции rectangle
        x1, y1, x2, y2 = self.line(x1, y1, x2, y2, x, y) 
        X = x1 - playr.w < playr.x + x < x2
        Y = y1 - playr.height < playr.y + y < y2
        kd = 1.25
        time1 = time.time()
        if X and Y and time1 - self.time > kd:
            self.time = time1
            print(time1, self.time)
            self.HP.width -= self.playr.HP_One
            if self.HP.width <= 0:
                self.HP.width = self.playr.w
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
    def ogran_rectangle(playr, x1, y1, width, height, x=0, y=0):
        # Переназначение переменных согласно функции rectangle
        x2, y2 = x1 + width, x2 + height
        X = x1 - playr.w < playr.x + x < x2
        Y = y1 - playr.height < playr.y + y < y2
        if X and Y:
            return False
        return True
    
    # Получение урона при прохаждение через прямоуглоьники
    def damag_rectangle(self, playr, x1, y1, width, height, x=0, y=0):
        # Переназначение переменных согласно функции rectangle
        x2, y2 = self.rectangle(x1, y1, width, height, x, y)
        X = x1 - playr.w < playr.x + x < x2
        Y = y1 - playr.height < playr.y + y < y2
        kd = 1.25
        time1 = time.time()
        if X and Y and time1 - self.time > kd:
            self.time = time1
            print(time1, self.time)
            playr.HP.width -= playr.HP_One
            if playr.HP.width <= 0:
                playr.HP.width = playr.width
                playr.playr.x = playr.x
                playr.playr.y = playr.y
                playr.HP.x = playr.x
                playr.HP.y = playr.y + playr.height
    

    def entering_kollision(playr, object):
        x, y, x1, y1 = playr.x, playr.y, playr.x + playr.width, playr.y + playr.height
        zx, zx1, zy, zy1 = object.x, object.y, object.x + object.width, object.y + object.height
        if ((zy1 >= y1 >= zy) or (zy1 >= y >= zy)) and ((zx1 >= x1 >= zx) or (zx1 >= x >= zx)):
            return True
        return 