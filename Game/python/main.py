from objects import *
from management import *
import pyglet
from pyglet.window import key

screens = pyglet.display.get_display().get_screens()[0] # Определение максимальной высоты и ширины экрана
# Отключает синхронизацию (У меня моник с низкой герцовкой так что не уберай)
pyglet.options['vsync'] = False  
wind_width, wind_height = 720, 620
wind = pyglet.window.Window(wind_width, wind_height, resizable=True, caption="gameOnPyglet") # Создание окна 
wind.maximize()

fps_display = pyglet.window.FPSDisplay(wind)
fps_display.y = 600


pl = Player()
player = pl.avatar()
hp = pl.hp_player()

@wind.event
def on_mouse_press(x,y,button,modifiers):
    print(f"x = {x}, y = {y}")


wall = Wall(player, hp)
Managmentlenie = Managment(player, hp, screens)
zombi = Zombi(player, hp, screens)
damage = Damage(player, hp)
keys = key.KeyStateHandler()
wind.push_handlers(keys)

def update(dt, speed=5, uron=1):
    zombi.moving()
    zombi.attack()   
    for objects_damage in wall.all_spikes_in_forest:
        damage.damage_rectangle(
            objects_damage[0], objects_damage[1], 
            objects_damage[2], objects_damage[3], 
            uron)
        
    if walking_y := (keys[key.W] - keys[key.S]): # Проверка ходьбы по оси y
        y_moving = speed * walking_y
        Managmentlenie.player_moving(0, y_moving, wall.all_walls(0, y_moving))
        
    if walking_x := (keys[key.D] - keys[key.A]): # Проверка ходьбы по оси x
        x_moving = speed * walking_x
        Managmentlenie.player_moving(x_moving, 0, wall.all_walls(x_moving, 0))

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