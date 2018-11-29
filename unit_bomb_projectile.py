from pico2d import*
import game_world
import game_framework
import smoke
import unit_functions

class FlyingState:

    @staticmethod
    def enter(unit):
        pass

    @staticmethod
    def exit(unit):
        unit.search_unit_in_exploding_range()

    @staticmethod
    def do(unit):
        if unit.collide():
            unit.add_event(ExplodingState)

        unit.dir = math.atan2(unit.destination_y - unit.y, unit.destination_x - unit.x)

        unit.x += unit.RUN_SPEED_PPS * math.cos(unit.dir) * game_framework.frame_time
        unit.y += unit.RUN_SPEED_PPS * math.sin(unit.dir) * game_framework.frame_time

        unit.generate_smoke_time -= game_framework.frame_time
        if unit.generate_smoke_time <= 0:
            smoke.Smoke(unit.x, unit.y)
            unit.generate_smoke_time += 0.1



    @staticmethod
    def draw(unit):
        cx, cy = unit_functions.get_cx_cy(unit.x, unit.y)

        if math.cos(unit.dir) > 0:
            unit.image.clip_draw(0, unit.IMAGE_SIZE * 0, unit.IMAGE_SIZE,
                                 unit.IMAGE_SIZE, cx, cy)
        else:
            unit.image.clip_draw(0, unit.IMAGE_SIZE * 1, unit.IMAGE_SIZE,
                                 unit.IMAGE_SIZE, cx, cy)


class ExplodingState:

    @staticmethod
    def enter(unit):
        unit.explode_sound.play()
        game_world.remove_object(unit)

    @staticmethod
    def exit(unit):
        game_world.remove_object(unit)

    @staticmethod
    def do(unit):
        pass

    @staticmethod
    def draw(unit):
        pass



class BombProjectile:

    def __init__(self):
        self.IMAGE_SIZE = 0

        self.PIXEL_PER_METER = (100 / 0.02)
        self.RUN_SPEED_KMPH = 0.1
        self.RUN_SPEED_MPM = (self.RUN_SPEED_KMPH * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * self.PIXEL_PER_METER)

        self.EXPLODING_TIME_PER_ACTION = 0.3
        self.EXPLODING_ACTION_PER_TIME = 1.0 / self.EXPLODING_TIME_PER_ACTION
        self.EXPLODING_FRAMES_PER_ACTION = 4

        self.generate_smoke_time = 0

        self.valid_target_list = []
        self.target = None
        self.frame = 0
        self.init_time = 0
        self.radius = 0

        self.x, self.y = 0, 0
        self.destination_x, self.destination_y = 0, 0
        self.dir = 0
        self.damage = 0

        self.event_que = []
        self.cur_state = FlyingState

        self.add_self()

        self.explode_sound = None

    def add_self(self):
        game_world.add_object(self, 4)

    def attack_target(self, o):
        o.hp -= self.damage

    def search_unit_in_exploding_range(self):
        if (self.valid_target_list is None) is False:
            for o in self.valid_target_list:
                if self.collide_explosion_radius(o):
                    self.attack_target(o)

    def collide(self):
        if self.destination_x - 20 > self.x: return False
        if self.destination_y + 20 < self.y: return False
        if self.destination_x + 20 < self.x: return False
        if self.destination_y - 20 > self.y: return False
        return True

    def collide_explosion_radius(self, o):
        left, bottom, right, top = o.get_bb()
        if self.x - self.radius > right: return False
        if self.y + self.radius < bottom: return False
        if self.x + self.radius < left: return False
        if self.y - self.radius > top: return False
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




class ProjectileBazookaBug(BombProjectile):
    image = None

    def __init__(self, x, y, target, vaild_target_list, damage):
        self.IMAGE_SIZE = 90

        self.PIXEL_PER_METER = (100 / 0.02)
        self.RUN_SPEED_KMPH = 0.2
        self.RUN_SPEED_MPM = (self.RUN_SPEED_KMPH * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * self.PIXEL_PER_METER)

        self.generate_smoke_time = 0.1

        self.valid_target_list = vaild_target_list
        self.target = target
        self.frame = 0
        self.init_time = 0
        self.radius = 40

        self.x, self.y = x, y
        self.destination_x, self.destination_y = target.x, target.y
        self.dir = math.atan2(self.destination_y - self.y, self.destination_x - self.x)

        self.damage = damage

        self.event_que = []
        self.cur_state = FlyingState

        self.explode_sound = load_wav('resource\\sound\\bomb_explosion.wav')
        self.explode_sound.set_volume(32)

        if ProjectileBazookaBug.image is None:
            self.image = load_image('resource\\image\\projectile\\dragon_bomb.png')

        self.add_self()


class ProjectileBomBardDragonFly(BombProjectile):
    image = None

    def __init__(self, x, y, target, vaild_target_list, damage):
        self.IMAGE_SIZE = 90

        self.PIXEL_PER_METER = (100 / 0.02)
        self.RUN_SPEED_KMPH = 0.2
        self.RUN_SPEED_MPM = (self.RUN_SPEED_KMPH * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * self.PIXEL_PER_METER)

        self.generate_smoke_time = 0.1

        self.valid_target_list = vaild_target_list
        self.target = target
        self.frame = 0
        self.init_time = 0
        self.radius = 50

        self.x, self.y = x, y
        self.destination_x, self.destination_y = target.x, target.y

        if self.x <= self.destination_x:
            self.dir = 0
        else:
            self.dir= math.pi

        self.damage = damage

        self.event_que = []
        self.cur_state = FlyingState

        self.explode_sound = load_wav('resource\\sound\\bomb_explosion.wav')
        self.explode_sound.set_volume(32)
        self.fire_sound = load_wav('resource\\sound\\bomb_fall.wav')
        self.fire_sound.set_volume(20)

        if ProjectileBomBardDragonFly.image is None:
            self.image = load_image('resource\\image\\projectile\\dragon_bomb.png')

        self.add_self()

        self.fire_sound.play()