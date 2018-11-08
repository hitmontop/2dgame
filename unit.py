import game_world
import game_framework

from hp_bar import*

UNIT_LIST = 2


class RunState:

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
        if unit.is_this_unit_dead():
            unit.add_event(DyingState)

        distance = game_framework.frame_time * unit.velocity

        if unit.is_foe:
            unit.x -= distance
        else:
            unit.x += distance

        unit.frame = (unit.frame + unit.RUN_FRAMES_PER_ACTION * unit.RUN_ACTION_PER_TIME * game_framework.frame_time) \
                     % unit.RUN_FRAMES_PER_ACTION

        if get_time() - unit.init_time >= 0.2:
            unit.add_event(RunState)


    @staticmethod
    def draw(unit):
        if unit.is_foe is False:
            unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 4,  unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)
        else:
            unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 5,  unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)




class ChaseState:

    @staticmethod
    def enter(unit):

        unit.init_time = get_time()
        unit.is_safe_to_go = True

        if unit.target.hp <= 0 or unit.target is None:
            unit.is_this_unit_targeting_enemy = False
            unit.search_for_enemy_by_sight_and_get_target()

        if unit.is_this_unit_targeting_enemy:
            if unit.is_the_target_located_inside_of_this_units_range():
                unit.add_event(AttackState)
                unit.is_safe_to_go = False

            elif unit.search_for_enemy_by_range_and_get_target():
                unit.add_event(AttackState)
                unit.is_safe_to_go = False

            elif unit.is_the_target_located_inside_of_this_units_sight():
                pass

            else:
                unit.is_this_unit_targeting_enemy = False
                unit.add_event(RunState)
        else:
            unit.is_this_unit_targeting_enemy = False
            unit.add_event(RunState)

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        if unit.is_this_unit_dead():
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

        if unit.target.x > unit.x:
            unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 4,  unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)
        else:
            unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 5,  unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)




class AttackState:

    @staticmethod
    def enter(unit):
        unit.init_time = get_time()

    @staticmethod
    def exit(unit):
        if unit.is_this_unit_dead() is False:
            unit.attack_target()

    @staticmethod
    def do(unit):

        if unit.is_this_unit_dead():
            unit.add_event(DyingState)

        unit.frame = (unit.frame + unit.ATTACK_FRAMES_PER_ACTION *
                      unit.ATTACK_ACTION_PER_TIME * game_framework.frame_time) % unit.ATTACK_FRAMES_PER_ACTION

        if get_time() - unit.init_time >= unit.ATTACK_TIME_PER_ACTION:
            unit.add_event(ChaseState)



    @staticmethod
    def draw(unit):
        if unit.target.x > unit.x:
            unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 2,  unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)
        else:
            unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 3,  unit.IMAGE_SIZE, unit.IMAGE_SIZE, unit.x, unit.y)

class DyingState:

    @staticmethod
    def enter(unit):
        game_world.pull_object(unit)
        game_world.add_object(unit, 1)
        unit.init_time = get_time()
        game_world.remove_object(unit.hp_bar)


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

        self.target = None

        self.is_foe = False
        self.is_this_unit_targeting_enemy = False
        self.is_safe_to_go = False

        self.hp_bar = None


########################################################################################################################

    def search_for_enemy_by_sight_and_get_target(self):
        if self.is_foe:
            return self.search_for_closest_target_and_get_target_with_value(self.sight, self.is_foe)

        else:
            return self.search_for_closest_target_and_get_target_with_value(self.sight, self.is_foe)

    def search_for_enemy_by_range_and_get_target(self):
        if self.is_foe:
            return self.search_for_closest_target_and_get_target_with_value(self.range, self.is_foe)

        else:
            return self.search_for_closest_target_and_get_target_with_value(self.range, self.is_foe)

    def search_for_closest_target_and_get_target_with_value(self, value, is_foe):
        min_distance_between_this_unit_and_target = 10000
        if is_foe:
            for subject in game_world.search_objects(UNIT_LIST):
                if subject.is_foe is False:
                    if self.x - value <= subject.x <= self.x + value:
                        if min_distance_between_this_unit_and_target > subject.x:
                            min_distance_between_this_unit_and_target = subject.x
                            self.target = subject

        else:
            for subject in game_world.search_objects(UNIT_LIST):
                if subject.is_foe:
                    if self.x - value <= subject.x <= self.x + value:
                        if min_distance_between_this_unit_and_target > subject.x:
                            min_distance_between_this_unit_and_target = subject.x
                            self.target = subject

        if (min_distance_between_this_unit_and_target == 10000) is False:
            self.is_this_unit_targeting_enemy = True
            return True

    def is_the_target_located_inside_of_this_units_range(self):
        if self.x - self.range <= self.target.x <= self.x + self.range:
            return True

    def is_the_target_located_inside_of_this_units_sight(self):
        if self.x - self.sight <= self.target.x <= self.x + self.sight:
            return True

    def attack_target(self):
        self.target.hp -= self.damage

    def is_this_unit_dead(self):
        if self.hp <= 0 or self.x < -100 or self.x > 1300:
            return True
        else:
            return False

########################################################################################################################

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






