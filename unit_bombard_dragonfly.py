import game_world
import game_framework
import unit_functions
from behavior_tree import*
from hp_bar import*
import particle

import unit_bomb_projectile

UNIT_LIST = 2


class RunState:

    @staticmethod
    def enter(unit):
        unit.speed = unit.RUN_SPEED_PPS

        if unit.is_foe:
            unit.dir = -1

        else:
            unit.dir = 1

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):

        unit.frame = (unit.frame + unit.RUN_FRAMES_PER_ACTION *
                      unit.RUN_ACTION_PER_TIME * game_framework.frame_time) % unit.RUN_FRAMES_PER_ACTION
        unit.x += unit.RUN_SPEED_PPS * unit.dir * game_framework.frame_time


    @staticmethod
    def draw(unit):
        cx, cy = unit_functions.get_cx_cy(unit.x, unit.y)

        if unit.is_attacked:
            if unit.dir == 1:
                unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 2, unit.IMAGE_SIZE,
                                 unit.IMAGE_SIZE, cx, cy)
            else:
                unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 3, unit.IMAGE_SIZE,
                                 unit.IMAGE_SIZE, cx, cy)

        else:
            if unit.dir == 1:
                unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 4, unit.IMAGE_SIZE,
                                 unit.IMAGE_SIZE, cx, cy)
            else:
                unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 5, unit.IMAGE_SIZE,
                                 unit.IMAGE_SIZE, cx, cy)



class ChaseState:

    @staticmethod
    def enter(unit):
        if unit.target.x <= unit.x:
            unit.dir = -1
        else:
            unit.dir = 1

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        if (unit.target is None) is False:
            unit.temp_x, unit.temp_y = unit.target.x, unit.target.y

        if (unit.target is None) is False:
            if unit.target.x <= unit.x:
                unit.dir = -1
            else:
                unit.dir = 1

        unit.frame = (unit.frame + unit.RUN_FRAMES_PER_ACTION *
                      unit.RUN_ACTION_PER_TIME * game_framework.frame_time) % unit.RUN_FRAMES_PER_ACTION

        unit.x += unit.RUN_SPEED_PPS * unit.dir * game_framework.frame_time

    @staticmethod
    def draw(unit):
        cx, cy = unit_functions.get_cx_cy(unit.x, unit.y)

        if unit.is_attacked:
            if unit.dir == 1:
                unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 2, unit.IMAGE_SIZE,
                                 unit.IMAGE_SIZE, cx, cy)
            else:
                unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 3, unit.IMAGE_SIZE,
                                 unit.IMAGE_SIZE, cx, cy)

        else:
            if unit.dir == 1:
                unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 4, unit.IMAGE_SIZE,
                                 unit.IMAGE_SIZE, cx, cy)
            else:
                unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 5, unit.IMAGE_SIZE,
                                 unit.IMAGE_SIZE, cx, cy)



class AttackState:

    @staticmethod
    def enter(unit):
        unit.frame = 0

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):

        unit.attack_target()

        if (unit.target is None) is False:
            if unit.target.x <= unit.x:
                unit.dir = -1
            else:
                unit.dir = 1

        unit.frame = (unit.frame + unit.ATTACK_FRAMES_PER_ACTION *
                      unit.ATTACK_ACTION_PER_TIME * game_framework.frame_time) % unit.ATTACK_FRAMES_PER_ACTION

    @staticmethod
    def draw(unit):
        cx, cy = unit_functions.get_cx_cy(unit.x, unit.y)

        if unit.is_attacked:
            if unit.dir == 1:
                unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 2, unit.IMAGE_SIZE,
                                 unit.IMAGE_SIZE, cx, cy)
            else:
                unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 3, unit.IMAGE_SIZE,
                                 unit.IMAGE_SIZE, cx, cy)

        else:
            if unit.dir == 1:
                unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 4, unit.IMAGE_SIZE,
                                 unit.IMAGE_SIZE, cx, cy)
            else:
                unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 5, unit.IMAGE_SIZE,
                                 unit.IMAGE_SIZE, cx, cy)

