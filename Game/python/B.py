import pyglet
from pyglet import shapes as sh
from pyglet.window.key import *
import random
# доки пайглета https://pyglet.readthedocs.io/en/latest/programming_guide/shapes.html
#это чтобы писать названия клавиш не указывая функцию key
# wind is a window object

xp=100
#Сори но это хп персонажа я не мог не реализовать хп если есть зомби
wind = pyglet.window.Window(width=720,height=720,caption="gameOnPyglet")
#могут ли зомби появляться
isZombSpawn=True
spawnSpeed=1/5
#Скорость появления зомбей попробуй изменить число на какое нибудь оч маленькое по типу 1/60 и тд
w = 30
h = 30
zombies = {}
drawInfuncs=[]
text = pyglet.graphics.Batch()
playr = sh.Rectangle(331, 331, w, h, color=(54, 136, 181))
zombi = pyglet.graphics.Batch()
xpB=pyglet.text.Label(str(xp),20,690,color=(255,0,0),batch=text)
#Почему хрb? Я сам не знаю
@wind.event
def on_mouse_press(x,y,button,modifiers):
    print(f"x = {x}, y = {y}")


class OutOfXpError(Exception):
    pass


l_l_v = (240, 480)
l_l_n = (240, 240)
r_r_v = (480, 480)
r_r_n = (480, 240)

Shir_S = 20
left_S = (
    min(l_l_v[0], l_l_n[0]), 
    min(l_l_n[1], l_l_v[1]) - Shir_S / 2,
    max(l_l_v[0], l_l_n[0]),
    max(l_l_n[1], l_l_v[1]) + Shir_S / 2
)
right_S = (
    min(r_r_v[0], r_r_n[0]), 
    min(r_r_v[1], r_r_n[1]) - Shir_S / 2,
    max(r_r_v[0], r_r_n[0]), 
    max(r_r_v[1], r_r_n[1]) + Shir_S / 2
)
verh_S = (
    min(r_r_v[0], l_l_v[0]) - Shir_S / 2, 
    min(r_r_v[1], l_l_v[1]), 
    max(r_r_v[0], l_l_v[0]) + Shir_S / 2,
    max(r_r_v[1], l_l_v[1])
)
niz_S = (
    min(r_r_n[0], l_l_n[0]) + 120 - Shir_S / 2, 
    min(r_r_n[1], l_l_n[1]), 
    max(r_r_n[0], l_l_n[0]) + Shir_S / 2, 
    max(r_r_n[1], l_l_n[1])
)


dom = pyglet.graphics.Batch()
wall_verh_left = sh.Line(
    left_S[0], left_S[1], 
    left_S[2], left_S[3], 
    thickness=Shir_S, batch=dom
)
wall_verh_right = sh.Line(
    right_S[0], right_S[1], 
    right_S[2], right_S[3], 
    thickness=Shir_S, batch=dom
)
wall_left_verh = sh.Line(
    verh_S[0], verh_S[1], 
    verh_S[2], verh_S[3], 
    thickness=Shir_S, batch=dom
)
wall_left_niz = sh.Line(
    niz_S[0], niz_S[1], 
    niz_S[2], niz_S[3], 
    thickness=Shir_S, batch=dom
) 

""" Ворота. Не доделано
wall_niz_left = sh.Line(100, 100, 100, 200, thickness=20, batch=dom)
wall_niz_right = sh.Line(100, 100, 100, 200, thickness=20, batch=dom)

wall_right_verh = sh.Line(100, 100, 100, 200, thickness=20, batch=dom)
wall_right_niz = sh.Line(100, 100, 100, 200, thickness=20, batch=dom)"""

