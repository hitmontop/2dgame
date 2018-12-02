from pico2d import*
import game_world
import game_framework

import unit_functions
import main_state

class IdleState:

    @staticmethod
    def enter(unit):
        pass

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        unit.lapse_time -= game_framework.frame_time
        if unit.lapse_time <= 0:
            game_world.remove_object(unit)

        if unit.mouse_collide():
            unit.sun_sound.play()
            unit.add_event(FlyingState)



    @staticmethod
    def draw(unit):
        cx, cy = unit_functions.get_cx_cy(unit.x, unit.y)

        unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, 0, unit.IMAGE_SIZE, unit.IMAGE_SIZE, cx, cy)


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
            game_world.money += unit.cost
            game_world.remove_object(unit)

        unit.dir = math.atan2(unit.temp_y - unit.y, unit.temp_x - unit.x)

        unit.x += unit.RUN_SPEED_PPS * math.cos(unit.dir) * game_framework.frame_time
        unit.y += unit.RUN_SPEED_PPS * math.sin(unit.dir) * game_framework.frame_time


    @staticmethod
    def draw(unit):
        cx, cy = unit_functions.get_cx_cy(unit.x, unit.y)

        unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, 0, unit.IMAGE_SIZE, unit.IMAGE_SIZE, cx, cy)



class ResourceSun:
    image = None
    cost = 50

    def __init__(self, x, y):
        self.IMAGE_SIZE = 80

        self.PIXEL_PER_METER = (100 / 0.02)
        self.RUN_SPEED_KMPH = 0.4
        self.RUN_SPEED_MPM = (self.RUN_SPEED_KMPH * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * self.PIXEL_PER_METER)

        self.EXPLODING_TIME_PER_ACTION = 0.3
        self.EXPLODING_ACTION_PER_TIME = 1.0 / self.EXPLODING_TIME_PER_ACTION
        self.EXPLODING_FRAMES_PER_ACTION = 4

        self.target = main_state.moeny_indicator
        self.obj_left, self.obj_bottom, self.obj_right, self.obj_top = 0, 0, 0, 0
        self.frame = 0
        self.init_time = 0
        self.dir = 0

        self.image_dir = 0
        self.DIR_CHANGE_TIME = 0.5
        self.dir_time = self.DIR_CHANGE_TIME

        self.LAPSE_TIME = 5
        self.lapse_time = self.LAPSE_TIME

        self.x, self.y = x, y
        self.temp_x, self.temp_y = x, y

        self.sun_sound = load_wav('resource\\sound\\sun.wav')
        self.sun_sound.set_volume(100)

        self.event_que = []
        self.cur_state = IdleState

        if ResourceSun.image is None:
            ResourceSun.image = load_image('resource\\image\\sun_resource.png')

        self.add_self()


    def add_self(self):
        game_world.add_object(self, 5)

    def get_target_bb(self):
        self.obj_left, self.obj_bottom, self.obj_right, self.obj_top = self.target.get_bb()

    def mouse_collide(self):
        if self.x + self.IMAGE_SIZE //2 < main_state.camera.x - main_state.canvas_width //2  + game_world.x: return False
        if self.x - self.IMAGE_SIZE //2 > main_state.camera.x - main_state.canvas_width //2  + game_world.x: return False
        if self.y + self.IMAGE_SIZE //2 < main_state.camera.y - main_state.canvas_height //2  + game_world.y: return False
        if self.y - self.IMAGE_SIZE //2 > main_state.camera.y - main_state.canvas_height //2  + game_world.y: return False
        return True

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

        self.dir_time -= game_framework.frame_time
        if self.dir_time <= 0:
            self.image_dir += math.pi // 6
            self.dir_time += self.DIR_CHANGE_TIME

        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self)
            self.cur_state = event
            self.cur_state.enter(self)

    def draw(self):
        self.cur_state.draw(self)
