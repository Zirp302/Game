from pyglet import shapes as sh
from Uprav import Uprav


class Pl:
    # Создание самого игрока
    playr = None
    def __init__(self, x, y, width, height, color, batch):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.batch = batch
        Pl.playr = sh.Rectangle(x, y, width, height, color, batch=batch)
        

    # HP игрока
    def HP(self):
        playr = Pl.playr
        HP_playr = 5
        HP_One = self.width / HP_playr
        Polosa = HP_playr * HP_One # Полоска HP
        return sh.Rectangle(playr.x, playr.y + self.height, Polosa, 15, color=(255,0,0), batch=self.batch)

    def draw(self):
        Pl.playr.draw()

