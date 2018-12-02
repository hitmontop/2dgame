from pico2d import*
import game_framework
import game_world

import unit_list
import unit_functions

import random
from hp_bar import HpBar

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
        cx, cy = unit_functions.get_cx_cy(unit.x, unit.y)

        unit.image.clip_draw(0, 2 * unit.IMAGE_SIZE,  unit.IMAGE_SIZE, unit.IMAGE_SIZE, cx, cy)


class ExplodingState:

    @staticmethod
    def enter(unit):
        unit.delete_this_unit_from_checking_layer()

        unit.init_time = unit.EXPLODING_TIME_PER_ACTION

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):

        unit.frame = (unit.frame + unit.EXPLODING_FRAMES_PER_ACTION *
                      unit.EXPLODING_ACTION_PER_TIME * game_framework.frame_time) % unit.EXPLODING_FRAMES_PER_ACTION

        unit.init_time -= game_framework.frame_time
        if unit.init_time <= 0:
            unit.init_time += unit.EXPLODING_TIME_PER_ACTION
            unit.add_event(BrokenState)



    @staticmethod
    def draw(unit):
        cx, cy = unit_functions.get_cx_cy(unit.x, unit.y)

        unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, 1 * unit.IMAGE_SIZE,  unit.IMAGE_SIZE, unit.IMAGE_SIZE, cx, cy)


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
        cx, cy = unit_functions.get_cx_cy(unit.x, unit.y)

        unit.image.clip_draw(0, 0 * unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.IMAGE_SIZE, cx, cy)


class ComputerBase:

    def __init__(self, x, y):

        self.IMAGE_SIZE = 300
        self.PIXEL_PER_METER = (100 / 0.02)

        self.EXPLODING_TIME_PER_ACTION = 0.5
        self.EXPLODING_ACTION_PER_TIME = 1.0 / self.EXPLODING_TIME_PER_ACTION
        self.EXPLODING_FRAMES_PER_ACTION = 5

        self.event_que = []
        self.cur_state = IdleState

        self.max_hp = 2000
        self.hp = 2000
        self.temp_hp = 2000
        self.x = x
        self.y = y

        self.frame = 0
        self.init_time = 0

        self.unit_generate_time =0

        self.is_foe = True

        self.is_air_unit = False

        self.image = load_image('resource\\image\\unit\\base.png')
        self.font = load_font('ENCR10B.TTF', 16)

        self.add_self()

        self.init_time = 0
        self.cnt =0

        hp_bar = HpBar(self.x, self.y, self.max_hp, self.max_hp, self.is_foe, self)
        self.hp_bar = hp_bar
        game_world.add_object(hp_bar, 4)

    def add_self(self):
        game_world.add_object(self, 1)

        game_world.computer_all_unit.append(self)
        game_world.computer_ground_unit.append(self)


    def delete_this_unit_from_checking_layer(self):
        game_world.computer_all_unit.remove(self)
        game_world.computer_ground_unit.remove(self)
        game_world.remove_object(self.hp_bar)

    def generate_unit(self , num):
        if num == 0:
            unit_list.Ant(self.x, self.y- random.randint(0,50), self.is_foe)
        elif num ==1:
            unit_list.SpitterAnt(self.x, self.y - random.randint(0, 50), self.is_foe)
        elif num ==2:
            unit_list.Wasp(self.x, unit_functions.SKY_HEIGHT_WASP + random.randint(0,50), self.is_foe)
        elif num ==3:
            unit_list.QueenAnt(self.x, self.y - random.randint(0, 50), self.is_foe)
        elif num ==4:
            unit_list.Beetle(self.x, self.y - random.randint(0, 50), self.is_foe)
        elif num == 5:
            unit_list.BazookaBug(self.x, self.y - random.randint(0, 50), self.is_foe)
        elif num == 6:
            unit_list.BombardDragonFly(self.x, unit_functions.SKY_HEIGHT_BOMBARD + random.randint(0,50), self.is_foe)


    def get_bb(self):
        return self.x - (self.IMAGE_SIZE-80) // 2, \
               self.y - (self.IMAGE_SIZE-70) // 2, \
               self.x + (self.IMAGE_SIZE-80) // 2, \
               self.y + (self.IMAGE_SIZE-70) // 2

    def is_this_unit_dead(self):
        if self.hp <= 0:
            return True
        return False

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.unit_generate_time -= game_framework.frame_time
        if self.unit_generate_time <= 0:
            self.unit_generate_time += 3
            i = random.randint(0, 6)
            self.generate_unit(i)

        if (self.temp_hp == self.hp) is False:
            i = random.randint(0, 6)
            self.generate_unit(i)
            unit_list.Bee(self.x, unit_functions.SKY_HEIGHT + random.randint(0,50), self.is_foe)
            self.temp_hp = self.hp

        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self)
            self.cur_state = event
            self.cur_state.enter(self)

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())
