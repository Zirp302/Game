import pyglet
from pyglet import shapes as sh
from pyglet.window.key import *
from Uprav import playrUprav
import random
from pyglet.window import key
from Objects import Zombi, Pl, Stena
import os
isSpawn=True
wind_width, wind_height = (720, 720)
wind = pyglet.window.Window(width=wind_width, height=wind_height, caption="gameOnPyglet")
width, height = (50, 100)
playr = Pl()
xp = 100
Uprav = playrUprav(playr, playr.HP)
defaultZomb = Zombi(playr, Uprav)
MiniBoss = Zombi(playr=playr,plrUprv=Uprav, width=25, height=25, type="big", xp=1000, speed=0.2, spawnSpeed=3, damage=30)


@wind.event
def on_mouse_press(x,y,button,modifiers):
    defaultZomb.attack()
    print(f"x = {x}, y = {y}")

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



defaultZomb.test(360, 360, 30, 30)
@wind.event
def on_draw():
    wind.clear()
    Stena().draw()
    playr.draw()
    defaultZomb.batch.draw()
pyglet.clock.schedule_interval(defaultZomb.spawn,defaultZomb.spawSpeed)
pyglet.clock.schedule_interval(defaultZomb.moving,1/20)
#передвижения зомбей с обновлением каждые 1/4 секунды может уже не 1/4 
pyglet.clock.schedule_interval(update, 1/60)
pyglet.clock.schedule_interval(defaultZomb.attack, 1)
pyglet.app.run()