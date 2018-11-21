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

        if (unit.target is None) is False:
            unit.get_target_bb()
            unit.temp_x, unit.temp_y = unit.target.x, unit.target.y

        if unit.collide():
            unit.add_event(ExplodingState)

        unit.dir = math.atan2(unit.temp_y - unit.y, unit.temp_x - unit.x)

        unit.x += unit.RUN_SPEED_PPS * math.cos(unit.dir) * game_framework.frame_time
        unit.y += unit.RUN_SPEED_PPS * math.sin(unit.dir) * game_framework.frame_time


        #0unit.add_event(ExplodingState)



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



class HomingProjectile:

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

        self.target = None
        self.obj_left, self.obj_bottom, self.obj_right, self.obj_top = 0, 0, 0, 0
        self.frame = 0
        self.init_time = 0

        self.x, self.y = 0, 0
        self.temp_x, self.temp_y = 0, 0
        self.dir = math.atan2(self.target.y - self.y, self.target.x - self.x)

        self.damage = 0

        self.event_que = []
        self.cur_state = FlyingState

        self.add_self()


    def add_self(self):
        game_world.add_object(self, 4)

    def attack_target(self):
        self.target.hp -= self.damage

    def get_target_bb(self):
        self.obj_left, self.obj_bottom, self.obj_right, self.obj_top = self.target.get_bb()

    def collide(self):
        if self.obj_left > self.x: return False
        if self.obj_bottom > self.y: return False
        if self.obj_right < self.x: return False
        if self.obj_top < self.y: return False
        return True



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


















class ProjectileSpitterAnt(HomingProjectile):
    image = None

    def __init__(self, x, y, target, damage):
        self.IMAGE_SIZE = 25

        self.PIXEL_PER_METER = (100 / 0.02)
        self.RUN_SPEED_KMPH = 0.18
        self.RUN_SPEED_MPM = (self.RUN_SPEED_KMPH * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * self.PIXEL_PER_METER)

        self.EXPLODING_TIME_PER_ACTION = 0.3
        self.EXPLODING_ACTION_PER_TIME = 1.0 / self.EXPLODING_TIME_PER_ACTION
        self.EXPLODING_FRAMES_PER_ACTION = 4

        self.target = target
        self.obj_left, self.obj_bottom, self.obj_right, self.obj_top = 0,0,0,0
        self.frame = 0
        self.init_time = 0


        self.x, self.y = x, y
        self.temp_x, self.temp_y = x, y
        self.dir = math.atan2(self.temp_y - self.y, self.temp_x - self.x)

        self.damage = damage

        self.event_que = []
        self.cur_state = FlyingState

        if ProjectileSpitterAnt.image is None:
            self.image = load_image('resource\\image\\projectile\\projectile_spitter_ant.png')

        self.add_self()