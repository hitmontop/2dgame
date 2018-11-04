from pico2d import*

import game_world
import game_framework

computer_units_list = 2
player_units_list = 1

TIMER = range(1)
RUN, CHASE, ATTACK, DYING = range(4)


class RunState:

    # idle state ; search for units by sight while moving one's direction

    @staticmethod
    def enter(unit):
        unit.init_time = get_time()
        if unit.search_for_enemy_by_sight_and_get_target():
            unit.add_event(ChaseState)

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        if unit.check_my_hp():
            unit.add_event(DyingState)

        distance = game_framework.frame_time * unit.velocity

        if unit.is_foe:
            unit.x -= distance
        else:
            unit.x += distance

        unit.frame = (unit.frame + unit.RUN_FRAMES_PER_ACTION * unit.RUN_ACTION_PER_TIME * game_framework.frame_time) \
                     % unit.RUN_FRAMES_PER_ACTION

        if get_time() - unit.init_time >= 0.5:
            unit.add_event(RunState)


    @staticmethod
    def draw(unit):

        if unit.is_foe is False:
            unit.font.draw(unit.x - 60, unit.y + 50, '(%d/' % unit.hp, (100, 255, 0))
            unit.font.draw(unit.x - 10, unit.y + 50, '%d)' % unit.max_hp, (100, 255, 0))
        else:
            unit.font.draw(unit.x - 60, unit.y + 50, '(%d/' % unit.hp, (255, 0, 0))
            unit.font.draw(unit.x - 10, unit.y + 50, '%d)' % unit.max_hp, (255, 0, 0))

        if unit.is_foe is False:
            unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 4,  unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)
        else:
            unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 5,  unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)




class ChaseState:

    # chase state ; found the target but target out of range.
    # when other enemy move in to one's range while chasing state, one's target change to it.

    @staticmethod
    def enter(unit):

        unit.init_time = get_time()
        unit.is_safe_to_go = True

        if unit.target.hp <= 0 or unit.target is None:
            unit.is_lock_on = False
            unit.search_for_enemy_by_sight_and_get_target()

        if unit.is_lock_on:
            if unit.check_range():
                unit.add_event(AttackState)
                unit.is_safe_to_go = False

            elif unit.search_for_enemy_by_range_and_get_target():
                unit.add_event(AttackState)
                unit.is_safe_to_go = False

            elif unit.check_sight():
                pass

            else:
                unit.is_lock_on = False
                unit.add_event(RunState)
        else:
            unit.is_lock_on = False
            unit.add_event(RunState)

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        if unit.check_my_hp():
            unit.add_event(DyingState)

        if unit.is_safe_to_go:
            distance = game_framework.frame_time * unit.velocity

            if unit.target.x > unit.x:
                unit.x += distance
            else:
                unit.x -= distance

            unit.frame = (unit.frame + unit.RUN_FRAMES_PER_ACTION * unit.RUN_ACTION_PER_TIME * game_framework.frame_time) % unit.RUN_FRAMES_PER_ACTION

            if get_time() - unit.init_time >= 0.5:
                unit.add_event(ChaseState)



    @staticmethod
    def draw(unit):

        if unit.is_foe is False:
            unit.font.draw(unit.x - 60, unit.y + 50, '(%d/' % unit.hp, (100, 255, 0))
            unit.font.draw(unit.x - 10, unit.y + 50, '%d)' % unit.max_hp, (100, 255, 0))
        else:
            unit.font.draw(unit.x - 60, unit.y + 50, '(%d/' % unit.hp, (255, 0, 0))
            unit.font.draw(unit.x - 10, unit.y + 50, '%d)' % unit.max_hp, (255, 0, 0))

        if unit.target.x > unit.x:
            unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 4,  unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)
        else:
            unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 5,  unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)




