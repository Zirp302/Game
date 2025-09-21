from Objekts import Pl, Stena, Damag
from Uprav import Uprav
import keyboard as k
import pyglet
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


keys = key.KeyStateHandler()
wind.push_handlers(keys)
S = Stena(playr, HP, width)

def avanpost(x_moving, y_moving):
    stena_l = S.ogran_line(S.left_S[0], S.left_S[1], 
                            S.left_S[2], S.left_S[3], 
                            x_moving, y_moving)
    
    stena_r = S.ogran_line(S.right_S[0],S.right_S[1], 
                            S.right_S[2],S.right_S[3], 
                            x_moving, y_moving)
    
    stena_v = S.ogran_line(S.verh_S[0], S.verh_S[1], 
                            S.verh_S[2], S.verh_S[3], 
                            x_moving, y_moving)
    
    stena_n = S.ogran_line(S.niz_S[0], S.niz_S[1], 
                            S.niz_S[2], S.niz_S[3], 
                            x_moving, y_moving)

    return stena_v and stena_n and stena_l and stena_r


upravlenie = Uprav(playr, HP, width)
damag = Damag(playr, HP)

def update(dt, speed=5):
    damag.damag_rectangle(200, 200, 20, 20, 1)
    if keys[key.W]:
        x_moving, y_moving = 0, speed
        upravlenie.pl_moving(x_moving, y_moving, avanpost(x_moving, y_moving))
    if keys[key.S]:
        x_moving, y_moving = 0, -speed
        upravlenie.pl_moving(x_moving, y_moving, avanpost(x_moving, y_moving))
    if keys[key.A]:
        x_moving, y_moving = -speed, 0
        upravlenie.pl_moving(x_moving, y_moving, avanpost(x_moving, y_moving))
    if keys[key.D]:
        x_moving, y_moving = speed, 0
        upravlenie.pl_moving(x_moving, y_moving, avanpost(x_moving, y_moving))


@wind.event
def on_draw():
    wind.clear()
    S.draw()
    Pl.draw()

pyglet.clock.schedule_interval(update, 1/60)
'''pyglet.clock.schedule_interval(Damag, 1/60, HP.HP_One)'''
pyglet.app.run()