class DyingState:

    @staticmethod
    def enter(unit):


        unit.frame = 0
        unit.delete_this_unit_from_checking_layer()

        game_world.add_object(unit, 1)
        game_world.pull_object(unit)

        unit.dying_init_time = unit.DYING_TIME_PER_ACTION

    @staticmethod
    def exit(unit):
        game_world.remove_object(unit)

    @staticmethod
    def do(unit):
        unit.dying_init_time -= game_framework.frame_time
        if unit.dying_init_time <= 0:
            unit.dying_init_time += unit.DYING_TIME_PER_ACTION
            unit.add_event(RunState)

        if unit.is_air_unit:
            if unit.y > unit_functions.GROUND_HEIGHT_FOR_AIR_UNITS:
                unit.y -= unit.acc * game_framework.frame_time
                unit.acc += 5

        unit.frame = (unit.frame + unit.DYING_FRAMES_PER_ACTION *
                    unit.DYING_ACTION_PER_TIME * game_framework.frame_time) % unit.DYING_FRAMES_PER_ACTION

    @staticmethod
    def draw(unit):
        cx, cy = unit_functions.get_cx_cy(unit.x, unit.y)

        if unit.dir == 1:
            unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 0, unit.IMAGE_SIZE,
                                 unit.IMAGE_SIZE, cx, cy)
        else:
            unit.image.clip_draw(int(unit.frame) * unit.IMAGE_SIZE, unit.IMAGE_SIZE * 1, unit.IMAGE_SIZE,
                                 unit.IMAGE_SIZE, cx, cy)


class BombardDragonFly:
    image = None
    cost = 40
    BUILD_TIME = 5
    def __init__(self, x, y, is_foe):
        self.IMAGE_SIZE = 200

        self.PIXEL_PER_METER = (100 / 0.02)
        self.RUN_SPEED_KMPH = 0.2
        self.RUN_SPEED_MPM = (self.RUN_SPEED_KMPH * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * self.PIXEL_PER_METER)

        self.RUN_TIME_PER_ACTION = 0.05
        self.RUN_ACTION_PER_TIME = 1.0 / self.RUN_TIME_PER_ACTION
        self.RUN_FRAMES_PER_ACTION = 2

        self.ATTACK_TIME_PER_ACTION = 0.01
        self.ATTACK_ACTION_PER_TIME = 1.0 / self.ATTACK_TIME_PER_ACTION
        self.ATTACK_FRAMES_PER_ACTION = 2
        self.attack_init_time = 0

        self.DYING_TIME_PER_ACTION = 3
        self.DYING_ACTION_PER_TIME = 1.0 / self.DYING_TIME_PER_ACTION
        self.DYING_FRAMES_PER_ACTION = 1
        self.dying_init_time = 0

        self.max_hp = 200
        self.hp = 200
        self.damage = 100
        self.range = self.PIXEL_PER_METER * 0.01
        self.sight = self.PIXEL_PER_METER * 0.01
        self.speed = 0
        self.dir = 0

        self.temp_x, self.temp_y = 0, 0
        self.x = x
        self.y = y
        self.target_x_temp = 0

        self.flying_sound = load_wav('resource\\sound\\helicopter.wav')
        self.flying_sound.set_volume(10)

        self.frame = 0
        self.time = 0
        self.init_time = 0
        self.smoke_time =0
        self.acc = 0

        self.target = None

        self.is_this_unit_can_attack_ground = True
        self.is_this_unit_can_attack_air = False

        self.is_air_unit = True

        self.is_attacked = False

        self.is_foe = is_foe

        self.valid_target_list = []
        self.get_valid_target_list(self.is_this_unit_can_attack_air, self.is_this_unit_can_attack_ground)

        self.build_behavior_tree()

        hp_bar = HpBar(self.x, self.y, self.max_hp, self.max_hp, self.is_foe, self)
        self.hp_bar = hp_bar
        game_world.add_object(hp_bar, 4)

        if BombardDragonFly.image is None:
            BombardDragonFly.image = load_image('resource\\image\\unit\\dragon.png')

        self.add_self()

        self.event_que = []
        self.cur_state = RunState

        if self.is_foe:
            self.dir = -1
        else:
            self.dir = 1

        self.flying_sound.play()


