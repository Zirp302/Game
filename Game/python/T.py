import pyglet
from pyglet import shapes as sh
from pyglet.window.key import *

# доки пайглета https://pyglet.readthedocs.io/en/latest/programming_guide/shapes.html
#это чтобы писать названия клавиш не указывая функцию key
# wind is a window object

wind = pyglet.window.Window(width=720, height=720, caption="gameOnPyglet")
w = 50
h = 100
playr = sh.Rectangle(331, 331, w, h, color=(54, 136, 181))


@wind.event
def on_mouse_press(x,y,button,modifiers):
    print(f"x = {x}, y = {y}")
print(9)


l_l_v = (240, 480)
l_l_n = (240, 240)
r_r_v = (480, 480)
r_r_n = (480, 240)

dom = pyglet.graphics.Batch()
wall_verh_left = sh.Line(l_l_v[0] + 10, l_l_n[1], l_l_n[0] + 10, l_l_v[1], thickness=20, batch=dom)
wall_verh_right = sh.Line(r_r_v[0] - 10, r_r_v[1], r_r_n[0] - 10, r_r_n[1], thickness=20, batch=dom)

wall_left_verh = sh.Line(r_r_v[0], r_r_v[1], l_l_v[0], l_l_v[1], thickness=20, batch=dom)
#wall_left_niz = sh.Line(r_r_n[0], r_r_n[1], l_l_n[0], l_l_n[1], thickness=20, batch=dom) Раскаментируй для появления нижней стены, a также раскаментируй код на 74 а также на 76 

""" Ворота. Не доделано
wall_niz_left = sh.Line(100, 100, 100, 200, thickness=20, batch=dom)
wall_niz_right = sh.Line(100, 100, 100, 200, thickness=20, batch=dom)

wall_right_verh = sh.Line(100, 100, 100, 200, thickness=20, batch=dom)
wall_right_niz = sh.Line(100, 100, 100, 200, thickness=20, batch=dom)"""


def ogran(x1, y1, x2, y2, playr_x, playr_y, zonaw=w, zonah=h, speed=5): # Доделать блокировку cтенам
    x1 = min(x1, x2)
    x2 = max(x1, x2)

    y1 = min(y1, y2)
    y2 = max(y1, y2)


    if x1 == x2:
        visota = y1 < playr.y + zonah < y2 + zonah
        if playr_xy > 0:
            shirina = x1 + speed > playr.x + zonaw > x2 - 10
        else: 
            shirina =  x2 + 15 < playr.x + speed < x1 + 20     
        return shirina and visota

    else:
        shirina = x1 + speed < playr.x + zonaw < x2 + zonaw
        if playr_xy > 0:
            visota = y1 + speed > playr.y + zonah> y2 - 10
        else: 
            visota = y1 + 15 < playr.y + speed < y2 + 20

        print(shirina, visota, playr.x, playr.y)
        return shirina and visota


def pl_moving(x,y):
    stena_l = not ogran(l_l_v[0] + 10, l_l_n[1], l_l_n[0] + 10, l_l_v[1] + 10, x, y)
    stena_r = not ogran(r_r_v[0] - 10, r_r_n[1], r_r_v[0] - 10, r_r_v[1] + 10, x, y)

    if 0 < x + playr.x < 721 - w and stena_l and stena_r:
        playr.x += x

    stena_v = not ogran(l_l_v[0], r_r_v[1], r_r_v[0], l_l_v[1], x, y)
    #stena_n = not ogran(l_l_v[0], r_r_n[1], r_r_v[0], l_l_n[1], y) прочитай послание на 31 строке

    if 0 < y + playr.y < 721 - w and stena_v and '''stena_n прочитай послание на 31 строке''':
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

pyglet.clock.schedule_interval(update,1/60)
pyglet.app.run()