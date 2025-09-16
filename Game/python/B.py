import pyglet
from pyglet import shapes as sh
from pyglet.window.key import *
from Uprav import playrUprav
import random
from pyglet.window import key
from Objects import Zombi, Pl, Stena, Ognestrel
import os
# доки пайглета https://pyglet.readthedocs.io/en/latest/programming_guide/shapes.html
#это чтобы писать названия клавиш не указывая функцию key
# wind is a window
isSpawn=True
#Сори но это хп персонажа я не мог не реализовать хп если есть зомби
wind_width, wind_height = (720, 720)
wind = pyglet.window.Window(width=wind_width, height=wind_height, caption="gameOnPyglet")
width, height = (50, 100)
playr = Pl()
xp=100
pist = Ognestrel(playr)
Uprav = playrUprav(playr, playr.HP, pist)
#могут ли зомби появляться
#Скорость появления зомбей попробуй изменить число на какое нибудь оч маленькое по типу 1/60 и тд
w = 30
h = 30
drawInfuncs=[]
#Почему хрb? Я сам не знаю
@wind.event
def on_mouse_press(x,y,button,modifiers):
    print(f"x = {x}, y = {y}")
defaultZomb = Zombi(playr, Uprav)
MiniBoss = Zombi(playr=playr,plrUprv=Uprav, width=25, height=25, type="big", xp=1000, speed=0.2, spawnSpeed=3, damage=30)



@wind.event
def on_mouse_press(x,y,button,modifiers):
    defaultZomb.attack()
    print(f"x = {x}, y = {y}")

'''
dm = False
time_kd = 1

def Damag(dt, HP_One=HP.HP_One):
    global dm
    global time_kd
    t = time.time()
    kd = t - time_kd

    if dm and kd > 1:
        print(time_kd, t, kd)
        time_kd = t
        cd = 0
        HP.width -= HP_One
        if HP.width == 0:
            playr.x, playr.y = (360, 360)
            HP.x, HP.y = (360, 360 + 100)
            HP.width = playr.width
            dm = False'''


keys = key.KeyStateHandler()
wind.push_handlers(keys)
walls = Stena()

def avanpost(xM, yM):
    stena_l = Uprav.ogran_line(walls.left_S[0], walls.left_S[1], walls.left_S[2], walls.left_S[3], xM, yM)
    stena_r = Uprav.ogran_line(walls.right_S[0], walls.right_S[1], walls.right_S[2], walls.right_S[3], xM, yM)
    stena_v = Uprav.ogran_line(walls.verh_S[0], walls.verh_S[1], walls.verh_S[2], walls.verh_S[3], xM, yM)
    stena_n = Uprav.ogran_line(walls.niz_S[0], walls.niz_S[1], walls.niz_S[2], walls.niz_S[3], xM, yM)

    return stena_v and stena_n and stena_l and stena_r


def update(dt, speed=5):
    if keys[W]:
        x_moving, y_moving = 0, speed
        Uprav.pl_moving(x_moving, y_moving, avanpost(x_moving, y_moving))
    if keys[S]:
        x_moving, y_moving = 0, -speed
        Uprav.pl_moving(x_moving, y_moving, avanpost(x_moving, y_moving))
    if keys[A]:
        x_moving, y_moving = -speed, 0
        Uprav.pl_moving(x_moving, y_moving, avanpost(x_moving, y_moving))
    if keys[D]:
        x_moving, y_moving = speed, 0
        Uprav.pl_moving(x_moving, y_moving, avanpost(x_moving, y_moving))
    if keys[Q]:
        pist.shot()
    if keys[E]:
        pist.recharge()
    #pist.Rotat(keys)



defaultZomb.test(360, 360, 30, 30)
@wind.event
def on_draw():
    wind.clear()
    Stena().draw()
    playr.draw()
    #кстати чтобы определить цвет я использую https://colorscheme.ru/color-names.html
    defaultZomb.batch.draw()
    pist.bat.draw()
    pist.pist.draw()
    pist.mugsInLab.draw()
    pist.AllmugsLab.draw()
"""i=1
while True:
    os.mkdir("hihi" + str(i))
    i += 1"""
#defaultZomb.spawn()
pyglet.clock.schedule_interval(defaultZomb.spawn,defaultZomb.spawSpeed)
pyglet.clock.schedule_interval(defaultZomb.moving,1/20)
pyglet.clock.schedule_interval(pist.pulaMoving, 1/300)
#передвижения зомбей с обновлением каждые 1/4 секунды может уже не 1/4 
pyglet.clock.schedule_interval(update, 1/60)
pyglet.clock.schedule_interval(defaultZomb.attack, 1)
pyglet.clock.schedule_interval(pist.damage,1/20)
pyglet.app.run()