# -----------------------------------------------------------------------------------------------------------------#

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


    def get_valid_target_list(self, is_this_unit_can_attack_air, is_this_unit_can_attack_ground):
        if self.is_foe:
            if is_this_unit_can_attack_ground and is_this_unit_can_attack_air:
                self.valid_target_list = game_world.player_all_unit

            elif is_this_unit_can_attack_ground and is_this_unit_can_attack_air is False:
                self.valid_target_list = game_world.player_ground_unit

            else:
                self.valid_target_list = game_world.player_air_unit

        else:
            if is_this_unit_can_attack_ground and is_this_unit_can_attack_air:
                self.valid_target_list = game_world.computer_all_unit

            elif is_this_unit_can_attack_ground and is_this_unit_can_attack_air is False:
                self.valid_target_list = game_world.computer_ground_unit

            else:
                self.valid_target_list = game_world.computer_air_unit

# -----------------------------------------------------------------------------------------------------------------#

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


    def is_target_live(self):
        if self.target is None:
            self.target = None
        elif self.target.hp <= 0:
            self.target = None
        return BehaviorTree.FAIL


    def is_target_empty(self):
        if self.target is None:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL


    def empty_target(self):
        self.target = None
        return BehaviorTree.SUCCESS


    def get_proximate_target_with_range(self):
        min_distance = 10000
        for o in self.valid_target_list:
            if self.collide(o):
                if abs(self.x - o.x) < min_distance:
                    min_distance = abs(self.x - o.x)
                    self.target = o
        return BehaviorTree.SUCCESS


    def get_proximate_target_with_sight(self):
        min_distance = 10000
        for o in self.valid_target_list:
            if abs(self.x - o.x) < min_distance:
                min_distance = abs(self.x - o.x)
                self.target = o
        return BehaviorTree.SUCCESS


    def is_target_in_range(self):
        if (self.target is None) is False:
            if self.collide(self.target):
                return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL


    def is_target_in_sight(self):
        if (self.target is None) is False:
            if self.collide_sight(self.target):
                return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL


    def is_there_any_enemy_in_range(self):
        if (self.valid_target_list is None) is False:
            for o in self.valid_target_list:
                if self.collide(o):
                    return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL


    def is_there_any_enemy_in_sight(self):
        if (self.valid_target_list is None) is False:
            for o in self.valid_target_list:
                if self.collide_sight(o):
                    return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def is_there_no_enemy_in_sight(self):
        if (self.valid_target_list is None) is False:
            for o in self.valid_target_list:
                if self.collide_sight(o):
                    return BehaviorTree.FAIL
        return BehaviorTree.SUCCESS


    def attack_target(self):
        if (self.target is None) is False:
            self.is_attacked = True
            missile = unit_bomb_projectile.ProjectileBomBardDragonFly(self.x, self.y, self.target, self.valid_target_list, self.damage)
            self.add_event(RunState)



    def run(self):
        if (self.cur_state is RunState) is False:
            self.add_event(RunState)

        return BehaviorTree.SUCCESS

    def chase(self):
        if (self.cur_state is ChaseState) is False and self.is_attacked is False:
            self.add_event(ChaseState)
        return BehaviorTree.SUCCESS

    def attack(self):
        if (self.cur_state is AttackState) is False and self.is_attacked is False:
            self.add_event(AttackState)
        return BehaviorTree.SUCCESS

    def fail_node(self):
        return BehaviorTree.FAIL


    def get_bb(self):
        return self.x - (self.IMAGE_SIZE-25) // 2, \
               self.y - (self.IMAGE_SIZE-50) // 2, \
               self.x + (self.IMAGE_SIZE-25) // 2, \
               self.y + (self.IMAGE_SIZE-50) // 2

    def collide_sight(self, o):
        left, bottom, right, top = o.get_bb()
        if self.x + self.sight < left: return False
        if self.x - self.sight > right: return False
        return True

    def collide(self, o):
        left, bottom, right, top = o.get_bb()
        if self.x + self.range < left: return False
        if self.x - self.range > right: return False
        return True

