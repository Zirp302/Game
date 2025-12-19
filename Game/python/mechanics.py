import pyglet 
from os import path

class Animation:
    def __init__(self):
        self.filу_python = path.dirname(__file__)
        self.file_game = path.dirname(self.filу_python)
        print(self.file_game)
        self.imgs_left = (
            pyglet.image.load(str(self.file_game)+"/img/left_fox0.png"), 
            pyglet.image.load(str(self.file_game)+"/img/left_fox1.png")
            )

        self.imgs_right = (
            pyglet.image.load(str(self.file_game)+"/img/right_fox0.png"), 
            pyglet.image.load(str(self.file_game)+"/img/right_fox1.png")
            )

        self.animation_right = pyglet.image.Animation.from_image_sequence(
            self.imgs_right, 
            duration=0.4,  # время показа одного кадра
            loop=True      # анимация повторяется
            )

        self.animation_left = pyglet.image.Animation.from_image_sequence(
            self.imgs_left, 
            duration=0.4,  # время показа одного кадра
            loop=True
            )      # анимация повторяется


    def fox(self, x=0, y=0, img_name=''): # Добавить автоматизацию
        self.sprite_right = pyglet.sprite.Sprite(self.animation_right, x, y)
        self.sprite_left = pyglet.sprite.Sprite(self.animation_left, x, y)

        self.sprite_right.scale = 0.06
        self.sprite_left.scale = 0.06
        
        return self.sprite_left, self.sprite_right
    