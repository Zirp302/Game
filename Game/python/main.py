from Objeсts import Pl, Stena, Damag, Zombi
from Uprav import Playr_uprav
import pyglet
from pyglet import shapes as sh
from pyglet.window.key import *
from pyglet.window import key

wind_width, wind_height = (720, 720) # Ширина и высота окна
wind = pyglet.window.Window(width=wind_width, height=wind_height, caption="gameOnPyglet") # Создание окна
pl = Pl()
playr = pl.playr()
HP = pl.HP()

"""@wind.event
def on_mouse_press(x,y,button,modifiers):
    print(f"x = {x}, y = {y}")"""


keys = key.KeyStateHandler()
wind.push_handlers(keys)
walls = Stena(playr, HP, Pl.width)

def avanpost(x_moving, y_moving):
    #во первых передавая в качестве первых четырех аргументов распакованный список это легче читается чем твои гроомоздкие куски кода а во вторых это быстрее И лучше
    stena_l = walls.ogran_line( 
                            *walls.left_S,
                            x_moving, y_moving)
    stena_r = walls.ogran_line( 
                            *walls.right_S, 
                            x_moving, y_moving)
    stena_v = walls.ogran_line(
                            *walls.verh_S,
                            x_moving, y_moving)
    stena_n = walls.ogran_line(
                            *walls.niz_S,
                            x_moving, y_moving)

    return stena_v and stena_n and stena_l and stena_r


uprav_playr = Playr_uprav(playr, HP, Pl.width)
damag = Damag(playr, HP)
default_zomb = Zombi(playr, HP, uprav_playr)

def update(dt, speed=5):
    default_zomb.moving()
    default_zomb.attack()
    #Не используй буквы в качестве переменных во первых из за этого мы не сможем использовать клавишу а во вторых это плохо читается
    #Вот это все что связано с проверкой входения персонажа в стену нужно переместить в одну функциюа то это плохо читается, а также нагружает главный файл
    damag.damag_rectangle(200, 200, 20, 20, 1)
    if True in {keys[W], keys[A], keys[S], keys[D]}:
        uprav_playr(keys)
        #Полностью перенесем управление в отдельный файл


@wind.event
def on_draw():
    wind.clear()
    default_zomb.draw()
    walls.draw()
    pl.draw()

pyglet.clock.schedule_interval(update, 1/60)
pyglet.clock.schedule_interval(default_zomb.spawn, 2)
pyglet.app.run()