# -----------------------------------------------------------------------------------------------------------------#

    def build_behavior_tree(self):

        is_target_live_node = LeafNode("is_target_live", self.is_target_live)
        is_target_empty_node = LeafNode("is_target_empty", self.is_target_empty)
        empty_target_node = LeafNode("empty_target", self.empty_target)

        get_proximate_target_with_range_node = LeafNode("get_proximate_target_with_range",
                                                   self.get_proximate_target_with_range)
        get_proximate_target_with_sight_node = LeafNode("get_proximate_target_with_sight",
                                                   self.get_proximate_target_with_sight)

        is_target_in_range_node = LeafNode("is_target_in_range", self.is_target_in_range)
        is_target_in_sight_node = LeafNode("is_target_in_sight", self.is_target_in_sight)

        is_there_any_enemy_in_range_node = LeafNode("is_there_any_enemy_in_range", self.is_there_any_enemy_in_range)
        is_there_any_enemy_in_sight_node = LeafNode("is_there_any_enemy_in_sight", self.is_there_any_enemy_in_sight)

        is_there_no_enemy_in_sight_node = LeafNode("is_there_no_enemy_in_sight", self.is_there_no_enemy_in_sight)

        attack_node = LeafNode("attack", self.attack)
        run_node = LeafNode("run", self.run)
        chase_node = LeafNode("chase", self.chase)

        fail_node = LeafNode("fail_node", self.fail_node)


        check_target_is_empty_and_run_node = SequenceNode("check_target_is_empty_and_run")
        check_target_is_empty_and_run_node.add_children(empty_target_node, run_node)

        find_enemy_with_sight_and_chase_node = SequenceNode("find_enemy_with_sight_and_chase")
        find_enemy_with_sight_and_chase_node.add_children(is_there_any_enemy_in_sight_node, get_proximate_target_with_sight_node, chase_node)

        check_target_in_sight_and_chase_node = SequenceNode("check_target_in_sight_and_chase")
        check_target_in_sight_and_chase_node.add_children(is_target_in_sight_node, chase_node)

        find_enemy_with_range_and_attack_node = SequenceNode("find_enemy_with_range_and_attack")
        find_enemy_with_range_and_attack_node.add_children(is_there_any_enemy_in_range_node, get_proximate_target_with_range_node, attack_node)

        check_target_in_range_and_attack_node = SequenceNode("check_target_in_range_and_attack")
        check_target_in_range_and_attack_node.add_children(is_target_in_range_node, attack_node)

        attack_chase_run_node = SelectorNode("attack_chase_run")
        attack_chase_run_node.add_children(check_target_in_range_and_attack_node, find_enemy_with_range_and_attack_node,
                                           check_target_in_sight_and_chase_node, find_enemy_with_sight_and_chase_node,
                                           check_target_is_empty_and_run_node)




        check_target_is_empty_and_find_target_with_sight_node = SequenceNode("check_target_is_empty_and_find_target_with_sight")
        check_target_is_empty_and_find_target_with_sight_node.add_children(is_target_empty_node, get_proximate_target_with_sight_node,
                                                                           fail_node)

        find_enemy_with_sight_and_run_node = SequenceNode("find_enemy_with_sight_and_run")
        find_enemy_with_sight_and_run_node.add_children(is_target_empty_node, is_there_no_enemy_in_sight_node, run_node)

        run_get_do_node = SelectorNode("run_get_do")
        run_get_do_node.add_children(find_enemy_with_sight_and_run_node, find_enemy_with_sight_and_run_node, attack_chase_run_node)





        basic_ai_node = SelectorNode("basic_ai")
        basic_ai_node.add_children(is_target_live_node, run_get_do_node)


        self.bt = BehaviorTree(basic_ai_node)


# -----------------------------------------------------------------------------------------------------------------#

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        if unit_functions.is_this_unit_dead(self):
            if (self.cur_state is DyingState) is False:
                self.add_event(DyingState)

        else:
            self.init_time -= game_framework.frame_time
            if self.init_time <= 0:
                self.bt.run()
                self.init_time += 0.1
                smoke = particle.Smoke(self.x, self.y)

        self.smoke_time -= game_framework.frame_time
        if self.smoke_time <= 0:
            smoke = particle.Smoke(self.x, self.y)
            self.smoke_time += 0.1

        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self)
            self.cur_state = event
            self.cur_state.enter(self)

    def draw(self):
        self.cur_state.draw(self)
# -----------------------------------------------------------------------------------------------------------------#
