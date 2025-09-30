from Objeсts import Pl, Stena, Damag, Zombi
from Uprav import Playr_uprav
import pyglet
from pyglet import shapes as sh
from pyglet.window.key import *
from pyglet.window import key

wind_width, wind_height = (720, 720) # Ширина и высота окна
wind = pyglet.window.Window(width=wind_width, height=wind_height, caption="gameOnPyglet") # Создание окна
playr = Pl()

"""@wind.event
def on_mouse_press(x,y,button,modifiers):
    print(f"x = {x}, y = {y}")"""


keys = key.KeyStateHandler()
wind.push_handlers(keys)
walls = Stena(playr, playr.HP, Pl.width)

uprav_playr = Playr_uprav(playr, playr.HP, Pl.width)
damag = Damag(playr, playr.HP)
default_zomb = Zombi(playr, playr.HP, uprav_playr)

def update(dt, speed=5):
    default_zomb.moving()
    default_zomb.attack()
    #Не используй буквы в качестве переменных во первых из за этого мы не сможем использовать клавишу а во вторых это плохо читается
    #Вот это все что связано с проверкой входения персонажа в стену нужно переместить в одну функциюа то это плохо читается, а также нагружает главный файл
    damag.damag_rectangle(200, 200, 20, 20, 1)
    if True in {keys[W], keys[A], keys[S], keys[D]}:
        uprav_playr.pl_moving(keys)
        #Полностью перенесем управление в отдельный файл


@wind.event
def on_draw():
    wind.clear()
    default_zomb.draw()
    walls.draw()
    playr.draw()

pyglet.clock.schedule_interval(update, 1/60)
#pyglet.clock.schedule_interval(default_zomb.spawn, 2)
pyglet.app.run()