class AttackState:
    # attack state ; attack when one's is_lock_on is true and one's target is in one's range

    @staticmethod
    def enter(unit):
        unit.init_time = get_time()

    @staticmethod
    def exit(unit):
        unit.deal_damage_to_target()

    @staticmethod
    def do(unit):

        if unit.check_my_hp():
            unit.add_event(DyingState)

        unit.frame = (unit.frame + unit.ATTACK_FRAMES_PER_ACTION *
                      unit.ATTACK_ACTION_PER_TIME * game_framework.frame_time) % unit.ATTACK_FRAMES_PER_ACTION

        if get_time() - unit.init_time >= unit.ATTACK_TIME_PER_ACTION:
            unit.add_event(ChaseState)



    @staticmethod
    def draw(unit):

        if unit.is_foe is False:
            unit.font.draw(unit.x - 60, unit.y + 50, '(%d/' % unit.hp, (100, 255, 0))
            unit.font.draw(unit.x - 10, unit.y + 50, '%d)' % unit.max_hp, (100, 255, 0))
        else:
            unit.font.draw(unit.x - 60, unit.y + 50, '(%d/' % unit.hp, (255, 0, 0))
            unit.font.draw(unit.x - 10, unit.y + 50, '%d)' % unit.max_hp, (255, 0, 0))

        if unit.target.x > unit.x:
            unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 2,  unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)
        else:
            unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 3,  unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)

class DyingState:
    # dying state: print one's dying motion

    @staticmethod
    def enter(unit):
        unit.init_time = get_time()


    @staticmethod
    def exit(unit):
        game_world.remove_object(unit)

    @staticmethod
    def do(unit):

        unit.frame = (unit.frame + unit.DYING_FRAMES_PER_ACTION *
                      unit.DYING_ACTION_PER_TIME * game_framework.frame_time) % unit.DYING_FRAMES_PER_ACTION

        if get_time() - unit.init_time >= unit.DYING_TIME_PER_ACTION:
            unit.add_event(RunState)



    @staticmethod
    def draw(unit):
        if unit.velocity >= 0:
            unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE,  0,  unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)
        else:
            unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 1, unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)

next_state_table = {
    RunState: {TIMER: RunState},
    ChaseState: {TIMER: ChaseState},
    AttackState: {TIMER: ChaseState},
    DyingState: {TIMER: RunState}
}

class Unit:

    def __init__(self):

        self.IMAGE_SIZE = 0

        self.RUN_TIME_PER_ACTION = 0
        self.RUN_ACTION_PER_TIME = 0
        self.RUN_FRAMES_PER_ACTION = 0

        self.ATTACK_TIME_PER_ACTION = 0
        self.ATTACK_ACTION_PER_TIME = 0
        self.ATTACK_FRAMES_PER_ACTION = 0

        self.DYING_TIME_PER_ACTION = 0
        self.DYING_ACTION_PER_TIME = 0
        self.DYING_FRAMES_PER_ACTION = 0

        self.event_que = []
        self.cur_state = RunState

        self.max_hp = 0
        self.hp = 0
        self.damage = 0
        self.range = 0
        self.sight = 0
        self.velocity = 0

        self.x = 0
        self.y = 0

        self.frame = 0
        self.init_time = 0


        self.is_foe = False
        self.is_lock_on = False
        self.target = None
        self.is_melee = True
        self.is_safe_to_go = False

    ###############################################

    def search_for_enemy_by_sight_and_get_target(self):
        min = 10000

        if self.is_foe:
            for i in game_world.search_objects(player_units_list):
                if self.x - self.sight <= i.x <= self.x + self.sight:
                    if min > i.x:
                        min = i.x
                        self.target = i

        else:
            for i in game_world.search_objects(computer_units_list):
                if self.x - self.sight <= i.x <= self.x + self.sight:
                    if min > i.x:
                        min = i.x
                        self.target = i

        if (min == 10000) is False:
            self.is_lock_on = True
            return True

    def search_for_enemy_by_range_and_get_target(self):
        min = 10000

        if self.is_foe:
            for i in game_world.search_objects(player_units_list):
                if self.x - self.range <= i.x <= self.x + self.range:
                    if min > i.x:
                        min = i.x
                        self.target = i

        else:
            for i in game_world.search_objects(computer_units_list):
                if self.x - self.range <= i.x <= self.x + self.range:
                    if min > i.x:
                        min = i.x
                        self.target = i

        if (min == 10000) is False:
            return True

    def check_range(self):
        if self.x - self.range <= self.target.x <= self.x + self.range:
            return True

    def check_sight(self):
        if self.x - self.sight <= self.target.x <= self.x + self.sight:
            return True

    def deal_damage_to_target(self):
        self.target.hp -= self.damage

    def check_my_hp(self):
        if self.hp <= 0:
            return True

    ###############################################

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






