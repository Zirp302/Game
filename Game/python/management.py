# Управление 
class Managment:
    def __init__(self, playr, HP, screens):
        self.playr = playr
        self.HP = HP
        self.screens = screens

    #   Передвижеие игрока и его полоски жизни
    def playr_moving(self, x, y, avanpost):
        # left - линия огранияения ухода влево
        # right - линия огранияения ухода вправо
        # bottom - линия огранияения ухода вниз
        # top - линия огранияения ухода вверх
        left, right = 0, self.screens.width - self.playr.width 
        bottom, top = 0, self.screens.height - self.playr.height - self.HP.height

        map_x = left < self.playr.x + x < right
        map_y = bottom < self.playr.y + y < top
        if map_x and avanpost:
            self.playr.x += x
            self.HP.x += x
        if map_y and avanpost:
            self.playr.y += y
            self.HP.y += y
