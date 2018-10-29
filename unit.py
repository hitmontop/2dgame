from pico2d import*

import main_state
import game_world

import random

computer_units_list = 2
player_units_list = 1

TIMER = range(1)
RUN, CHASE, ATTACK, DYING = range(4)




class RunState:

    # idle state ; search for units by sight while moving one's direction

    @staticmethod
    def enter(unit):
        unit.timer = 100
        if Unit.search_for_enemy_by_sight():
            Unit.add_event(ChaseState)

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):

        if unit.is_foe:
            unit.x -= unit.velocity
        else:
            unit.x += unit.velocity

        unit.timer -= 1

        unit.frame = (unit.frame + 1) % 5
        if unit.timer == 0:
            Unit.add_event(ChaseState)


    @staticmethod
    def draw(unit):
        if unit.velocity >= 0:
            unit.image.clip_draw(unit.frame * 100, 400,  100, 100, unit.x, unit.y)
        else:
            unit.image.clip_draw(unit.frame * 100, 500,  100, 100, unit.x, unit.y)




class ChaseState:

    # chase state ; found the target but target out of range.
    # when other enemy move in to one's range while chasing state, one's target change to it.

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        if unit.target.x > unit.x:
            unit.x -= unit.velocity
        else:
            unit.x += unit.velocity

        unit.timer -= 1

        unit.frame = (unit.frame + 1) % 5

        if unit.timer == 0:
            unit.add_event(ChaseState)




    @staticmethod
    def draw(unit):
        if unit.velocity >= 0:
            unit.image.clip_draw(unit.frame * 100, 400,  100, 100, unit.x, unit.y)
        else:
            unit.image.clip_draw(unit.frame * 100, 500,  100, 100, unit.x, unit.y)

    @staticmethod
    def enter(unit):
        unit.timer = 100
        if unit.search_for_enemy_by_sight():
            if unit.check_range():
                unit.add_event(AttackState)
        else:
            unit.is_lock_on = False
            unit.add_event(RunState)


class AttackState:

    # attack state ; attack when one's is_lock_on is true and one's target is in one's range

    @staticmethod
    def enter(unit):
        unit.set_frame_to_attack_frame()

    @staticmethod
    def exit(unit):
        unit.deal_damage_to_target()

    @staticmethod
    def do(unit):
        unit.frame = (unit.frame + 1) % 5
        unit.timer -= 1
        if unit.timer == 0:
            unit.add_event(ChaseState)



    @staticmethod
    def draw(unit):
        if unit.velocity >= 0:
            unit.image.clip_draw(unit.frame * 100, 200,  100, 100, unit.x, unit.y)
        else:
            unit.image.clip_draw(unit.frame * 100,300,  100, 100, unit.x, unit.y)

class DyingState:

    # dying state: print one's dying motion

    @staticmethod
    def enter(unit):
        unit.set_frame_to_dying_frame()

    @staticmethod
    def exit(unit):
        game_world.remove_object(unit)

    @staticmethod
    def do(unit):
        unit.frame = (unit.frame + 1) % 5
        unit.timer -= 1
        if unit.timer == 0:
            unit.add_event(RunState)

    @staticmethod
    def draw(unit):
        if unit.velocity >= 0:
            unit.image.clip_draw(unit.frame * 100,  0,  100, 100, unit.x, unit.y)
        else:
            unit.image.clip_draw(unit.frame * 100, 100, 100, 100, unit.x, unit.y)

next_state_table = {

    RunState: {TIMER: ChaseState},

    ChaseState: {TIMER: ChaseState},

    AttackState: {TIMER: ChaseState},

    DyingState: {TIMER: RunState}
}

class Unit:

    def __init__(self):
        self.event_que = []
        self.cur_state = RunState
        self.cur_state.enter(self, None)

        self.hp = 1
        self.damage = 1
        self.range = 1
        self.sight = 1
        self.velocity = 0


        self.x = 1
        self.y = 1




        self.attack_frame = 0
        self.dying_frame = 0

        self.frame = 0

        self.timer = 0
        self.is_foe = False
        self.target = None
        self.image = None
        self.is_melee = False
        self.is_lock_on = False


    def search_for_enemy_by_sight(self):
        min = 10000

        if self.is_foe:
            for i in game_world.search_objects(player_units_list):
                if self.x - self.sight <= i.x <= self.x + self.sight:
                    if min > i.x:
                        min = i.x
                        self.target = i
                        self.is_lock_on = True

            if self.is_lock_on:
                return True

        else:
            for i in game_world.search_objects(computer_units_list):
                if self.x - self.sight <= i.x <= self.x + self.sight:
                    if min > i.x:
                        min = i.x
                        self.target = i
                        self.is_lock_on = True

            if self.is_lock_on:
                return True


    def check_range(self):
        if self.x - self.range <= self.target.x <= self.x + self.range:
            return True


    def deal_damage_to_target(self):
        self.target.hp -= self.damage

    def set_frame_to_attack_frame(self):
        self.timer = self.attack_frame

    def set_frame_to_dying_frame(self):
        self.timer = self.dying_frame




    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = event
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)






