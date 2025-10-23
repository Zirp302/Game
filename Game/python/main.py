from objeсts import Playr, Wall, Zombi, Damag
from management import Managment
import pyglet
from pyglet.window import key

screens = pyglet.display.get_display().get_screens()[0] # Определение максимальной высоты и ширины экрана
wind = pyglet.window.Window(               # Создание окна
    screens.width, screens.height, 
    resizable=True, caption="gameOnPyglet"
    ) 

wind.maximize()

pl = Playr()
playr = pl.avatar()
hp = pl.hp_playr()

@wind.event
def on_mouse_press(x,y,button,modifiers):
    print(f"x = {x}, y = {y}")


wall = Wall(playr, hp)
Managmentlenie = Managment(playr, hp, screens)
damag = Damag(playr, hp)
zombi = Zombi(playr, hp, screens)

keys = key.KeyStateHandler()
wind.push_handlers(keys)

def update(dt, speed=5, uron=1):
    zombi.moving()
    zombi.attack()   
    damag.damag_rectangle(200, 200, 20, 20, uron)

    walking_y = int(keys[key.W]) - int(keys[key.S]) # Ходьба по оси х
    walking_x = int(keys[key.D]) - int(keys[key.A]) # Ходьба по оси у
    if bool(walking_y):  
        y_moving = speed * walking_y
        Managmentlenie.playr_moving(
            0, y_moving, 
            wall.all_walls(0, y_moving)
            )
        
    if bool(walking_x):  
        x_moving = speed * walking_x
        Managmentlenie.playr_moving(
            x_moving, 0, 
            wall.all_walls(x_moving, 0)
            )


@wind.event
def on_draw():
    wind.clear()
    zombi.draw()
    Wall.draw()
    pl.draw()

pyglet.clock.schedule_interval(update, 1/60)
pyglet.clock.schedule_interval(zombi.spawn, 2)
pyglet.app.run()