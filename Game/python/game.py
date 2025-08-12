import pyglet
from pyglet import shapes as sh
from pyglet.window.key import *
speed=5
# доки пайглета https://pyglet.readthedocs.io/en/latest/programming_guide/shapes.html
#это чтобы писать названия клавиш не указывая функцию key
# wind is a window object
wind = pyglet.window.Window(width=720,height=720,caption="gameOnPyglet")
playr=pyglet.graphics.Batch()
#playr is a player with all his parts
body=sh.Rectangle(200,200,10,30,batch=playr,color=[54,136,181])
head=sh.Circle(205,231,10,batch=playr,color=[54,136,181])
leg1=sh.Line(201,202,193,189,batch=playr,color=[54,136,181])
leg2=sh.Line(210,202,218,189,batch=playr,color=[54,136,181])
arm1=sh.Line(200,224,192,215,batch=playr,color=[54,136,181])
arm2=sh.Line(209,224,217,215,batch=playr,color=[54,136,181])
@wind.event
# this need to create a default-type function
def on_draw():
    wind.clear()
    #кстати чтобы определить цвет я использую https://colorscheme.ru/color-names.html
    playr.draw()
@wind.event
def on_mouse_press(x,y,button,modifiers):
    print(f"x = {x}, y = {y}")
def pl_moving(dX,dY):
    for i in [body,head,leg1,leg2,arm1,arm2]:
        i.x+=dX
        i.y+=dY
    #не работает
keys={'W': False, 'A': False, 'S': False, 'D': False}
@wind.event
def on_key_press(symbol, modifiers):
    if symbol == W:
        keys['W'] = True
    elif symbol == A:
        keys['A'] = True
    elif symbol == S:
        keys['S'] = True
    elif symbol == D:
        keys['D'] = True

@wind.event
def on_key_release(symbol, modifiers):
    if symbol == W:
        keys['W'] = False
    elif symbol == A:
        keys['A'] = False
    elif symbol == S:
        keys['S'] = False
    elif symbol == D:
        keys['D'] = False

def update(dt):
    if keys['W']:
        pl_moving(0, speed)
    if keys['A']:
        pl_moving(-speed, 0)
    if keys['S']:
        pl_moving(0, -speed)
    if keys['D']:
        pl_moving(speed, 0)

pyglet.clock.schedule_interval(update,1/60)
pyglet.app.run()