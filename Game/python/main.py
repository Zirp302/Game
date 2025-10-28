from objects import Playr, Wall, Zombi, Damag
from management import Managment
import pyglet
from pyglet.window import key

screens = pyglet.display.get_display().get_screens()[0] # Определение максимальной высоты и ширины экрана
# Отключает синхронизацию (У меня моник с низкой герцовкой так что не уберай)
pyglet.options['vsync'] = False  
wind_width, wind_height = 720, 620
wind = pyglet.window.Window(wind_width, wind_height, resizable=True, caption="gameOnPyglet") # Создание окна 

fps_display = pyglet.window.FPSDisplay(wind)

fps_display.y = 600

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
    for objects_damag in wall.all_spikes_in_forest:
        damag.damag_rectangle(
            objects_damag[0], objects_damag[1], 
            objects_damag[2], objects_damag[3], 
            uron)

    walking_y = int(keys[key.W]) - int(keys[key.S]) # Ходьба по оси х
    walking_x = int(keys[key.D]) - int(keys[key.A]) # Ходьба по оси у

    if walking_y:  
        y_moving = speed * walking_y
        Managmentlenie.playr_moving(
            0, y_moving, 
            wall.all_walls(0, y_moving)
            )
        
    if walking_x:  
        x_moving = speed * walking_x
        Managmentlenie.playr_moving(
            x_moving, 0, 
            wall.all_walls(x_moving, 0)
            )
    global fps_display

@wind.event
def on_draw():
    wind.clear()
    Wall.draw()
    pl.draw()
    zombi.draw()
    fps_display.draw()
    

pyglet.clock.schedule_interval(update, 1/60)
pyglet.clock.schedule_interval(zombi.spawn, 2)
pyglet.app.run()