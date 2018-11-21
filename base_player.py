from pico2d import *
import game_framework
import game_world

from ant import Ant
from spitter_ant import SpitterAnt
from bee import Bee

import random


class IdleState:

    @staticmethod
    def enter(unit):
        pass

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        if unit.is_this_unit_dead():
            unit.add_event(ExplodingState)

    @staticmethod
    def draw(unit):
        unit.image.clip_draw(0, 5 * unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)



class ExplodingState:

    @staticmethod
    def enter(unit):
        unit.delete_this_unit_from_checking_layer()
        game_world.pull_object(unit)
        game_world.add_object(unit, 1)

        unit.init_time = get_time()

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):

        unit.frame = (unit.frame + unit.EXPLODING_FRAMES_PER_ACTION *
                      unit.EXPLODING_ACTION_PER_TIME * game_framework.frame_time) % unit.EXPLODING_FRAMES_PER_ACTION

        if get_time() - unit.init_time >= unit.EXPLODING_TIME_PER_ACTION:
            unit.add_event(BrokenState)

    @staticmethod
    def draw(unit):
        unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, 4 * unit.IMAGE_SIZE, unit.IMAGE_SIZE,
                                 unit.IMAGE_SIZE, unit.x, unit.y)



class BrokenState:

    @staticmethod
    def enter(unit):
        pass

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        pass

    @staticmethod
    def draw(unit):
        unit.image.clip_draw(0, 3 * unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)



class PlayerBase:

    def __init__(self, x, y):

        self.IMAGE_SIZE = 300
        self.PIXEL_PER_METER = (100 / 0.02)

        self.EXPLODING_TIME_PER_ACTION = 0.5
        self.EXPLODING_ACTION_PER_TIME = 1.0 / self.EXPLODING_TIME_PER_ACTION
        self.EXPLODING_FRAMES_PER_ACTION = 5

        self.event_que = []
        self.cur_state = IdleState

        self.max_hp = 100
        self.hp = 100

        self.x = x
        self.y = y

        self.frame = 0
        self.init_time = 0

        self.is_foe = False

        self.is_air_unit = False

        self.image = load_image('resource\\image\\unit\\base.png')
        self.font = load_font('ENCR10B.TTF', 16)

        self.add_self()

        self.init_time = 0
        self.cnt = 0

    def add_self(self):
        game_world.add_object(self, 2)

        game_world.player_all_unit.append(self)
        game_world.player_ground_unit.append(self)

    def delete_this_unit_from_checking_layer(self):
        game_world.player_all_unit.remove(self)
        game_world.player_ground_unit.remove(self)

    def generate_unit(self):
        ant = Ant(random.randint(100, 1100), self.y- random.randint(20,50), self.is_foe)
        ant = Ant(random.randint(100, 1100), self.y - random.randint(20, 50), True)

    def get_bb(self):
        return self.x - (self.IMAGE_SIZE - 80) // 2, \
               self.y - (self.IMAGE_SIZE - 70) // 2, \
               self.x + (self.IMAGE_SIZE - 80) // 2, \
               self.y + (self.IMAGE_SIZE - 70) // 2

    def is_this_unit_dead(self):
        if self.hp <= 0:
            return True
        elif self.x < 0 or self.x > 1200:
            self.hp = 0
            return True

        return False

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        if get_time() - self.init_time > 2 and self.cnt < 3:
            self.init_time = get_time()
            self.cnt += 1

        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self)
            self.cur_state = event
            self.cur_state.enter(self)

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())
