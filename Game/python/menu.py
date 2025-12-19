import pyglet
from pyglet import shapes as sh
from pyglet.window import key
from objects import all_batch


class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.knop_height = self.height // 8
        pyglet.font.add_file("SevenExEightPixel-Regular.otf")
        self.gr = pyglet.graphics.Group(993)

        self.x1 = self.width // 3
        self.x2 = self.x1 * 2
        self.y_play = (self.height // 5) * 2
        self.y_settings = self.y_play - self.knop_height - 20
        self.y_exat = self.y_settings - self.knop_height - 20

        self.y_menu = 620
        self.x1_menu = 10
        self.x2_menu = 110
    
    def game(self):
        self.menu_key = sh.Line(
            self.x1_menu, self.y_menu, self.x2_menu, self.y_menu, 
            self.knop_height, color=(133, 133, 133), 
            batch=all_batch, group=self.gr
            )
        
        self.menu_text = pyglet.text.Label( 
                '||', self.x1_menu + 39, self.y_menu - 30, 
                font_size=40, font_name='SevenExEight Pixel', 
                color=(13, 13, 13), batch=all_batch, group=self.gr
                )

    
    def stop(self):
        self.keys_texts = {
            self.y_play: "Играть", 
            self.y_settings: "Настройки", 
            self.y_exat: "Выйти"
            }
    
        self.keys_click = list(self.keys_texts)
        self.knop = []
        
        for y in self.keys_texts: # Цикл для создания клавишь и текста на них
            text = self.keys_texts[y]
            x = self.width // 2 - len(text) * 16

            self.knop.append(
                (   # Создание клавиши
                    sh.Line(
                        self.x1, y, self.x2, y, 
                        self.knop_height, color=(133, 133, 133)
                        ),
                    # Создание текста
                    pyglet.text.Label( 
                        text, x, y - 20, font_size=27, 
                        font_name='SevenExEight Pixel', color=(13, 13, 13)
                        )
                    )
                )
            

    def key(self, x, y):
        X = self.x2 > x > self.x1
        height_ser = self.knop_height // 2

        self.key_menu = (
            self.x2_menu > x > self.x1_menu and 
            self.y_menu + height_ser > y > self.y_menu - height_ser
            )
        
        list_keys_texts = list(self.keys_texts)
        for i in range(len(self.keys_click)):
            self.keys_click[i] = (
                list_keys_texts[i] + height_ser > y > 
                list_keys_texts[i] - height_ser and X
                )
            if self.keys_click[i]:
                return

    def draw(self):
        for i in self.knop:
            i[0].draw()
            i[1].draw()









