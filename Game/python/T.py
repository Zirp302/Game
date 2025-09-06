from Objekts import Pl, Stena
from Uprav import Uprav
import keyboard as k
import pyglet
import time
from pyglet import shapes as sh
from pyglet.window.key import *
from pyglet.window import key
# доки пайглета https://pyglet.readthedocs.io/en/latest/programming_guide/shapes.html
#это чтобы писать названия клавиш не указывая функцию key
# wind is a window object


wind_width, wind_height = (720, 720)
wind = pyglet.window.Window(width=wind_width, height=wind_height, caption="gameOnPyglet")
width, height = (50, 100)
playr = Pl().playr()
HP = Pl().HP()

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
    stena_l = U.ogran(S.left_S[0], S.left_S[1], S.left_S[2], S.left_S[3], xM, yM)
    stena_r = U.ogran(S.right_S[0], S.right_S[1], S.right_S[2], S.right_S[3], xM, yM)
    stena_v = U.ogran(S.verh_S[0], S.verh_S[1], S.verh_S[2], S.verh_S[3], xM, yM)
    stena_n = U.ogran(S.niz_S[0], S.niz_S[1], S.niz_S[2], S.niz_S[3], xM, yM)

    return stena_v and stena_n and stena_l and stena_r

def update(dt, speed=5):
    if keys[key.W]:
        x_moving = 0
        y_moving = speed
        U.pl_moving(x_moving, y_moving, avanpost(x_moving, y_moving))
    if keys[key.S]:
        x_moving = 0
        y_moving = -speed
        U.pl_moving(x_moving, y_moving, avanpost(x_moving, y_moving))
    if keys[key.A]:
        x_moving = -speed
        y_moving = 0
        U.pl_moving(x_moving, y_moving, avanpost(x_moving, y_moving))
    if keys[key.D]:
        x_moving = speed
        y_moving = 0
        U.pl_moving(x_moving, y_moving, avanpost(x_moving, y_moving))


@wind.event
def on_draw():
    wind.clear()
    Stena().draw()
    Pl.draw()

pyglet.clock.schedule_interval(update, 1/60)
'''pyglet.clock.schedule_interval(Damag, 1/60, HP.HP_One)'''
pyglet.app.run()