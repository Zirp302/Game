from pyglet import shapes
import pyglet
from pyglet.window.key import *
col=pyglet.text.Label("0, 0, 0")
b=pyglet.graphics.Batch()
krug=shapes.Circle(0,0,10,color=[0,0,0],batch=b)
window=pyglet.window.Window(width=720, height=720)
'''@window.event
def on_key_press(symbol,modifiers):
    if LEFT == symbol and modifiers != MOD_CTRL:
        krug.x -= 1
    elif symbol == RIGHT and modifiers != MOD_CTRL:
        krug.x +=1
    elif symbol == UP and modifiers != MOD_CTRL:
        krug.y += 1
    elif symbol == DOWN and modifiers != MOD_CTRL:
        krug.y -=1
    elif symbol == UP and  modifiers == MOD_CTRL:
        krug.radius += 1
    elif symbol == DOWN and modifiers == MOD_CTRL:
        krug.radius -=1
    elif symbol == R and modifiers == MOD_CAPSLOCK:
        krug.color[0]+=1
        col.text=str(krug.color)
    elif symbol == G and modifiers == MOD_CAPSLOCK:
        krug.color[1]+=1
        col.text=str(krug.color)
    elif symbol == B and modifiers == MOD_CAPSLOCK:
        krug.color[2]+=1
        col.text=str(krug.color)
@window.event
def on_mouse_press(x,y,symbol,modifiers):
    col.x=x
    col.y=y'''
@window.event
def on_draw():
    window.clear()
    b.draw()
pyglet.app.run()