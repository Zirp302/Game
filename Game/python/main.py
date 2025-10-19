from Objeсts import Pl, Wall, Zombi, Damag
from Management import Uprav
import pyglet
from pyglet.window import key

screens = pyglet.display.get_display().get_screens()[0] # Определение максимальной высоты и ширины экрана
wind = pyglet.window.Window(               # Создание окна
    screens.width, screens.height, 
    resizable=True, caption="gameOnPyglet"
    ) 

wind.maximize()

pl = Pl()
playr = pl.playr()
HP = pl.HP()

@wind.event
def on_mouse_press(x,y,button,modifiers):
    print(f"x = {x}, y = {y}")




wall = Wall(playr, HP)
upravlenie = Uprav(playr, HP, screens)
damag = Damag(playr, HP)
Z = Zombi(playr, HP, screens)

keys = key.KeyStateHandler()
wind.push_handlers(keys)

def update(dt, speed=5, uron=1):
    Z.moving()
    Z.attack()   
    damag.damag_rectangle(200, 200, 20, 20, uron)

    hodba_y = int(keys[key.W]) - int(keys[key.S])
    hodba_x = int(keys[key.D]) - int(keys[key.A])
    if hodba_y:  
        y_moving = speed * hodba_y
        upravlenie.pl_moving(
            0, y_moving, 
            wall.avanpost(0, y_moving)
            )
        
    if hodba_x:  
        x_moving = speed * hodba_x
        upravlenie.pl_moving(
            x_moving, 0, 
            wall.avanpost(x_moving, 0)
            )


@wind.event
def on_draw():
    wind.clear()
    Z.draw()
    Wall.draw()
    pl.draw()

pyglet.clock.schedule_interval(update, 1/60)
pyglet.clock.schedule_interval(Z.spawn, 2)
pyglet.app.run()