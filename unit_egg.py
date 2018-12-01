from pico2d import*
import game_world
import game_framework
import unit_functions
import unit_list

from hp_bar import HpBar

UNIT_LIST = 2

class WaitingState:

    @staticmethod
    def enter(unit):
        pass

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        unit.frame = (unit.frame + unit.WAITING_FRAMES_PER_ACTION *
                      unit.WAITING_ACTION_PER_TIME * game_framework.frame_time) % unit.WAITING_FRAMES_PER_ACTION

        if get_time() - unit.waiting_init_time >= unit.WAITING_TIME_PER_ACTION:
            if unit.is_hatching:
                unit.add_event(HatchState)
            else:
                unit.add_unit()
                unit.delete_this_unit_from_checking_layer()
                game_world.remove_object(unit)


    @staticmethod
    def draw(unit):
        cx, cy = unit_functions.get_cx_cy(unit.x, unit.y)

        unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 2, unit.IMAGE_SIZE,
                             unit.IMAGE_SIZE, cx, cy)

class HatchState:

    @staticmethod
    def enter(unit):
        unit.frame = 0
        unit.hatch_init_time = get_time()

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        unit.frame = (unit.frame + unit.WAITING_FRAMES_PER_ACTION *
                      unit.WAITING_ACTION_PER_TIME * game_framework.frame_time) % unit.WAITING_FRAMES_PER_ACTION

        if get_time() - unit.hatch_init_time >= unit.HATCH_TIME_PER_ACTION:
            unit.add_unit()
            unit.delete_this_unit_from_checking_layer()
            game_world.remove_object(unit)


    @staticmethod
    def draw(unit):
        cx, cy = unit_functions.get_cx_cy(unit.x, unit.y)

        unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 1, unit.IMAGE_SIZE,
                             unit.IMAGE_SIZE, cx, cy)


class DyingState:

    @staticmethod
    def enter(unit):

        unit.frame = 0
        unit.delete_this_unit_from_checking_layer()

        game_world.add_object(unit, 1)
        game_world.pull_object(unit)

        unit.dying_init_time = get_time()

    @staticmethod
    def exit(unit):
        game_world.remove_object(unit)

    @staticmethod
    def do(unit):
        if get_time() - unit.dying_init_time >= unit.DYING_TIME_PER_ACTION:
            unit.add_event(WaitingState)

        unit.frame = (unit.frame + unit.DYING_FRAMES_PER_ACTION *
                    unit.DYING_ACTION_PER_TIME * game_framework.frame_time) % unit.DYING_FRAMES_PER_ACTION

    @staticmethod
    def draw(unit):
        cx, cy = unit_functions.get_cx_cy(unit.x, unit.y)

        unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 0, unit.IMAGE_SIZE,
                                 unit.IMAGE_SIZE, cx, cy)

class Egg:

    def __init__(self):
        self.IMAGE_SIZE

        self.WAITING_TIME_PER_ACTION
        self.WAITING_ACTION_PER_TIME
        self.WAITING_FRAMES_PER_ACTION

        self.HATCH_TIME_PER_ACTION
        self.HATCH_ACTION_PER_TIME
        self.HATCH_FRAMES_PER_ACTION

        self.DYING_TIME_PER_ACTION
        self.DYING_ACTION_PER_TIME
        self.DYING_FRAMES_PER_ACTION

        self.is_air_unit
        self.is_foe

        self.is_hatching
        self.max_hp
        self.hp

        self.frame
        self.x, self.y

        self.event_que
        self.cur_state

        self.waiting_init_time
        self.hatch_init_time
        self.dying_init_time


    def add_unit(self):
        pass

    def delete_this_unit_from_checking_layer(self):
        if self.is_foe:
            game_world.computer_all_unit.remove(self)
            if self.is_air_unit:
                game_world.computer_air_unit.remove(self)
            else:
                game_world.computer_ground_unit.remove(self)
        else:
            game_world.player_all_unit.remove(self)
            if self.is_air_unit:
                game_world.player_air_unit.remove(self)
            else:
                game_world.player_ground_unit.remove(self)

        game_world.remove_object(self.hp_bar)


    def add_self(self):
        game_world.add_object(self, UNIT_LIST)

        if self.is_foe:
            game_world.computer_all_unit.append(self)
            if self.is_air_unit:
                game_world.computer_air_unit.append(self)
            else:
                game_world.computer_ground_unit.append(self)
        else:
            game_world.player_all_unit.append(self)
            if self.is_air_unit:
                game_world.player_air_unit.append(self)
            else:
                game_world.player_ground_unit.append(self)

    def get_bb(self):
        return self.x - (self.IMAGE_SIZE) // 2, \
               self.y - (self.IMAGE_SIZE) // 2, \
               self.x + (self.IMAGE_SIZE) // 2, \
               self.y + (self.IMAGE_SIZE) // 2

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        if unit_functions.is_this_unit_dead(self):
            if (self.cur_state is DyingState) is False:
                self.add_event(DyingState)

        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self)
            self.cur_state = event
            self.cur_state.enter(self)

    def draw(self):
        self.cur_state.draw(self)


class Bloom(Egg):
    image = None
    def __init__(self, x, y, is_foe):
        self.IMAGE_SIZE = 150

        self.WAITING_TIME_PER_ACTION = 10
        self.WAITING_ACTION_PER_TIME = 1.0 / self.WAITING_TIME_PER_ACTION
        self.WAITING_FRAMES_PER_ACTION = 4

        self.HATCH_TIME_PER_ACTION = 1
        self.HATCH_ACTION_PER_TIME = 1.0 / self.HATCH_TIME_PER_ACTION
        self.HATCH_FRAMES_PER_ACTION = 0

        self.DYING_TIME_PER_ACTION = 2
        self.DYING_ACTION_PER_TIME = 1.0 / self.DYING_TIME_PER_ACTION
        self.DYING_FRAMES_PER_ACTION = 1
        self.dying_init_time = 0

        self.is_air_unit = False
        self.is_foe = is_foe

        self.is_hatching = False
        self.max_hp = 1
        self.hp = 1

        self.frame = 0
        self.x, self.y = x, y
        self.opacity = 1

        self.event_que = []
        self.cur_state = WaitingState

        self.waiting_init_time = get_time()
        self.hatch_init_time =0
        self.dying_init_time = 0

        hp_bar = HpBar(self.x, self.y, self.max_hp, self.max_hp, self.is_foe, self)
        self.hp_bar = hp_bar
        game_world.add_object(hp_bar, 4)


        if Bloom.image is None:
            Bloom.image = load_image('resource\\image\\unit\\bloom.png')

        self.add_self()

    def get_bb(self):
        return self.x - (self.IMAGE_SIZE - 100) // 2, \
               self.y - (self.IMAGE_SIZE - 100) // 2, \
               self.x + (self.IMAGE_SIZE - 100) // 2, \
               self.y + (self.IMAGE_SIZE - 100) // 2

    def add_unit(self):
        unit_list.Turret(self.x, self.y, self.is_foe)