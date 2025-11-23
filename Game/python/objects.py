import pyglet
from pyglet import shapes as sh
from time import time
from mechanics import Animation
from random import choice, randint


#_____Сущности_____________________________________________________________________________#

class Entitie:
    def __init__(self):
        # Игровые параметры
        self.x_spawn = 320
        self.y_spawn = 320
        self.time = 0
        self.kd = 0.75
        self.pak = pyglet.graphics.Batch()

        # Параметры сущности
        self.color_body = (54, 136, 181)
        self.width = 100
        self.height = 100
        
        # Параметры полоски HP 
        self.color_hp = (255, 0, 0)
        self.height_hp = 15
        self.x_hp = self.x_spawn
        self.y_hp = self.y_spawn + self.height
        self.hp_quantity = 15

    def hp(self):
        self.hp_quantity = self.hp_quantity
        self.width_one_hp = self.width / self.hp_quantity
        self.hp_entitie = sh.Rectangle(
            self.x_hp, self.y_hp, 
            self.width, self.height_hp, 
            self.color_hp, batch=self.pak
            )

    def body(self): # Создание существа
        self.body_entitie = sh.Rectangle(
            self.x_spawn, self.y_spawn, 
            self.width, self.height, 
            self.color_body, batch=self.pak
            )

    def damage(self, x1, y1, width_threat, height_threat, uron=1):
        # Распределение крайних точек атакующего обекта
        x2 = x1 + width_threat
        y2 = y1 + height_threat
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        X = x1 - self.width < self.body_entitie.x < x2
        Y = y1 - self.height < self.body_entitie.y < y2
        time0 = time()
        time_kd = time0 - self.time > self.kd

        if X and Y and time_kd: 
            self.time = time0
            self.hp_entitie.width -= self.width_one_hp * uron
            if self.hp_entitie.width <= 0:
                self.death()

    def death(self): # Механника смерти
        # Возраждение игрока
        self.body_entitie.x = self.x_spawn
        self.body_entitie.y = self.x_spawn
        # Возполнение hp
        self.hp_entitie.width = self.width
        self.hp_entitie.x = self.x_spawn
        self.hp_entitie.y = self.y_spawn + self.height
            

    def draw(self):
        self.pak.draw()


#_____Игрок________________________________________________________________________________#

class Player(Entitie):
    def __init__(self, screens):
        super().__init__()
        self.width = 50
        self.screens = screens
        self.screens_width = screens.width
        self.screens_height =  screens.height
    


    #   Передвижеие игрока и его полоски жизни
    def moving(self, x, y, all_walls):
        # left - линия огранияения ухода влево
        # right - линия огранияения ухода вправо
        # bottom - линия огранияения ухода вниз
        # top - линия огранияения ухода вверх
        left = 0
        right = self.screens_width - self.width 
        bottom = 0
        top = self.screens_height - self.height - self.hp_entitie.height

        map_x = left < self.body_entitie.x + x < right
        map_y = bottom < self.body_entitie.y + y < top

        if all_walls:
            if map_x:
                self.body_entitie.x += x
                self.hp_entitie.x += x

            if map_y:
                self.body_entitie.y += y
                self.hp_entitie.y += y


#_____Зомби________________________________________________________________________________#

