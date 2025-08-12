import pyglet
from pyglet import shapes as sh
from pyglet.window.key import *

# доки пайглета https://pyglet.readthedocs.io/en/latest/programming_guide/shapes.html
#это чтобы писать названия клавиш не указывая функцию key
# wind is a window object

wind = pyglet.window.Window(width=720,height=720,caption="gameOnPyglet")
w = 50
h = 100
playr = sh.Rectangle(331, 331, w, h, color=(54,136,181))


@wind.event
def on_mouse_press(x,y,button,modifiers):
    print(f"x = {x}, y = {y}")


dom = pyglet.graphics.Batch()

l_l_v = (240, 480)
l_l_n = (240, 240)
r_r_v = (480, 480)
r_r_n = (480, 240)

# Мысленно подели поле на 9 одинаковых квадратов

wall_verh_left = sh.Line(l_l_v[0] + 10, l_l_v[1], l_l_n[0] + 10, l_l_n[1], thickness=20, batch=dom)
wall_verh_right = sh.Line(r_r_v[0] - 10, r_r_v[1], r_r_n[0] - 10, r_r_n[1], thickness=20, batch=dom)

wall_left_verh = sh.Line(r_r_v[0], r_r_v[1], l_l_v[0], l_l_v[1], thickness=20, batch=dom)
wall_left_niz = sh.Line(r_r_n[0], r_r_n[1], l_l_n[0], l_l_n[1], thickness=20, batch=dom)

wall_niz_left = sh.Line(100, 100, 100, 200, thickness=20, batch=dom)
wall_niz_right = sh.Line(100, 100, 100, 200, thickness=20, batch=dom)

wall_right_verh = sh.Line(100, 100, 100, 200, thickness=20, batch=dom)
wall_right_niz = sh.Line(100, 100, 100, 200, thickness=20, batch=dom)


zonaw = w + 10
zonah = h / 2
#                 проверяет является ли х игрока х стен и если да то прорверяет являетсяли у игрока выше нижней точки стены и является ли y игрока ниже высшой точки стены
#                 и если все 3 условия выполнены то он не позваляет х увеличеваться
# Работает только на левой стене НЕ ТРОГАЙ я сам допелю
left_stena = not(5 + r_r_v[0] - 5 < zonaw + playr.x < 5 + r_r_v[0] and r_r_n[1] < zonah + playr.y < r_r_v[1] and not playr.x + x < playr.x)

def pl_moving(x,y):
    if 0 < x + playr.x < 721 - w and :
        print(zonah + playr.x == r_r_v[0], r_r_n[1] < zonah + playr.y < r_r_v[1])
        playr.x+=x
    if 0 < y + playr.y < 721 - w:
        playr.y+=y

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
