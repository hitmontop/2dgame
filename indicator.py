from pico2d import*
import unit_functions
import game_world

class Indicator_1:
    def __init__(self):
        self.image = load_image('resource\\image\\indicator.png')
        self.IMAGE_SIZE = self.image.w
        self.x = game_world.x
        self.add_self()

    def add_self(self):
        game_world.add_object(self, 5)

    def draw(self):
        self.image.draw(game_world.x, unit_functions.GROUND_HEIGHT_FOR_INDICATORS, self.IMAGE_SIZE, self.IMAGE_SIZE)

    def update(self):
        self.x = game_world.x

    def handle_event(self, event):
        pass