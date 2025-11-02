import pyglet
from pyglet import shapes as sh
from time import time
from mechanics import Animation
from random import choice, randint

class Playr:
    def __init__(self):
        # Характеристеки игрока
        self.x, self.y = 340, 340 # Координаты спавна
        self.width = 50   # Длинна персонажа и полосы здоровья
        self.height_playr = 100
        self.height_hp_playr = 15
        self.time = 0
        # Характеристики здаровья
        self.hp_playr_width = 15          # Количество здоровья
        self.hp_playr_One = self.width / self.hp_playr_width  # Длина одной еденице здаровья
        # Пакет для обединения hp_playr и playr
        self.pak_playr = pyglet.graphics.Batch()

    def avatar(self, color=(54, 136, 181)): #Создание и отображение игрока
        self.playr = sh.Rectangle(
            self.x, self.y, 
            self.width, self.height_playr, 
            color, batch=self.pak_playr)
        return self.playr

    # hp_playr игрока
    def hp_playr(self, color=(255,0,0)):
        self.hp_playr = sh.Rectangle(
            self.x, self.y + self.height_playr, 
            self.width, self.height_hp_playr, 
            color, batch=self.pak_playr)
        return self.hp_playr
    
    def draw(self):
        self.pak_playr.draw()



class Damag:
    time = 0
    def __init__(self, playr, hp_playr):  # значение по умолчанию
        self.playr = playr
        self.hp_playr = hp_playr
        self.hp_playr_One = Playr().width / Playr().hp_playr_width
    # Функция для определения получаемого урона   
    def damag(self, uron, x1, y1, x2, y2, x, y):
        X = x1 - Playr().width < self.playr.x + x < x2
        Y = y1 - Playr().height_playr < self.playr.y + y < y2
        kd = 0.75
        time1 = time()
        # Миханника получение урона
        if X and Y and time1 - Damag.time > kd: 
            Damag.time = time1
            self.hp_playr.width -= self.hp_playr_One * uron
            # Механника смерти
            if self.hp_playr.width <= 0:
                self.hp_playr.width = Playr().width
                self.playr.x = Playr().x
                self.playr.y = Playr().y
                self.hp_playr.x = Playr().x
                self.hp_playr.y = Playr().y + Playr().height_playr

    
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
    def __init__(self, playr, hp_playr, screens):
        #Мне лень писать self
        #Но я напишу
        #type это тип зомби
        self.zombiBat = pyglet.graphics.Batch()
        self.zombiBatch = pyglet.graphics.Batch()
        self.width = 116
        self.height = 105
        self.color = (21, 110, 100)
        self.xp = 100
        self.speed = 1
        self.playr = playr
        self.hp_playr = hp_playr
        self.screens = screens
        self.zombies = {} # значение в хэш таблице это хр зомби
        self.bath = []
        self.damag = Damag(self.playr, self.hp_playr)
        self.animation = Animation()

    def turn(self, zombis, n):
        if n:
            zombis[1].batch = None
            self.zombies[zombis][2] = 0
            zombis[0].x = zombis[1].x
            zombis[0].y = zombis[1].y
            zombis[0].batch = self.zombiBat
            return zombis
        
        zombis[0].batch = None
        self.zombies[zombis][2] = 1
        zombis[1].x = zombis[0].x
        zombis[1].y = zombis[0].y
        zombis[1].batch = self.zombiBat
        return zombis

    def spawn(self, isSpawn=True):  
        if isSpawn:
            if choice((0, 1)):
                y = randint(0, self.screens.height)
                x = choice((0, self.screens.width))
            else:
                x = randint(0, self.screens.width)
                y = choice((0, self.screens.height))
            
            self.art = self.animation.fox(x, y, self.playr.x - x)
            self.art[0].batch = self.zombiBat
            zombi_key = self.art
            self.zombies[zombi_key] = [sh.Rectangle(
                x, y + self.height, 
                self.width, 8, 
                batch=self.zombiBat, color=(255, 0, 0)
                ), self.width / self.xp, 0]
            
        print(len(self.zombies))

    def moving(self):
        for zombis in self.zombies:
            n = self.zombies[zombis][2]

            if self.playr.x != zombis[n].x:
                if self.playr.x > zombis[n].x:
                    if not n:
                        zombis = self.turn(zombis, n)
                    zombis[1].x += self.speed
                    self.zombies[zombis][0].x += self.speed
                else:
                    if n:
                        zombis = self.turn(zombis, n)
                    zombis[0].x -= self.speed
                    self.zombies[zombis][0].x -= self.speed
            
            if self.playr.y != zombis[n].y:
                if self.playr.y > zombis[n].y:
                    zombis[n].y += self.speed
                    self.zombies[zombis][0].y += self.speed
                else:
                    zombis[n].y -= self.speed
                    self.zombies[zombis][0].y -= self.speed

    def attack(self, impact_force=1):
        for zomby in self.zombies:
            zomby = zomby[self.zombies[zomby][2]] # Проверяет нынешнию анимация для определения параметров зомби
            self.damag.damag_rectangle(
                zomby.x, zomby.y, 
                zomby.width, zomby.height, 
                impact_force
                )

    def draw(self):
        self.zombiBat.draw()

