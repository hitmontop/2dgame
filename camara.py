import game_world
import game_framework
from pico2d import*

class Camera:
    def __init__(self):
        self.PIXEL_PER_METER = (100 / 0.02)
        self.RUN_SPEED_KMPH = 0.5
        self.RUN_SPEED_MPM = (self.RUN_SPEED_KMPH * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * self.PIXEL_PER_METER)

        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()

        self.x, self.y = self.canvas_width // 2, self.canvas_height // 2
    def update(self):

        if self.collision_left():
            self.x -= self.RUN_SPEED_PPS * game_framework.frame_time

        if self.collision_right():
            self.x += self.RUN_SPEED_PPS * game_framework.frame_time

        self.x = clamp(self.canvas_width // 2, self.x, self.bg.w - self.canvas_width // 2)
        self.y = clamp(self.canvas_height // 2, self.y, self.bg.h - self.canvas_height // 2)


    def set_background(self, bg):
        self.bg = bg
        self.x = self.bg.w / 2
        self.y = self.bg.h / 2

    def draw(self):
        pass

    def collision_left(self):
        if 100 < game_world.x: return False

        if self.y + self.canvas_height//2 - 150 < game_world.y : return False
        if self.y - self.canvas_height//2 + 150 > game_world.y : return False
        return True

    def collision_right(self):
        if self.canvas_width - 100 > game_world.x: return False

        if self.y + self.canvas_height//2 - 150 < game_world.y : return False
        if self.y - self.canvas_height//2 + 150 > game_world.y : return False
        return True

    def handle_event(self, event):
        pass
