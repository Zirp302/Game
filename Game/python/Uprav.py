import pyglet
import time
from pyglet import shapes as sh
from pyglet.window.key import *
'''from Objekts import Pl, Stena'''


class Uprav:
    #   Передвижеие игрока и его полоски жизни
    def __init__(self, x, y, playr, HP, width):
        self.x = x
        self.y = y
        self.playr = playr
        self.HP = HP
        self.width = width
        if 0 < x + playr.x < 721 - width:
            playr.x += x
            HP.x += x
        if 0 < y + playr.y < 721 - width:
            playr.y += y
            HP.y += y
    
    #   Проверка кнопок для передвижения
    #   Доделать блокировку cтенам
    '''def ogran(self, x1, y1, x2, y2, x=0, y=0, zonaw=Pl.width, zonah=Pl.height, speed=5):
        if x1 == x2:
            x1 -= 10
            x2 += 10
            y1, y2 = min(y1, y2), max(y1, y2)
        else:
            y1 -= 10
            y2 += 10
            x1, x2 = min(x1, x2), max(x1, x2)
        
        if x1 - zonaw < Pl.playr().x + x < x2 and y1 - zonah < Pl.playr().y + y < y2:
            return False
        return True
        S = Stena
        stena_l = Uprav.ogran(left_S[0], left_S[1], left_S[2], left_S[3], x, y)
        stena_r = Uprav.ogran(right_S[0], right_S[1], right_S[2], right_S[3], x, y)
        stena_v = Uprav.ogran(verh_S[0], verh_S[1], verh_S[2], verh_S[3], x, y)
        stena_n = Uprav.ogran(niz_S[0], niz_S[1], niz_S[2], niz_S[3], x, y)

        avanpost = stena_v and stena_n and stena_l and stena_r'''