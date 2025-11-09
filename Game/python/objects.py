import pyglet
from pyglet import shapes as sh
from time import time
from mechanics import Animation
from random import choice, randint

class Player:
    def __init__(self):
        # Характеристеки игрока
        self.x, self.y = 340, 340 # Координаты спавна
        self.width = 50   # Длинна персонажа и полосы здоровья
        self.height_player = 100
        self.height_hp_player = 15
        self.time = 0
        # Характеристики здаровья
        self.hp_player_width = 15          # Количество здоровья
        self.hp_player_One = self.width / self.hp_player_width  # Длина одной еденице здаровья
        # Пакет для обединения hp_player и player
        self.pak_player = pyglet.graphics.Batch()

    def avatar(self, color=(54, 136, 181)): #Создание и отображение игрока
        self.player = sh.Rectangle(
            self.x, self.y, 
            self.width, self.height_player, 
            color, batch=self.pak_player)
        return self.player

    # hp_player игрока
    def hp_player(self, color=(255,0,0)):
        self.hp_player = sh.Rectangle(
            self.x, self.y + self.height_player, 
            self.width, self.height_hp_player, 
            color, batch=self.pak_player)
        return self.hp_player
    
    def draw(self):
        self.pak_player.draw()



class Damage:
    time = 0
    def __init__(self, player, hp_player):  # значение по умолчанию
        self.player = player
        self.hp_player = hp_player
        self.hp_player_One = Player().width / Player().hp_player_width
    # Функция для определения получаемого урона   
    def damage(self, uron, x1, y1, x2, y2, x, y):
        X = x1 - Player().width < self.player.x + x < x2
        Y = y1 - Player().height_player < self.player.y + y < y2
        kd = 0.75
        time1 = time()
        # Миханника получение урона
        if X and Y and time1 - Damage.time > kd: 
            Damage.time = time1
            self.hp_player.width -= self.hp_player_One * uron
            # Механника смерти
            if self.hp_player.width <= 0:
                self.hp_player.width = Player().width
                self.player.x = Player().x
                self.player.y = Player().y
                self.hp_player.x = Player().x
                self.hp_player.y = Player().y + Player().height_player

    
    #   Получение урона при нахождении в линии
    def damage_line(self, x1, y1, x2, y2, uron=1, x=0, y=0):
        if x1 == x2:
            x1 -= 10
            x2 += 10
            y1, y2 = min(y1, y2), max(y1, y2)
        else:
            y1 -= 10
            y2 += 10
            x1, x2 = min(x1, x2), max(x1, x2)
        self.damage(uron, x1, y1, x2, y2, x, y)

    #   Получение урона при нахождении в прямоуглоьнике
    def damage_rectangle(self, x1, y1, width, height, uron=1, x=0, y=0):
        x2 = x1 + width
        y2 = y1 + height
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        self.damage(uron, x1, y1, x2, y2, x, y)



class Zombi:
    def __init__(self, player, hp_player, screens):
        #Мне лень писать self
        #Но я напишу
        #type это тип зомби
        self.zombiBat = pyglet.graphics.Batch()
        self.zombiBatch = pyglet.graphics.Batch()
        self.width = 116
        self.height = 72
        self.xp = 100
        self.speed = 1
        self.player = player
        self.hp_player = hp_player
        self.screens = screens
        self.zombies = {} # значение в хэш таблице это хр зомби
        self.bath = []
        self.damage = Damage(self.player, self.hp_player)
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
            
            self.art = self.animation.fox(x, y, self.player.x)
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

            if self.player.x != zombis[n].x:
                if self.player.x > zombis[n].x:
                    if not n:
                        zombis = self.turn(zombis, n)
                    zombis[1].x += self.speed
                    self.zombies[zombis][0].x += self.speed
                else:
                    if n:
                        zombis = self.turn(zombis, n)
                    zombis[0].x -= self.speed
                    self.zombies[zombis][0].x -= self.speed
            
            if self.player.y != zombis[n].y:
                if self.player.y > zombis[n].y:
                    zombis[n].y += self.speed
                    self.zombies[zombis][0].y += self.speed
                else:
                    zombis[n].y -= self.speed
                    self.zombies[zombis][0].y -= self.speed

    def attack(self, impact_force=1):
        for zomby in self.zombies:
            zomby = zomby[self.zombies[zomby][2]] # Проверяет нынешнию анимация для определения параметров зомби
            self.damage.damage_rectangle(
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
    def __init__(self, player, hp_player): 
        self.player = player   
        self.hp_player = hp_player
        self.width = player.width

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
        X = x1 - Player().width < self.player.x + x < x2
        Y = y1 - Player().height_player < self.player.y + y < y2
        if X and Y:
            return False
        return True

    #   Ограничение прохаждение через прямоуглоьники
    def ogran_rectangle(self, x1, y1, width, height, x=0, y=0):
        x2, y2 = self.rectangle(x1, y1, width, height, x, y) # Переназначение переменных через функцию rectangle
        X = x1 - Player().width < self.player.x + x < x2
        Y = y1 - Player().height_player < self.player.y + y < y2
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