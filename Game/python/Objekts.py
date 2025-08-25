from pyglet import shapes as sh
from Uprav import Uprav
import pyglet

class Pl:
    # Создание самого игрока
    x=361
    y=361
    width=50
    height=100
    color=(54, 136, 181)
    pl = pyglet.graphics.Batch()
    def __init__(self):
        self.playr = sh.Rectangle(Pl.x, Pl.y, Pl.width, Pl.height, Pl.color, batch=Pl.pl)

    # HP игрока
    def HP(self):
        HP_playr = 5
        HP_One = Pl.width / HP_playr
        Polosa = HP_playr * HP_One # Полоска HP
        return sh.Rectangle(Pl.x, Pl.y + Pl.height, Polosa, 15, color=(255,0,0), batch=Pl.pl)

    def draw():
        Pl.pl.draw()