def spawn(dt,isSpawn):
    if isSpawn:
        #зомби спавнятся на краю карты значит одна из координат должна быть равна нулю или 720
        coord=random.randint(0,720)
        coord1=random.choice((0,720))
        global zombies
        if random.randint(0,1) == 0:
            #print(1,coord,coord1)
            zombies[(sh.Rectangle(coord,coord1,25,25,(21,110,100),batch=zombi))] = 100
        else:
            #print(2,coord1,coord)
            #зомбей справа  и сверху видно не было поэтому я думал что спaвн почему то не работает
            zombies[(sh.Rectangle(coord1,coord,25,25,(21,110,100),batch=zombi))] = 100
        #значение в хэш таблице это хр зомби


zombSpeed=1
def zombMoving(dt):
        if zombies:
    #зачем я создаю функции подо все что происходит? Так надо
            for zombis in zombies.keys():
                if playr.x > zombis.x:
                    zombis.x+=zombSpeed
                elif playr.x < zombis.x:
                    zombis.x=zombis.x-zombSpeed
                else:
                    pass
                if playr.y > zombis.y:
                    zombis.y+=zombSpeed
                elif playr.y < zombis.y:
                    zombis.y=zombis.y-zombSpeed




def zombAttack(dt):
    #это можно было сделать и в функции zombMoving но нет надо ведь нагрузить комп кучей бесполезных функций
    if zombies:
        for i in zombies:
            if i.x in list(range(playr.x-10,playr.x+10)) and i.y in list(range(playr.y-10,playr.y+10)):
                    xpB.text = str(int(xpB.text)-10)
                    if int(xpB.text)==0:
                        raise OutOfXpError


def ogran(x1, y1, x2, y2, x, y, zonaw=w, zonah=h, speed=5): # Доделать блокировку cтенам
    if x1 == x2:
        x1 -= 10
        x2 += 10
    else:
        y1 -= 10
        y2 += 10
    #print(x1, playr.x, x, x2 )
    
    if x1 + speed - zonaw < playr.x + x < x2 and y1 + speed - zonah < playr.y + y < y2:
        return False
    return True


def pl_moving(x,y):
    stena_l = ogran(left_S[0], left_S[1], left_S[2], left_S[3], x, y)
    stena_r = ogran(right_S[0], right_S[1], right_S[2], right_S[3], x, y)
    stena_v = ogran(verh_S[0], verh_S[1], verh_S[2], verh_S[3], x, y)
    stena_n = ogran(niz_S[0], niz_S[1], niz_S[2], niz_S[3], x, y) # прочитай послание на 31 строке

    avanpost = stena_v and stena_n and stena_l and stena_r

    if 0 < x + playr.x < 721 - w and avanpost:
        playr.x += x

    
    if 0 < y + playr.y < 721 - w and avanpost : # '''прочитай послание на 31 строке'''
        playr.y += y

keys={'W': False, 'A': False, 'S': False, 'D': False}
@wind.event
def on_key_press(symbol, modifiers):
    if symbol == W:
        keys['W'] = True
    elif symbol == A:
        keys['A'] = True
    elif symbol == S:
        keys['S'] = True
    elif symbol == D:
        keys['D'] = True


@wind.event
def on_key_release(symbol, modifiers):
    if symbol == W:
        keys['W'] = False
    elif symbol == A:
        keys['A'] = False
    elif symbol == S:
        keys['S'] = False
    elif symbol == D:
        keys['D'] = False
    



def update(dt, speed=5):
    if keys['W']:
        pl_moving(0, speed)
    if keys['S']:
        pl_moving(0, -speed)
    if keys['A']:
        pl_moving(-speed, 0)
    if keys['D']:
        pl_moving(speed, 0)


@wind.event
def on_draw():
    wind.clear()
    #кстати чтобы определить цвет я использую https://colorscheme.ru/color-names.html
    playr.draw()
    dom.draw()
    zombi.draw()
    text.draw()

pyglet.clock.schedule_interval(spawn,spawnSpeed,isZombSpawn)
pyglet.clock.schedule_interval(zombMoving,1/20)
#передвижения зомбей с обновлением каждые 1/4 секунды может уже не 1/4 
pyglet.clock.schedule_interval(update,1/60)
pyglet.clock.schedule_interval(zombAttack,1/2)
pyglet.app.run()