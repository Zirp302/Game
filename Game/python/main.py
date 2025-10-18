from Objeсts import Pl, Wall, Damag, Zombi
from Uprav import Uprav
import pyglet
from pyglet.window import key

screens = pyglet.display.get_display().get_screens()[0] # Определение максимальной высоты и ширины экрана
wind = pyglet.window.Window(
    screens.width, screens.height, 
    resizable=True, caption="gameOnPyglet"
    ) # Создание окна

wind.maximize()

pl = Pl()
playr = pl.playr()
HP = pl.HP()

@wind.event
def on_mouse_press(x,y,button,modifiers):
    print(f"x = {x}, y = {y}")
    print(wind)


wall = Wall(playr, HP, Pl.width)
def avanpost(x_moving, y_moving): # Перенести аванпост в object
    for walls in Wall.all_line_walls:
        ogran = wall.ogran_line( 
            walls[0], walls[1], 
            walls[2], walls[3], 
            x_moving, y_moving
            )
        if ogran == False:
            return False
    return True


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
    """
    if hodba_y or hodba_x:  # Исправить баг прилепания к стенам через нейтрализацию
        y_moving = speed * hodba_y
        x_moving = speed * hodba_x
        upravlenie.pl_moving(
            x_moving, y_moving, 
            avanpost(x_moving, y_moving)
            )
    """
    if hodba_y:  
        y_moving = speed * hodba_y
        upravlenie.pl_moving(
            0, y_moving, 
            avanpost(0, y_moving)
            )
        
    if hodba_x:  
        x_moving = speed * hodba_x
        upravlenie.pl_moving(
            x_moving, 0, 
            avanpost(x_moving, 0)
            )


@wind.event
def on_draw():
    wind.clear()
    Z.draw()
    pl.draw()
    Wall.draw()

pyglet.clock.schedule_interval(update, 1/60)
pyglet.clock.schedule_interval(Z.spawn, 2)
pyglet.app.run()