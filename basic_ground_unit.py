import game_world
import game_framework

from behavior_tree import*
from hp_bar import*

UNIT_LIST = 2

RUN, CHASE, ATTACK, DEATH = 1, 2, 3, 4

class BasicGroundUnit:

    def __init__(self):

        self.IMAGE_SIZE = 0

        self.PIXEL_PER_METER = 0
        self.RUN_SPEED_KMPH = 0
        self.RUN_SPEED_MPM = (self.RUN_SPEED_KMPH * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * self.PIXEL_PER_METER)

        self.RUN_TIME_PER_ACTION = 0
        self.RUN_ACTION_PER_TIME = 0
        self.RUN_FRAMES_PER_ACTION = 0

        self.ATTACK_TIME_PER_ACTION = 0
        self.ATTACK_ACTION_PER_TIME = 0
        self.ATTACK_FRAMES_PER_ACTION = 0

        self.DYING_TIME_PER_ACTION = 0
        self.DYING_ACTION_PER_TIME = 0
        self.DYING_FRAMES_PER_ACTION = 0

        self.max_hp = 0
        self.hp = 0
        self.damage = 0
        self.range = 0
        self.sight = 0
        self.speed = 0
        self.dir = 0

        self.x = 0
        self.y = 0

        self.frame = 0
        self.init_time = 0

        self.target = None

        self.is_this_unit_can_attack_ground = False
        self.is_this_unit_can_attack_air = False
        self.is_air_unit = False
        self.is_foe = False

        self.hp_bar = None

        self.valid_target_list = []
        self.get_valid_target_list(self.is_this_unit_can_attack_air, self.is_this_unit_can_attack_ground)

        self.build_behavior_tree()
        self.add_self()

# -----------------------------------------------------------------------------------------------------------------#

    def add_self(self):
        game_world.add_object(self, 2)

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



    def is_this_unit_dead(self):
        if self.hp <= 0:
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
            game_world.remove_object(self)

        if self.x < 0 or self.x > 1200:
            self.hp = 0


# -----------------------------------------------------------------------------------------------------------------#


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
            if self.x - self.range <= o.x <= self.x + self.range:
                if o.x < min_distance:
                    min_distance = abs(self.x - o.x)
                    self.target = o
        return BehaviorTree.SUCCESS


    def get_proximate_target_with_sight(self):
        min_distance = 10000
        for o in self.valid_target_list:
            if self.x - self.sight <= o.x <= self.x + self.sight:
                if o.x < min_distance:
                    min_distance = abs(self.x - o.x)
                    self.target = o
        return BehaviorTree.SUCCESS


    def is_target_in_range(self):
        if (self.target is None) is False:
            if self.x - self.range <= self.target.x <= self.x + self.range:
                return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL


    def is_target_in_sight(self):
        if (self.target is None) is False:
            if self.x - self.sight <= self.target.x <= self.x + self.sight:
                return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL


    def is_there_any_enemy_in_range(self):
        if (self.valid_target_list is None) is False:
            for o in self.valid_target_list:
                if self.x - self.range <= o.x <= self.x + self.range:
                    return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL


    def is_there_any_enemy_in_sight(self):
        if (self.valid_target_list is None) is False:
            for o in self.valid_target_list:
                if self.x - self.sight <= o.x <= self.x + self.sight:
                    return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def is_there_no_enemy_in_sight(self):
        if (self.valid_target_list is None) is False:
            for o in self.valid_target_list:
                if self.x - self.sight <= o.x <= self.x + self.sight:
                    return BehaviorTree.FAIL
        return BehaviorTree.SUCCESS


    def attack_target(self):
        self.target.hp -= self.damage





    def run(self):
        self.cur_state = RUN
        self.speed = self.RUN_SPEED_PPS

        if self.is_foe:
            self.dir = -1

        else:
            self.dir = 1
        return BehaviorTree.SUCCESS

    def chase(self):
        self.cur_state = CHASE
        if self.target.x <= self.x:
            self.dir = -1
        else:
            self.dir = 1
        return BehaviorTree.SUCCESS

    def attack(self):
        self.attack_target()
        return BehaviorTree.SUCCESS

    def fail_node(self):
        return BehaviorTree.FAIL

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

    def update(self):
        self.is_this_unit_dead()

        self.bt.run()

        self.frame = (self.frame + self.RUN_FRAMES_PER_ACTION *
                          self.RUN_ACTION_PER_TIME * game_framework.frame_time) % self.RUN_FRAMES_PER_ACTION
        self.x += self.RUN_SPEED_PPS * self.dir * game_framework.frame_time


    def draw(self):
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * self.IMAGE_SIZE, self.IMAGE_SIZE * 4, self.IMAGE_SIZE,
                                 self.IMAGE_SIZE, self.x, self.y)
        else:
            self.image.clip_draw(int(self.frame) * self.IMAGE_SIZE, self.IMAGE_SIZE * 5, self.IMAGE_SIZE,
                                 self.IMAGE_SIZE, self.x, self.y)


# -----------------------------------------------------------------------------------------------------------------#