class Wall: 
    # Координаты стен для отображения 
    left_wall = (240, 230, 240, 490, (255, 255, 255))
    right_wall = (480, 230, 480, 490, (255, 255, 255))
    niz_wall = (350, 240, 490, 240, (255, 255, 255))
    verh_wall = (230, 480, 490, 480, (255, 255, 255))
    # Координаты чегото наносящего урон
    spike1 = (200, 200, 20, 20, (111,111,111))
    # Ширина стен
    width_wall = 20
    # Пакет данных со всеми стенами
    dom = pyglet.graphics.Batch() 

    all_walls_in_forest = {
        left_wall: None, 
        right_wall: None, 
        niz_wall: None, 
        verh_wall: None
        }
    
    all_spikes_in_forest = {
        spike1: None
        }

    #   Отображение стен (смотри на названия)
    def __init__(self, playr, hp_playr): 
        self.playr = playr   
        self.hp_playr = hp_playr
        self.width = playr.width

        for line_wall in self.all_walls_in_forest:
            self.all_walls_in_forest[line_wall] = sh.Line(
                line_wall[0], line_wall[1], 
                line_wall[2], line_wall[3], 
                color=line_wall[4], thickness=self.width_wall, 
                batch=self.dom
                )
        
        for recta_wall in self.all_spikes_in_forest:
            self.all_spikes_in_forest[recta_wall] = sh.Rectangle(
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
        X = x1 - Playr().width < self.playr.x + x < x2
        Y = y1 - Playr().height_playr < self.playr.y + y < y2
        if X and Y:
            return False
        return True

    #   Ограничение прохаждение через прямоуглоьники
    def ogran_rectangle(self, x1, y1, width, height, x=0, y=0):
        x2, y2 = self.rectangle(x1, y1, width, height, x, y) # Переназначение переменных через функцию rectangle
        X = x1 - Playr().width < self.playr.x + x < x2
        Y = y1 - Playr().height_playr < self.playr.y + y < y2
        if X and Y:
            return False
        return True
    
    # Все стены
    def all_walls(self, x_moving, y_moving): 
        for walls in Wall.all_walls_in_forest:
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
        

# Доделай

mugs = {}
class Ognestrel:
    def __init__(self, playr, zombi, damag=10, MaxMugsNum=10, mugsType="common", type=None, isPist=True, mugsNow=100, kd=0.5, mugSpeed=99):
        self.ognTypes={}
        if not type or type not in self.ognTypes:
            self.bat = pyglet.graphics.Batch()
            self.damag = damag
            self.zombi = zombi
            self.MaxMugsNum = MaxMugsNum
            self.mugsType = mugsType
            self.playr = playr
            self.pist = pyglet.shapes.Line(
                playr.x, playr.y + 50, 
                playr.x - 10, playr.y + 50, 
                batch = self.bat
                )
            self.x = playr.x
            self.y = playr.y + self.playr.height / 3
            self.x2 = playr.x - 10
            self.y2 = self.y
            self.isPist = isPist
            self.mugsNum = MaxMugsNum
            self.AllmugsLab = pyglet.text.Label(
                str(mugsNow - MaxMugsNum), 
                650, 650, color=(255, 255, 0), batch = self.bat
                )
            self.kd = kd
            self.mugsInLab = pyglet.text.Label(
                str(MaxMugsNum) + "/" + str(MaxMugsNum), 
                650, 690, color=(255, 255, 0), batch = self.bat
                )
            self.time = 0
            self.mugSpeed = mugSpeed

            
    def shot(self):
        global mugs
        if self.time <= time() and self.mugsNum != 0:
            now, space = self.mugsInLab.text.split("/")
            self.mugsInLab.text = str(int(now) - 1) + "/" + space
            self.mugsNum -= 1
            self.time = time() + self.kd
            mx, my = self.x2, self.y2
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
            mug = pyglet.shapes.Rectangle(mx, my, 4, 2, color = (250, 250, 0), batch = self.bat)
            mugs[mug] = (x, y)
            return mug

    def pulaMoving(self, x, y):
        self.pist.x = x 
        self.pist.y = y      

    def recharge(self):
        if self.MaxMugsNum <= int(self.AllmugsLab.text):
            now = int(self.mugsInLab.text.split("/")[0])
            self.AllmugsLab.text = str(int(self.AllmugsLab.text) - (self.MaxMugsNum - int(now)))
            self.mugsNum = self.MaxMugsNum
            self.mugsInLab.text = str(str(self.mugsNum) + "/" + self.mugsInLab.text.split("/")[1])

    def damage(self):
        zombie = self.zombi.zombies
        mugsToDel = []
        for i in mugs:
            zombToDel = []
            for ii in zombie:
                try:
                    x, y, x1, y1 = i.x, i.y, i.x + i.width, i.y + i.height
                    zx, zy, zx1, zy1 = ii.x, ii.y, ii.x + ii.width, ii.y + ii.height
                    if ((zy1 >= y1 > zy) or (zy1 >= y > zy)) and ((zx1 >= x1 > zx) or (zx1 >= x > zx)):
                        mugsToDel.append(i)
                        rest, xp = zombie[ii]
                        rest.width -= xp * self.damag
                        #self.toDel.append(i)
                        if rest.width <= 0:
                            zombToDel.append(ii)
                        break
                except AttributeError:
                    break
            for ii in zombToDel:
                zombie.pop(ii)
                ii.delete()
        for i in mugsToDel:
            i.delete()
            mugs.pop(i)

    def draw(self):
        self.bat.draw()






