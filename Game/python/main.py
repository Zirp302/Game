from Objeсts import Player, Stena, Damag, Zombi
from Uprav import Playr_uprav
import pyglet
from pyglet import shapes as sh
from pyglet.window.key import *
from pyglet.window import key

wind_width, wind_height = (720, 720) # Ширина и высота окна
wind = pyglet.window.Window(width=wind_width, height=wind_height, caption="gameOnPyglet") # Создание окна
playr = Player()

"""@wind.event
def on_mouse_press(x,y,button,modifiers):
    print(f"x = {x}, y = {y}")"""


keys = key.KeyStateHandler()
wind.push_handlers(keys)
walls = Stena(playr.width)

uprav_playr = Playr_uprav(playr)
default_zomb = Zombi(playr, uprav_playr)
damag = Damag(playr)

def update(dt, speed=5):
    #default_zomb.moving()
    default_zomb.attack()
    #Не используй буквы в качестве переменных во первых из за этого мы не сможем использовать клавишу а во вторых это плохо читается
    #Вот это все что связано с проверкой входения персонажа в стену нужно переместить в одну функцию а то это плохо читается, а также нагружает главный файл
    if True in {keys[W], keys[A], keys[S], keys[D]}:
        uprav_playr.pl_moving(keys)
    damag.damag_rectangle(walls.shipi)
        #Полностью перенесем управление в отдельный файл

default_zomb.test(250, 250, 45, 45)
@wind.event
def on_draw():
    wind.clear()
    default_zomb.draw()
    walls.draw()
    playr.draw()

pyglet.clock.schedule_interval(update, 1/60)
#pyglet.clock.schedule_interval(default_zomb.spawn, 2)
pyglet.app.run()