class Zombi:
    def __init__(self, player, screens):
        #Мне лень писать self
        #Но я напишу
        #type это тип зомби
        self.batch_zombi = pyglet.graphics.Batch()
        self.width = 116
        self.height = 72
        self.xp = 100
        self.speed = 1
        self.player = player
        self.player_body = player.body_entitie

        self.screens = screens
        self.zombies = {} # значение в хэш таблице это хр зомби
        self.bath = []
        self.animation = Animation()

    def turn(self, zombis, n):
        if n:
            zombis[0].batch = None
            self.zombies[zombis][2] = 1
            zombis[1].x = zombis[0].x
            zombis[1].y = zombis[0].y
            zombis[1].batch = self.batch_zombi
            return zombis
        
        zombis[1].batch = None
        self.zombies[zombis][2] = 0
        zombis[0].x = zombis[1].x
        zombis[0].y = zombis[1].y
        zombis[0].batch = self.batch_zombi
        return zombis

    def spawn(self, isSpawn=True):  
        if isSpawn:
            if choice((0, 1)):
                y = randint(0, self.screens.height)
                x = choice((0, self.screens.width))
            else:
                x = randint(0, self.screens.width)
                y = choice((0, self.screens.height))
            
            self.art = self.animation.fox(x, y)
            self.art[0].batch = self.batch_zombi
            zombi_key = self.art
            self.zombies[zombi_key] = [
                sh.Rectangle(
                    x, y + self.height, 
                    self.width, 8, 
                    batch=self.batch_zombi, color=(255, 0, 0)
                ), self.width / self.xp, 0
                ]
            
        print(len(self.zombies))

    def moving(self):
        for zombis in self.zombies:
            n = self.zombies[zombis][2]
            zombis_ser_x = zombis[n].x + zombis[n].width // 2
            player_ser_x = self.player_body.x + self.player_body.width // 2

            if zombis_ser_x < player_ser_x - 70:
                if not n:
                    zombis = self.turn(zombis, 1)
                    n = 1
                zombis[1].x += self.speed
                self.zombies[zombis][0].x += self.speed

            elif player_ser_x < zombis_ser_x - 70:
                if n:
                    zombis = self.turn(zombis, 0)
                    n = 0
                zombis[0].x -= self.speed
                self.zombies[zombis][0].x -= self.speed


            if self.player_body.y > zombis[n].y + 5:
                zombis[n].y += self.speed 
                self.zombies[zombis][0].y += self.speed
            elif self.player_body.y < zombis[n].y - 5:
                zombis[n].y -= self.speed 
                self.zombies[zombis][0].y -= self.speed

    def attack(self, impact_force=1):
        for zomby in self.zombies:
            zomby = zomby[self.zombies[zomby][2]] # Проверяет нынешнию анимация для определения параметров зомби
            self.player.damage(
                zomby.x, zomby.y, 
                zomby.width, zomby.height,
                impact_force
                )

    def draw(self):
        self.batch_zombi.draw()


#_____Стены________________________________________________________________________________#

class Wall: 
    #   Отображение стен (смотри на названия)
    def __init__(self, player): 
        self.player = player   
        # Координаты стен для отображения 
        left_wall = (240, 230, 240, 490, (255, 255, 255))
        right_wall = (480, 230, 480, 490, (255, 255, 255))
        niz_wall = (350, 240, 490, 240, (255, 255, 255))
        verh_wall = (230, 480, 490, 480, (255, 255, 255))
        # Координаты чегото наносящего урон
        spike1 = (200, 200, 20, 20, (111,111,111))
        # Ширина стен
        self.width_wall = 20
        # Пакет данных со всеми стенами
        self.dom = pyglet.graphics.Batch() 

        self.all_walls_in_forest = {
            left_wall: None, 
            right_wall: None, 
            niz_wall: None, 
            verh_wall: None
            }
        
        self.all_spikes_in_forest = {
            spike1: None
            }

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
    def line(self, x1, y1, x2, y2, x=0, y=0, speed=5): 
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
    def rectangle(self, x1, y1, width, height, x=0, y=0, speed=5):
        x2 = x1 + width
        y2 = y1 + height
        return x2, y2

    # Проверка пересечений объектов
    def ogran(self, x, y, x1, y1, x2, y2):
        X = x1 - self.player.width < self.player.x + x < x2
        Y = y1 - self.player.height < self.player.y + y < y2
        if X and Y:
            return False
        return True
    
    def ogran_line(self, x1, y1, x2, y2, x=0, y=0):
        if x1 == x2:
            x1 -= 10
            x2 += 10
            return self.ogran(x, y, x1, y1, x2, y2)
        
        y1 -= 10
        y2 += 10
        return self.ogran(x, y, x1, y1, x2, y2)

    #   Ограничение прохаждение через прямоуглоьники
    def ogran_rectangle(self, x1, y1, width, height, x=0, y=0):
        x2 = x1 + width
        y2 = y1 + height
        return self.ogran(x, y, x1, y1, x2, y2)

    # Все стены
    def all_walls(self, x_moving, y_moving): 
        for walls in self.all_walls_in_forest:
            ogran = self.ogran_line( 
                walls[0], walls[1], 
                walls[2], walls[3], 
                x_moving, y_moving
                )
            if not ogran:
                return False
        return True

    #   Функция для отображения стен
    def draw(self): 
        self.dom.draw()


