import pyglet 
import os

class Animation:
    filу_python = os.path.dirname(__file__)
    file_game = os.path.dirname(filу_python)
    print(file_game)
    imgs_left = (
        pyglet.image.load(str(file_game)+"/img/left_f0.png"), 
        pyglet.image.load(str(file_game)+"/img/left_f1.png")
        )

    imgs_right = (
        pyglet.image.load(str(file_game)+"/img/right_f0.png"), 
        pyglet.image.load(str(file_game)+"/img/right_f1.png")
        )

    batch1 = pyglet.graphics.Batch()
    batch2 = pyglet.graphics.Batch()

    animation_right = pyglet.image.Animation.from_image_sequence(
        imgs_right, 
        duration=0.4,  # время показа одного кадра
        loop=True      # анимация повторяется
        )

    animation_left = pyglet.image.Animation.from_image_sequence(
        imgs_left, 
        duration=0.4,  # время показа одного кадра
        loop=True
        )      # анимация повторяется


    def fox(self, x=0, y=0, playr_x=0, img_name=''): # Добавить автоматизацию
        self.sprite_right = pyglet.sprite.Sprite(self.animation_right, x, y)
        self.sprite_left = pyglet.sprite.Sprite(self.animation_left, x, y)
        
        self.sprite_right.scale = 0.06
        self.sprite_left.scale = 0.06
        if playr_x > 0:
            return self.sprite_right
        return self.sprite_left
    