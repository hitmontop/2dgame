import game_world
import game_framework

from hp_bar import*

UNIT_LIST = 2


class RunState:

    @staticmethod
    def enter(unit):
        unit.init_time = get_time()
        if unit.is_there_a_unit_searched_by_value(unit.sight):
            unit.filter_valid_target_list_with_value(unit.sight)
            unit.get_closest_target_in_list()
            unit.is_this_unit_targeting_enemy = True

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

        if (unit.target is None) or unit.target.hp <= 0:
            unit.target = None
            unit.is_this_unit_targeting_enemy = False
            unit.add_event(RunState)

        else:
            unit.target_x_temp = unit.target.x

            if unit.is_this_unit_targeting_enemy is True:
                if unit.is_target_located_inside_of_this_units_value(unit.range) is False:
                    if unit.is_there_a_unit_searched_by_value(unit.range):
                        unit.filter_valid_target_list_with_value(unit.range)
                        unit.get_closest_target_in_list()
                        unit.add_event(AttackState)
                        unit.is_safe_to_go = False

                    else:
                        if unit.is_target_located_inside_of_this_units_value(unit.sight):
                            pass

                        else:
                            unit.is_this_unit_targeting_enemy = False
                            unit.add_event(RunState)

                else:
                    unit.is_safe_to_go = False
                    unit.add_event(AttackState)

            else:
                if unit.is_target_located_inside_of_this_units_value(unit.range):
                    unit.filter_valid_target_list_with_value(unit.range)
                    unit.get_closest_target_in_list()
                    unit.is_this_unit_targeting_enemy = True
                    unit.add_event(AttackState)
                    unit.is_safe_to_go = False

                else:
                    if unit.is_target_located_inside_of_this_units_value(unit.sight):
                        unit.filter_valid_target_list_with_value(unit.sight)
                        unit.get_closest_target_in_list()
                        unit.is_this_unit_targeting_enemy = True

                    else:
                        unit.add_event(RunState)

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        if unit.is_this_unit_dead():
            unit.add_event(DyingState)

        distance = game_framework.frame_time * unit.velocity

        if unit.is_safe_to_go:
            if unit.target_x_temp > unit.x:
                unit.x += distance

            else:
                unit.x -= distance

        unit.frame = (unit.frame + unit.RUN_FRAMES_PER_ACTION * unit.RUN_ACTION_PER_TIME * game_framework.frame_time) % unit.RUN_FRAMES_PER_ACTION

        if get_time() - unit.init_time >= 0.2:
            unit.add_event(ChaseState)

    @staticmethod
    def draw(unit):

        if unit.target_x_temp > unit.x:
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
            if unit.is_target_located_inside_of_this_units_value(unit.sight):
                unit.attack_target()
            else:
                if unit.is_target_located_inside_of_this_units_value(unit.range):
                    unit.filter_valid_target_list_with_value(unit.range)
                    unit.get_closest_target_in_list()
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


class BasicGroundUnit:

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
        self.target_x_temp = 0

        self.frame = 0
        self.init_time = 0

        self.target = None

        self.is_this_unit_can_attack_ground = False
        self.is_this_unit_can_attack_air = False

        self.is_air_unit = False

        self.is_foe = False
        self.is_this_unit_targeting_enemy = False
        self.is_safe_to_go = False

        self.hp_bar = None
        self.valid_target_list = []

# -----------------------------------------------------------------------------------------------------------------#

    def get_valid_target_list(self, is_this_unit_can_attack_air, is_this_unit_can_attack_ground):
        if self.is_foe:
            if is_this_unit_can_attack_ground and is_this_unit_can_attack_air:
                self.get_all_player_unit_list()

            elif is_this_unit_can_attack_ground and is_this_unit_can_attack_air is False:
                self.get_player_ground_unit_list()

            else:
                self.get_player_air_unit_list()

        else:
            if is_this_unit_can_attack_ground and is_this_unit_can_attack_air:
                self.get_all_computer_unit_list()

            elif is_this_unit_can_attack_ground and is_this_unit_can_attack_air is False:
                self.get_computer_ground_unit_list()

            else:
                self.get_computer_air_unit_list()

    def get_all_computer_unit_list(self):
        for o in game_world.search_objects(UNIT_LIST):
            if o.is_foe:
                self.valid_target_list.append(o)

    def get_computer_ground_unit_list(self):
        for o in game_world.search_objects(UNIT_LIST):
            if o.is_foe and o.is_air_unit is False:
                self.valid_target_list.append(o)

    def get_computer_air_unit_list(self):
        for o in game_world.search_objects(UNIT_LIST):
            if o.is_foe and o.is_air_unit:
                self.valid_target_list.append(o)

    def get_all_player_unit_list(self):
        for o in game_world.search_objects(UNIT_LIST):
            if o.is_foe is False:
                self.valid_target_list.append(o)

    def get_player_ground_unit_list(self):
        for o in game_world.search_objects(UNIT_LIST):
            if o.is_foe is False and o.is_air_unit is False:
                self.valid_target_list.append(o)

    def get_player_air_unit_list(self):
        for o in game_world.search_objects(UNIT_LIST):
            if o.is_foe is False and o.is_air_unit:
                self.valid_target_list.append(o)

# -----------------------------------------------------------------------------------------------------------------#

    def is_there_a_unit_searched_by_value(self, value):
        self.reset_valid_target_list()
        self.get_valid_target_list(self.is_this_unit_can_attack_air, self.is_this_unit_can_attack_ground)

        if (self.valid_target_list is None) is False:
            for o in self.valid_target_list:
                if self.x - value <= o.x <= self.x + value:
                    return True

        return False

    def filter_valid_target_list_with_value(self, value):
        for o in self.valid_target_list:
            if self.x - value > o.x or o.x > self.x + value:
                self.valid_target_list.remove(o)

    def get_closest_target_in_list(self):
        min_distance = 10000
        for o in self.valid_target_list:
            if abs(self.x - o.x) < min_distance:
                min_distance = abs(self.x - o.x)
                self.target = o

    def is_target_located_inside_of_this_units_value(self, value):
        if self.x - value <= self.target.x <= self.x + value:
            return True
        else:
            return False

    def reset_valid_target_list(self):
        for o in self.valid_target_list:
            self.valid_target_list.remove(o)

# -----------------------------------------------------------------------------------------------------------------#

    def attack_target(self):
        self.target.hp -= self.damage

    def is_this_unit_dead(self):
        if self.hp <= 0:
            return True

        if self.x < 0 or self.x > 1200:
            self.hp = 0
            return True


        return False

# -----------------------------------------------------------------------------------------------------------------#

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






