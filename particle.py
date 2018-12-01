
from pico2d import*
import game_world
import game_framework
import unit_functions

class IdleState:

    @staticmethod
    def enter(unit):
        pass

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        if unit.exploding_init_time <= 0:
            game_world.remove_object(unit)

        unit.frame = (unit.frame + unit.EXPLODING_FRAMES_PER_ACTION *
                      unit.EXPLODING_ACTION_PER_TIME * game_framework.frame_time) % unit.EXPLODING_FRAMES_PER_ACTION

        unit.exploding_init_time -= game_framework.frame_time
        unit.opacity_timer -= game_framework.frame_time
        if unit.opacity_timer <= 0:
            unit.opacity_decrease()
            unit.opacity_timer += unit.OPAC_DECREASE_TIME



    @staticmethod
    def draw(unit):
        cx, cy = unit_functions.get_cx_cy(unit.x, unit.y)

        unit.image.opacify(unit.opacity)

        unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 0, unit.IMAGE_SIZE,
                             unit.IMAGE_SIZE, cx, cy)



class Particle:
    image = None
    def __init__(self):
        self.IMAGE_SIZE

        self.PIXEL_PER_METER

        self.EXPLODING_TIME_PER_ACTION
        self.EXPLODING_ACTION_PER_TIME
        self.EXPLODING_FRAMES_PER_ACTION
        self.exploding_init_time

        self.OPAC_DECREASE_TIME
        self.opacity_timer

        self.x, self.y
        self.opacity
        self.generate_smoke_time
        self.frame

    def delete_this_unit(self):
        game_world.remove_object(self)

    def opacity_decrease(self):
        self.opacity -= 0.1

    def add_self(self):
        game_world.add_object(self, 4)

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

class Smoke(Particle):
    image = None
    def __init__(self,x ,y):
        self.IMAGE_SIZE = 50

        self.PIXEL_PER_METER = (100 / 0.02)

        self.EXPLODING_TIME_PER_ACTION = 0.8
        self.EXPLODING_ACTION_PER_TIME = 1.0 / self.EXPLODING_TIME_PER_ACTION
        self.EXPLODING_FRAMES_PER_ACTION = 5
        self.exploding_init_time = self.EXPLODING_TIME_PER_ACTION

        self.OPAC_DECREASE_TIME = self.EXPLODING_TIME_PER_ACTION / 10
        self.opacity_timer = self.OPAC_DECREASE_TIME

        self.x, self.y = x, y
        self.opacity = 1
        self.generate_smoke_time = 0.1
        self.frame = 0

        self.event_que = []
        self.cur_state = IdleState

        if Smoke.image is None:
            Smoke.image = load_image('resource\\image\\projectile\\smoke.png')

        self.add_self()


class Explosion(Particle):
    image = None

    def __init__(self, x, y):
        self.IMAGE_SIZE = 125

        self.PIXEL_PER_METER = (100 / 0.02)

        self.EXPLODING_TIME_PER_ACTION = 1
        self.EXPLODING_ACTION_PER_TIME = 1.0 / self.EXPLODING_TIME_PER_ACTION
        self.EXPLODING_FRAMES_PER_ACTION = 14
        self.exploding_init_time = self.EXPLODING_TIME_PER_ACTION

        self.OPAC_DECREASE_TIME = self.EXPLODING_TIME_PER_ACTION / 10
        self.opacity_timer = self.OPAC_DECREASE_TIME

        self.x, self.y = x, y
        self.opacity = 1
        self.generate_smoke_time = 0.1
        self.frame = 0

        self.event_que = []
        self.cur_state = IdleState

        if Explosion.image is None:
            Explosion.image = load_image('resource\\image\\projectile\\explosion1.png')

        self.add_self()


