import pyglet
from pyglet import shapes as sh
from pyglet.window import key


class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.knop_height = self.height // 8
        self.pak = pyglet.graphics.Batch()

        self.x1 = self.width // 3
        self.x2 = self.x1 * 2
        self.y_play = (self.height // 5) * 2
        self.y_settings = self.y_play - self.knop_height - 20
        self.y_exat = self.y_settings - self.knop_height - 20


        pyglet.font.add_file("SevenExEightPixel-Regular.otf")

        self.text_play = pyglet.text.Label(
            "Играть", self.width // 2.3, self.y_play - 20, 
            font_size=27, font_name='SevenExEight Pixel', 
            color=(13, 13, 13), batch=self.pak
            )

        self.text_settings = pyglet.text.Label(
            "Настройки", self.width // 2.5, self.y_settings - 20, 
            font_size=27, font_name='SevenExEight Pixel', 
            color=(13, 13, 13), batch=self.pak
            )

        self.text_exat = pyglet.text.Label(
            "Выход", self.width // 2.3, self.y_exat - 20, 
            font_size=27, font_name='SevenExEight Pixel', 
            color=(13, 13, 13), batch=self.pak
            )


        self.knop_play = sh.Line(
            self.x1, self.y_play, self.x2, self.y_play, 
            self.knop_height, color=(133, 133, 133), batch=self.pak
            )
        
        self.knop_settings = sh.Line(
            self.x1, self.y_settings, self.x2, self.y_settings, 
            self.knop_height, color=(133, 133, 133), batch=self.pak
            )
        
        self.knop_exat = sh.Line(
            self.x1, self.y_exat, self.x2, self.y_exat, 
            self.knop_height, color=(133, 133, 133), batch=self.pak
            )

    def key(self, x, y):
        X = self.x2 > x > self.x1
        height_ser = self.knop_height // 2

        self.key_play = X and self.y_play + height_ser > y > self.y_play - height_ser
        self.key_settings = X and self.y_settings + height_ser > y > self.y_settings - height_ser
        self.key_exat = X and self.y_exat + height_ser > y > self.y_exat - height_ser

        self.key_menu = 100 > x > 10 and 720 > y > 620 



    def draw(self):
        self.pak.draw()











