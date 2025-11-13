# Управление 
class Managment:
    def __init__(self, player, HP, screens):
        self.player = player
        self.HP = HP
        self.screens = screens

    #   Передвижеие игрока и его полоски жизни
    def player_moving(self, x, y, avanpost):
        # left - линия огранияения ухода влево
        # right - линия огранияения ухода вправо
        # bottom - линия огранияения ухода вниз
        # top - линия огранияения ухода вверх
        left, right = 0, self.screens.width - self.player.width 
        bottom, top = 0, self.screens.height - self.player.height - self.HP.height

        map_x = left < self.player.x + x < right
        map_y = bottom < self.player.y + y < top
        if map_x and avanpost:
            self.player.x += x
            self.HP.x += x
        if map_y and avanpost:
            self.player.y += y
            self.HP.y += y
