from Game.python.Objects import Pl
import pyglet
import time
from pyglet import shapes as sh
from pyglet.window.key import *

# доки пайглета https://pyglet.readthedocs.io/en/latest/programming_guide/shapes.html
#это чтобы писать названия клавиш не указывая функцию key
# wind is a window object


wind_width, wind_height = (720, 720)
wind = pyglet.window.Window(width=wind_width, height=wind_height, caption="gameOnPyglet")
w, h = (50, 100)
pl = pyglet.graphics.Batch()
playr = Pl(x=361, y=361, width=50, height=100, color=(54, 136, 181), batch=pl)
HP_playr = 5
HP_One = w / HP_playr
HP = sh.Rectangle(playr.x, playr.y + h, HP_playr * HP_One, 15, color=(255,0,0), batch=pl)







@wind.event
def on_mouse_press(x,y,button,modifiers):
    print(f"x = {x}, y = {y}")


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


dom = pyglet.graphics.Batch()
wall_left = sh.Line(left_S[0], left_S[1], left_S[2], left_S[3], thickness=Shir_S, batch=dom)
wall_right = sh.Line(right_S[0], right_S[1], right_S[2], right_S[3], thickness=Shir_S, batch=dom)
wall_verh = sh.Line(verh_S[0], verh_S[1], verh_S[2], verh_S[3], thickness=Shir_S, batch=dom)
wall_niz = sh.Line(niz_S[0], niz_S[1], niz_S[2], niz_S[3], thickness=Shir_S, batch=dom) 
shipi = sh.Rectangle(200, 200, 20, 20, color=(111,111,111), batch=pl)

def ogran(x1, y1, x2, y2, x=0, y=0, zonaw=w, zonah=h, speed=5): # Доделать блокировку cтенам
    if x1 == x2:
        x1 -= 10
        x2 += 10
    else:
        y1 -= 10
        y2 += 10
    
    
    if x1 - zonaw < playr.x + x < x2 and y1 - zonah < playr.y + y < y2:
        return False
    return True
dm = False

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
        HP.y += y

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
            dm = False


def update(dt, speed=5):
    if keys['W']:
        playr.pl_moving(0, speed)
    if keys['S']:
        playr.pl_moving(0, -speed)
    if keys['A']:
        playr.pl_moving(-speed, 0)
    if keys['D']:
        playr.pl_moving(speed, 0)

#кстати чтобы определить цвет я использую https://colorscheme.ru/color-names.html


@wind.event
def on_draw():
    wind.clear()
    playr.draw()
    dom.draw()

pyglet.clock.schedule_interval(update, 1/60)
pyglet.clock.schedule_interval(Damag, 1/60, HP_One)
pyglet.app.run()