# Управление 
class Uprav:
    def __init__(self, playr, HP, width):
        self.playr = playr
        self.HP = HP
        self.width = width

    #   Передвижеие игрока и его полоски жизни
    def pl_moving(self, x, y, avanpost):
        self.x = x
        self.y = y
        if 0 < self.playr.x + x < 721 - self.width and avanpost:
            self.playr.x += x
            self.HP.x += x
        if 0 < self.playr.y + y < 721 - self.width and avanpost:
            self.playr.y += y
            self.HP.y += y
