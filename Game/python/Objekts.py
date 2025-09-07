from pyglet import shapes as sh
import pyglet
"""
Файл для создания обектов и их вывода пряма тут 
"""

class Pl:
    # Характеристеки самого игрока
    x = 340
    y = 330
    width = 50
    height = 100
    color = (54, 136, 181)

    # Характеристики здаровья
    HP_playr = 5               # Количество здоровья
    HP_One = width / HP_playr  # Длина одной еденице здаровья
    Polosa = HP_playr * HP_One # Полоска HP

    # Пакет для обединения HP и playr
    pl = pyglet.graphics.Batch()
    def playr(self): #Создание и отображение игрока
        self.playr = sh.Rectangle(Pl.x, Pl.y, Pl.width, Pl.height, Pl.color, batch=Pl.pl)
        return self.playr

    # HP игрока
    def HP(self):
        self.HP = sh.Rectangle(Pl.x, Pl.y + Pl.height, Pl.Polosa, 15, color=(255,0,0), batch=Pl.pl)
        return self.HP

    def draw(): # Отрисовка пакета данных с игроком и его полоской так как они должны передвигаться одновременно и одинаково
        Pl.pl.draw() 


class Stena: # Характеристики стен для их отображения
    wind_width, wind_height = (720, 720)
    LeftNiz_X = wind_width / 2 - 120
    LeftNiz_Y =  wind_height / 2 - 120
    LeftVerh_X = wind_width / 2 - 120
    LeftVerh_Y =  wind_height / 2 + 120

    RightNiz_X = wind_width / 2 + 120
    RightNiz_Y =  wind_height / 2 - 120
    RightVerh_X = wind_width / 2 + 120
    RightVerh_Y =  wind_height / 2 + 120

    Shir_S = 20
    left_S = (
        LeftNiz_X, 
        LeftNiz_Y - Shir_S / 2,
        LeftVerh_X,
        LeftVerh_Y + Shir_S / 2
    )
    right_S = (
        RightNiz_X, 
        RightNiz_Y - Shir_S / 2,
        RightVerh_X, 
        RightVerh_Y + Shir_S / 2
    )
    verh_S = (
        LeftVerh_X - Shir_S / 2, 
        LeftVerh_Y, 
        RightVerh_X + Shir_S / 2,
        RightVerh_Y
    )
    niz_S = (
        LeftNiz_X + 120 - Shir_S / 2,
        LeftNiz_Y, 
        RightNiz_X + Shir_S / 2,
        RightNiz_Y
    )
    
    dom = pyglet.graphics.Batch() # Пакет данных со всеми стенами

    def __init__(self): # Отображение стен (смотри на названия какая это стена)
        self.wall_left = sh.Line(Stena.left_S[0], Stena.left_S[1], 
                                Stena.left_S[2], Stena.left_S[3], 
                                thickness=Stena.Shir_S, batch=Stena.dom)

        self.wall_right = sh.Line(Stena.right_S[0], Stena.right_S[1], 
                                Stena.right_S[2], Stena.right_S[3], 
                                thickness=Stena.Shir_S, batch=Stena.dom)

        self.wall_verh = sh.Line(Stena.verh_S[0], Stena.verh_S[1], 
                                Stena.verh_S[2], Stena.verh_S[3],
                                thickness=Stena.Shir_S, batch=Stena.dom)

        self.wall_niz = sh.Line(Stena.niz_S[0], Stena.niz_S[1], 
                                Stena.niz_S[2], Stena.niz_S[3], 
                                thickness=Stena.Shir_S, batch=Stena.dom) 
        self.shipi = sh.Rectangle(200, 200, 20, 20, color=(111,111,111), batch=Stena.dom)

    def draw(self): # Пакет для отображения стен
        Stena.dom.draw()

