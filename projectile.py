from pico2d import*
import game_world
import game_framework


class FlyingState:

    @staticmethod
    def enter(unit):
        pass

    @staticmethod
    def exit(unit):
        if unit.target.hp > 0:
            unit.attack_target()

    @staticmethod
    def do(unit):
        distance = game_framework.frame_time * unit.velocity

        if unit.i < 100:
            unit.i = unit.i + 2
            t = unit.i / 100
            unit.x = (1 - t) * unit.x + t * unit.destination_x
            unit.y = (1 - t) * unit.y + t * unit.destination_y

        else:
            unit.add_event(ExplodingState)



    @staticmethod
    def draw(unit):
        unit.image.clip_draw(0, unit.IMAGE_SIZE * 1, unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)


class ExplodingState:

    @staticmethod
    def enter(unit):
        unit.init_time = get_time()

    @staticmethod
    def exit(unit):
        game_world.remove_object(unit)

    @staticmethod
    def do(unit):
        unit.frame = (unit.frame + unit.EXPLODING_FRAMES_PER_ACTION * unit.EXPLODING_ACTION_PER_TIME * game_framework.frame_time) % unit.EXPLODING_FRAMES_PER_ACTION

        if get_time() - unit.init_time >= unit.EXPLODING_TIME_PER_ACTION:
            unit.add_event(FlyingState)

    @staticmethod
    def draw(unit):
        unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, 0, unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)



class Projectile:

    def __init__(self):
        self.IMAGE_SIZE = 0

        self.PIXEL_PER_METER = 0
        self.RUN_SPEED_KMPH = 0
        self.RUN_SPEED_MPM = (self.RUN_SPEED_KMPH * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * self.PIXEL_PER_METER)

        self.FLYING_TIME_PER_ACTION = 0
        self.FLYING_ACTION_PER_TIME = 0
        self.FLYING_FRAMES_PER_ACTION = 0

        self.EXPLODING_TIME_PER_ACTION = 0
        self.EXPLODING_ACTION_PER_TIME = 0
        self.EXPLODING_FRAMES_PER_ACTION = 0

        self.i = 0
        self.target = None
        self.frame = 0
        self.init_time = 0

        self.velocity = self.RUN_SPEED_PPS
        self.x, self.y = 0, 0
        self.destination_x, self.destination_y = 0, 0

        self.damage = 0

        self.event_que = []
        self.cur_state = FlyingState

    def attack_target(self):
        self.target.hp -= self.damage

######################################################################

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