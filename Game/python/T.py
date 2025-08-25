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
pl = Pl()
playr = pl.playr()
HP = pl.HP()

@wind.event
def on_mouse_press(x,y,button,modifiers):
    print(f"x = {x}, y = {y}")

'''
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
'''

"""dom = pyglet.graphics.Batch()
wall_left = sh.Line(left_S[0], left_S[1], left_S[2], left_S[3], thickness=Shir_S, batch=dom)
wall_right = sh.Line(right_S[0], right_S[1], right_S[2], right_S[3], thickness=Shir_S, batch=dom)
wall_verh = sh.Line(verh_S[0], verh_S[1], verh_S[2], verh_S[3], thickness=Shir_S, batch=dom)
wall_niz = sh.Line(niz_S[0], niz_S[1], niz_S[2], niz_S[3], thickness=Shir_S, batch=dom) 
shipi = sh.Rectangle(200, 200, 20, 20, color=(111,111,111), batch=dom)"""


"""def ogran(x1, y1, x2, y2, x=0, y=0, zonaw=width, zonah=height, speed=5): # Доделать блокировку cтенам
    if x1 == x2:
        x1 -= 10
        x2 += 10
    else:
        y1 -= 10
        y2 += 10
    
    
    if x1 - zonaw < playr.x + x < x2 and y1 - zonah < playr.y + y < y2:
        return False
    return True"""

"""
def pl_moving(x,y):
    stena_l = ogran(left_S[0], left_S[1], left_S[2], left_S[3], x, y)
    stena_r = ogran(right_S[0], right_S[1], right_S[2], right_S[3], x, y)
    stena_v = ogran(verh_S[0], verh_S[1], verh_S[2], verh_S[3], x, y)
    stena_n = ogran(niz_S[0], niz_S[1], niz_S[2], niz_S[3], x, y)
    global dm
    dm = not ogran(200, 200, 220, 220, x, y)
    

    avanpost = stena_v and stena_n and stena_l and stena_r
    if 0 < x + playr.x < 721 - w and avanpost:
        playr.x += x
        HP.x += x
    if 0 < y + playr.y < 721 - w and avanpost :
        playr.y += y
        HP.y += y"""
"""
dm = False



time_kd = 0
def Damag(dt, HP_One=HP_One):
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
            dm = False"""


keys = key.KeyStateHandler()
wind.push_handlers(keys)

def update(dt, speed=5):
    if keys[key.W]:
        Uprav(0, speed, playr, HP, width)
    if keys[key.S]:
        Uprav(0, -speed, playr, HP, width)
    if keys[key.A]:
        Uprav(-speed, 0, playr, HP, width)
    if keys[key.D]:
        Uprav(speed, 0, playr, HP, width)


@wind.event
def on_draw():
    wind.clear()
    Stena().draw()
    Pl.draw()

pyglet.clock.schedule_interval(update, 1/60)
"""pyglet.clock.schedule_interval(Damag, 1/60, HP_One)"""
pyglet.app.run()