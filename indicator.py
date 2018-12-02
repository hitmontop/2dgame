from pico2d import*
import unit_functions
import game_world
import main_state

import random
import game_framework

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
        self.x =clamp (200, self.x, main_state.background.w//2 + 500)

    def handle_event(self, event):
        pass

class PauseMark:
    def __init__(self):
        self.image = load_image('resource\\image\\pause_mark.png')
        self.IMAGE_SIZE = self.image.w//2
        self.x, self.y = main_state.canvas_width //2 , main_state.canvas_height//2
        self.frame = 0
        self.add_self()

        self.BLINK_TIME_PER_ACTION = 1
        self.BLINK_ACTION_PER_TIME = 1.0 / self.BLINK_TIME_PER_ACTION
        self.BLINK_FRAMES_PER_ACTION = 2


    def add_self(self):
        game_world.add_object(self, 5)

    def draw(self):
        self.image.clip_draw(int(self.frame) * self.IMAGE_SIZE, self.IMAGE_SIZE * 0, self.IMAGE_SIZE,
                             self.IMAGE_SIZE, self.x, self.y)


    def update(self):
        self.frame = (self.frame + self.BLINK_FRAMES_PER_ACTION *
                      self.BLINK_ACTION_PER_TIME * game_framework.frame_time) % self.BLINK_FRAMES_PER_ACTION

    def handle_event(self, event):
        pass


class MoneyIndicator:
    def __init__(self):
        self.cx, self.cy = 80, 650

        self.image = load_image('resource\\image\\sun_resource.png')
        self.IMAGE_SIZE = self.image.w
        self.x = main_state.camera.x - main_state.canvas_width //2 + self.cx
        self.y = main_state.camera.y - main_state.canvas_height //2 + self.cy
        self.add_self()

        self.font = load_font('ENCR10B.TTF', 30)




    def add_self(self):
        game_world.add_object(self, 5)

    def draw(self):
        self.image.draw(self.cx, self.cy, self.IMAGE_SIZE, self.IMAGE_SIZE)
        self.font.draw(self.cx+ 50, self.cy, '%d' % game_world.money, (255, 255, 0))

    def update(self):
        self.x = main_state.camera.x - main_state.canvas_width //2 + 100
        self.y = main_state.camera.y - main_state.canvas_height //2 + 600


    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.x - (self.IMAGE_SIZE) // 2, \
               self.y - (self.IMAGE_SIZE) // 2, \
               self.x + (self.IMAGE_SIZE) // 2, \
               self.y + (self.IMAGE_SIZE) // 2