# Управление 
class Managment:
    def __init__(self, player, screens):
        self.player = player
        self.screens = screens

    #   Передвижеие игрока и его полоски жизни
    def player_moving(self, x, y, avanpost):
        # left - линия огранияения ухода влево
        # right - линия огранияения ухода вправо
        # bottom - линия огранияения ухода вниз
        # top - линия огранияения ухода вверх
        left = 0
        right = self.screens.width - self.player.width 
        bottom = 0
        top = self.screens.height - self.player.height - self.player.hp_entitie.height

        map_x = left < self.player.body_entitie.x + x < right
        map_y = bottom < self.player.body_entitie.y + y < top
        if map_x and avanpost:
            self.player.body_entitie.x += x
            self.player.hp_entitie.x += x
        if map_y and avanpost:
            self.player.body_entitie.y += y
            self.player.hp_entitie.y += y
