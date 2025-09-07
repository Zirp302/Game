import pyglet
from pyglet import shapes as sh
from pyglet.window.key import *
from pyglet.window import key
from Uprav import Uprav
import random
from Objects import Zombi,Pl, Stena
# доки пайглета https://pyglet.readthedocs.io/en/latest/programming_guide/shapes.html
#это чтобы писать названия клавиш не указывая функцию key
# wind is a window
xp=100
isSpawn=True
#Сори но это хп персонажа я не мог не реализовать хп если есть зомби
wind_width, wind_height = (720, 720)
wind = pyglet.window.Window(width=wind_width, height=wind_height, caption="gameOnPyglet")
width, height = (50, 100)
playr = Pl().playr()
HP = Pl().HP()
#могут ли зомби появляться
#Скорость появления зомбей попробуй изменить число на какое нибудь оч маленькое по типу 1/60 и тд
w = 30
h = 30
drawInfuncs=[]
#Почему хрb? Я сам не знаю
@wind.event
def on_mouse_press(x,y,button,modifiers):
    print(f"x = {x}, y = {y}")
defaultZomb=Zombi(playr=playr)
MiniBoss=Zombi(playr=playr,w=25,h=25,type="big",xp=1000,speed=0.2,spawnSpeed=3,damage=30)



@wind.event
def on_mouse_press(x,y,button,modifiers):
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
U = Uprav(playr, HP, width)
S = Stena()

def avanpost(xM, yM):
    stena_l = U.ogran_line(S.left_S[0], S.left_S[1], S.left_S[2], S.left_S[3], xM, yM)
    stena_r = U.ogran_line(S.right_S[0], S.right_S[1], S.right_S[2], S.right_S[3], xM, yM)
    stena_v = U.ogran_line(S.verh_S[0], S.verh_S[1], S.verh_S[2], S.verh_S[3], xM, yM)
    stena_n = U.ogran_line(S.niz_S[0], S.niz_S[1], S.niz_S[2], S.niz_S[3], xM, yM)

    return stena_v and stena_n and stena_l and stena_r

def update(dt, speed=5):
    if keys[key.W]:
        x_moving, y_moving = 0, speed
        U.pl_moving(x_moving, y_moving, avanpost(x_moving, y_moving))
    if keys[key.S]:
        x_moving, y_moving = 0, -speed
        U.pl_moving(x_moving, y_moving, avanpost(x_moving, y_moving))
    if keys[key.A]:
        x_moving, y_moving = -speed, 0
        U.pl_moving(x_moving, y_moving, avanpost(x_moving, y_moving))
    if keys[key.D]:
        x_moving, y_moving = speed, 0
        U.pl_moving(x_moving, y_moving, avanpost(x_moving, y_moving))




@wind.event
def on_draw():
    wind.clear()
    Stena().draw()
    Pl.draw()
    #кстати чтобы определить цвет я использую https://colorscheme.ru/color-names.html
    defaultZomb.batch.draw()
defaultZomb.spawn()
pyglet.clock.schedule_interval(defaultZomb.spawn,defaultZomb.spawSpeed)
pyglet.clock.schedule_interval(defaultZomb.moving,1/20)
#передвижения зомбей с обновлением каждые 1/4 секунды может уже не 1/4 
pyglet.clock.schedule_interval(update,1/60)
pyglet.clock.schedule_interval(defaultZomb.attack,1/2)
pyglet.app.run()