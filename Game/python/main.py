from Objeсts import Pl, Stena, Damag, Zombi
from Uprav import Uprav
import pyglet
from pyglet.window import key


wind_width, wind_height = (720, 720) # Ширина и высота окна
wind = pyglet.window.Window(width=wind_width, height=wind_height, caption="gameOnPyglet") # Создание окна
pl = Pl()
playr = pl.playr()
HP = pl.HP()

@wind.event
def on_mouse_press(x,y,button,modifiers):
    print(f"x = {x}, y = {y}")


S = Stena(playr, HP, Pl.width)
def avanpost(x_moving, y_moving): # Перенести аванпост в object
    stena_l = S.ogran_line( 
        S.left_S[0], S.left_S[1], 
        S.left_S[2], S.left_S[3], 
        x_moving, y_moving)
    
    stena_r = S.ogran_line( 
        S.right_S[0],S.right_S[1], 
        S.right_S[2],S.right_S[3], 
        x_moving, y_moving)
    
    stena_v = S.ogran_line(
        S.verh_S[0], S.verh_S[1], 
        S.verh_S[2], S.verh_S[3], 
        x_moving, y_moving)
    
    stena_n = S.ogran_line(
        S.niz_S[0], S.niz_S[1], 
        S.niz_S[2], S.niz_S[3], 
        x_moving, y_moving)

    return stena_v and stena_n and stena_l and stena_r


upravlenie = Uprav(playr, HP, Pl.width)
damag = Damag(playr, HP)
Z = Zombi(playr, HP, upravlenie)

keys = key.KeyStateHandler()
wind.push_handlers(keys)

def update(dt, speed=5, uron=1):
    Z.moving()
    Z.attack()   
    damag.damag_rectangle(200, 200, 20, 20, uron)

    hodba_y = int(keys[key.W]) - int(keys[key.S])
    hodba_x = int(keys[key.D]) - int(keys[key.A])
    """
    if hodba_y != 0 or hodba_x != 0:  # Исправить баг прилепания к стенам через нейтрализацию
        y_moving = speed * hodba_y
        x_moving = speed * hodba_x
        upravlenie.pl_moving(
            x_moving, y_moving, 
            avanpost(x_moving, y_moving)
            )
    """
    if hodba_y != 0:  
        y_moving = speed * hodba_y
        upravlenie.pl_moving(
            0, y_moving, 
            avanpost(0, y_moving)
            )
        
    if hodba_x != 0:  
        x_moving = speed * hodba_x
        upravlenie.pl_moving(
            x_moving, 0, 
            avanpost(x_moving, 0)
            )


@wind.event
def on_draw():
    wind.clear()
    Z.draw()
    S.draw()
    pl.draw()

pyglet.clock.schedule_interval(update, 1/60)
pyglet.clock.schedule_interval(Z.spawn, 2)
pyglet.app.run()