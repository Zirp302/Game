import pyglet
from pyglet import shapes as sh
from time import time
from mechanics import Animation
from random import choice, randint


all_batch = pyglet.graphics.Batch()
#_____Игрок________________________________________________________________________________#

class Player:
    def __init__(self, screens):
        # Игровые параметры
        self.x_spawn = 0
        self.y_spawn = 0
        self.time = 0
        self.kd = 0.75

        # Параметры сущности
        self.color_body = (54, 136, 181)
        self.width = 50
        self.height = 100
        
        # Параметры полоски HP 
        self.color_hp = (255, 0, 0)
        self.height_hp = 50
        self.width_hp = 400
        self.x_hp = 200
        self.y_hp = 600
        self.hp_quantity = 15

        self.screens = screens
        self.screens_width = screens.width
        self.screens_height =  screens.height

    def hp(self):
        self.hp_quantity = self.hp_quantity
        self.width_one_hp = self.width_hp / self.hp_quantity
        self.hp_player = sh.Rectangle(
            self.x_hp, self.y_hp, 
            self.width_hp, self.height_hp, 
            self.color_hp, batch=all_batch, 
            group = pyglet.graphics.Group(993)
            )

    def body(self): # Создание существа
        self.body_player = sh.Rectangle(
            self.x_spawn, self.y_spawn, 
            self.width, self.height, 
            self.color_body, batch=all_batch
            )

    def damage(self, x1, y1, width_threat, height_threat, uron=1):
        # Распределение крайних точек атакующего обекта
        x2 = x1 + width_threat
        y2 = y1 + height_threat
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        X = x1 - self.width < self.body_player.x < x2
        Y = y1 - self.height < self.body_player.y < y2
        time0 = time()
        time_kd = time0 - self.time > self.kd

        if X and Y and time_kd: 
            self.time = time0
            self.hp_player.width -= self.width_one_hp * uron
            if self.hp_player.width <= 0:
                self.death()

    def death(self): # Механника смерти
        # Возраждение игрока
        self.body_player.x = self.x_spawn
        self.body_player.y = self.x_spawn
        # Возполнение hp
        self.hp_player.width = self.width_hp
        # Нож
        self.knife.x = self.body_player.x + (self.height // 2) 
        self.knife.y = self.body_player.y + self.width
    
    #   Передвижеие игрока и его полоски жизни
    def moving(self, x, y, all_walls):
        # left - линия огранияения ухода влево
        # right - линия огранияения ухода вправо
        # bottom - линия огранияения ухода вниз
        # top - линия огранияения ухода вверх
        left = 0
        right = self.screens_width - self.width 
        bottom = 0
        top = self.screens_height - self.height - self.hp_player.height

        map_x = left < self.body_player.x + x < right
        map_y = bottom < self.body_player.y + y < top

        if all_walls:
            if map_x:
                self.body_player.x += x
                self.knife.x += x

            if map_y:
                self.body_player.y += y
                self.knife.y += y
        
    def weapion(self):
        self.knife = sh.Rectangle(
            self.body_player.x + (self.height // 2), 
            self.body_player.y + self.width,
            40, 15, color=(133, 133, 133)
            )
        print(9)





#_____Зомби________________________________________________________________________________#

class Zombi:
    def __init__(self, player, screens):
        #Мне лень писать self
        #Но я напишу
        #type это тип зомби
        self.width = 116
        self.height = 72
        self.xp = 100
        self.speed = 1
        self.player = player
        self.player_body = player.body_player
        self.kd = 1
        
        self.height_hp = 15
        self.hp_quantity = 1
        self.hp_quantity = self.hp_quantity
        self.width_one_hp = self.width / self.hp_quantity

        self.screens = screens
        self.zombies = {} # значение в хэш таблице это хр зомби
        self.bath = []
        self.animation = Animation()


    def spawn(self, isSpawn=True):  
        if len(self.zombies) > 0:
            isSpawn = False
        
        if isSpawn:
            if choice((False, True)):
                y = randint(0, self.screens.height)
                x = choice((0, self.screens.width))
            else:
                x = randint(0, self.screens.width)
                y = choice((0, self.screens.height))
            
            self.art = self.animation.fox(x, y)
            self.art[0].batch = all_batch
            self.zombies[self.art] = [
                sh.Rectangle(
                    x, y + self.height, 
                    self.width, 8, 
                    batch=all_batch, color=(255, 0, 0)
                ), self.width / self.xp, 0, 0
                ]
            

    def turn(self, zombis, n):
        if n:
            zombis[0].batch = None
            self.zombies[zombis][2] = 1
            zombis[1].x = zombis[0].x
            zombis[1].y = zombis[0].y
            zombis[1].batch = all_batch
            return zombis
        
        zombis[1].batch = None
        self.zombies[zombis][2] = 0
        zombis[0].x = zombis[1].x
        zombis[0].y = zombis[1].y
        zombis[0].batch = all_batch
        return zombis
    
    def moving(self):
        for zombis in self.zombies:
            n = self.zombies[zombis][2]
            zombis_ser_x = zombis[n].x + zombis[n].width // 2
            player_ser_x = self.player_body.x + self.player_body.width // 2

            # Передвижение по Х
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

            # Передвижение по У
            if self.player_body.y > zombis[n].y + 5:
                zombis[n].y += self.speed 
                self.zombies[zombis][0].y += self.speed
            elif self.player_body.y < zombis[n].y - 5:
                zombis[n].y -= self.speed 
                self.zombies[zombis][0].y -= self.speed
            
    
    def damag(self, x1, y1, width, height):
        for zomby_one in self.zombies:
            hp_zomby = self.zombies[zomby_one][0]
            zomby = zomby_one[self.zombies[zomby_one][2]] # Проверяет нынешнию анимация для определения параметров зомби
            x2 = x1 + width
            y2 = y1 + height

            x_zomb = zomby.x
            y_zomb = zomby.y

            X = x1 - zomby.width < x_zomb < x2 
            Y = y1 - zomby.height < y_zomb < x2 

            
            time0 = time()
            zomby_time = self.zombies[zomby_one][3]
            time_kd = time0 - zomby_time > self.kd
            if X and Y and time_kd:
                self.zombies[zomby_one][3] = time0
                hp_zomby.width -= self.width_one_hp
                
                if hp_zomby.width <= 0:
                    zomby_one[0].batch = None
                    zomby_one[1].batch = None
                    self.zombies.pop(zomby_one)
                    del zomby_one
                    print('Лиса умирла от психической травмы')
                    break


    def attack(self, impact_force=1):
        for zomby in self.zombies:
            zomby = zomby[self.zombies[zomby][2]] # Проверяет нынешнию анимация для определения параметров зомби
            self.player.damage(
                zomby.x, zomby.y, 
                zomby.width, zomby.height,
                impact_force
                )


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
                batch=all_batch
                )
        
        for recta_wall in self.all_spikes_in_forest:
            self.all_spikes_in_forest[recta_wall] = sh.Rectangle(
                recta_wall[0], recta_wall[1], 
                recta_wall[2], recta_wall[3], 
                color=recta_wall[4], batch=all_batch
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


