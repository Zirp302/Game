from objects import *
import pyglet
from pyglet.window import key
from menu import *


screens = pyglet.display.get_display().get_screens()[0] # Определение максимальной высоты и ширины экрана
pyglet.options['vsync'] = False  # Отключает синхронизацию (У меня моник с низкой герцовкой так что не уберай)
wind_width, wind_height = 720, 620
wind = pyglet.window.Window(wind_width, wind_height, resizable=True, caption="gameOnPyglet") # Создание окна 
wind.maximize()

draw_run = True
play_run = True
menu = Menu(screens.width, screens.height)

fps_display = pyglet.window.FPSDisplay(wind)
fps_display.y = 600


player = Player(screens)
player.body()
player.hp()
player_body = player.body_entitie
hp = player.hp_entitie

@wind.event
def on_mouse_press(x, y, button, modifiers):
    print(f"x = {x}, y = {y}")

    global play_run
    global draw_run
    menu.key(x, y)

    if menu.key_play and play_run:
        pyglet.clock.schedule_interval(update, 1/60)
        pyglet.clock.schedule_interval(zombi.spawn, 2)
        draw_run = False
        play_run = False

    elif menu.key_menu:
        pyglet.clock.unschedule(update)
        pyglet.clock.unschedule(zombi.spawn)
        play_run = True
        draw_run = True
    
    elif menu.key_settings:
        print(9)

    elif menu.key_exat:
        wind.close()

wall = Wall(player_body)
zombi = Zombi(player, screens)
keys = key.KeyStateHandler()
wind.push_handlers(keys)

def update(dt, speed=5, uron=1):
    zombi.moving()
    zombi.attack()  
    player.damage(
        200, 200, 
        20, 20, 
        uron)
    
    if walking_y := (keys[key.W] - keys[key.S]): # Проверка ходьбы по оси y
        y_moving = speed * walking_y
        player.moving(0, y_moving, wall.all_walls(0, y_moving))
        
    if walking_x := (keys[key.D] - keys[key.A]): # Проверка ходьбы по оси x
        x_moving = speed * walking_x
        player.moving(x_moving, 0, wall.all_walls(x_moving, 0))


@wind.event
def on_draw():
    wind.clear()
    if draw_run:
        menu.draw()
        return
    wall.draw()
    player.draw()
    zombi.draw()
    fps_display.draw()


pyglet.app.run()