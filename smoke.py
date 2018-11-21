
from pico2d import*
import game_world
import game_framework

class IdleState:

    @staticmethod
    def enter(unit):
        pass

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        if unit.opacity <= 0:
            unit.delete_this_unit()



        unit.generate_smoke_time -= game_framework.frame_time

        unit.opacity_decrease()


    @staticmethod
    def draw(unit):
        unit.image.opacify(unit.opacity)

        if unit.opacity > 0.8:
            unit.image.clip_draw(unit.IMAGE_SIZE * 4, 0, unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)

        elif unit.opacity > 0.6:
            unit.image.clip_draw(unit.IMAGE_SIZE * 3, 0, unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)

        elif unit.opacity > 0.4:
            unit.image.clip_draw(unit.IMAGE_SIZE * 2, 0, unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)

        elif unit.opacity > 0.2:
            unit.image.clip_draw(unit.IMAGE_SIZE * 1, 0, unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)

        else:
            unit.image.clip_draw(unit.IMAGE_SIZE * 0, 0, unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)



class Smoke:
    def __init__(self, x, y):
        self.IMAGE_SIZE = 50

        self.PIXEL_PER_METER = (100 / 0.02)

        self.EXPLODING_TIME_PER_ACTION = 2
        self.EXPLODING_ACTION_PER_TIME = 1.0 / self.EXPLODING_TIME_PER_ACTION
        self.EXPLODING_FRAMES_PER_ACTION = 1


        self.x, self.y = x, y
        self.opacity = 1
        self.generate_smoke_time = 0.1

        self.event_que = []
        self.cur_state = IdleState

        self.image = load_image('resource\\image\\projectile\\smoke.png')

        self.add_self()

    def delete_this_unit(self):
        game_world.remove_object(self)

    def opacity_decrease(self):
        self.generate_smoke_time -= game_framework.frame_time
        if self.generate_smoke_time <= 0:
            self.opacity -= 0.05
            self.generate_smoke_time += 0.1

    def add_self(self):
        game_world.add_object(self, 1)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self)
            self.cur_state = event
            self.cur_state.enter(self)

    def draw(self):
        self.cur_state.draw(self)


