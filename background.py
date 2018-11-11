from pico2d import*

class Background:
    def __init__(self):
        self.image = load_image('resource\\image\\background2.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(600, 400)