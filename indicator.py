from pico2d import*
import unit_functions
import game_world
import main_state

import random

class Indicator_1:
    def __init__(self):
        self.image = load_image('resource\\image\\indicator.png')
        self.IMAGE_SIZE = self.image.w
        self.x = main_state.camera.x - main_state.canvas_width //2  + game_world.x
        self.true_y = unit_functions.GROUND_HEIGHT_FOR_INDICATORS
        self.y = self.true_y + random.randint(0, 40)
        self.add_self()

    def add_self(self):
        game_world.add_object(self, 5)

    def draw(self):
        cx, cy = unit_functions.get_cx_cy(self.x, self.true_y)
        self.image.draw(cx, cy, self.IMAGE_SIZE, self.IMAGE_SIZE)

    def update(self):
        self.x = main_state.camera.x - main_state.canvas_width //2  + game_world.x
        self.x =clamp (0, self.x, main_state.background.w//2 + 500)

    def handle_event(self, event):
        pass