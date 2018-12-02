from pico2d import*
import game_world
import game_framework
import unit_functions
import unit_list

import random

from hp_bar import HpBar
from resource_sun import ResourceSun

UNIT_LIST = 2

class IdleState:

    @staticmethod
    def enter(unit):
        pass

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        unit.frame = (unit.frame + unit.IDLE_FRAMES_PER_ACTION *
                      unit.IDLE_ACTION_PER_TIME * game_framework.frame_time) % unit.IDLE_FRAMES_PER_ACTION

        unit.product_init_time -= game_framework.frame_time
        if unit.product_init_time <= 0:
            unit.product_init_time  += unit.PRODUCT_TIME
            ResourceSun(unit.x + 50 +random.randint(-30, 30), unit.y + random.randint(0, 30))



    @staticmethod
    def draw(unit):
        cx, cy = unit_functions.get_cx_cy(unit.x, unit.y)

        unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 0, unit.IMAGE_SIZE,
                             unit.IMAGE_SIZE, cx, cy)


class DyingState:

    @staticmethod
    def enter(unit):

        unit.frame = 0
        unit.delete_this_unit_from_checking_layer()

        game_world.add_object(unit, 1)
        game_world.pull_object(unit)


    @staticmethod
    def exit(unit):
        game_world.remove_object(unit)

    @staticmethod
    def do(unit):
        unit.add_event(IdleState)


    @staticmethod
    def draw(unit):
        pass

class SunFlower:
    image = None
    cost = 50

    def __init__(self, x, y, is_foe):
        self.IMAGE_SIZE = 150

        self.IDLE_TIME_PER_ACTION = 1
        self.IDLE_ACTION_PER_TIME = 1.0 / self.IDLE_TIME_PER_ACTION
        self.IDLE_FRAMES_PER_ACTION = 2

        self.PRODUCT_TIME = 8

        self.product_init_time = self.PRODUCT_TIME

        self.is_air_unit = False
        self.is_foe = is_foe
        self.max_hp = 1
        self.hp = 1

        self.frame = 0
        self.x, self.y = x, y

        self.event_que = []
        self.cur_state = IdleState

        hp_bar = HpBar(self.x, self.y, self.max_hp, self.max_hp, self.is_foe, self)
        self.hp_bar = hp_bar
        game_world.add_object(hp_bar, 4)


        if SunFlower.image is None:
            SunFlower.image = load_image('resource\\image\\unit\\sunflower.png')

        self.add_self()


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