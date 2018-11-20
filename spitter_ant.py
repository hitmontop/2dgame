from basic_ground_unit import*
from projectile_spitterant import*

class SpitterAnt(BasicGroundUnit):
    image = None

    def __init__(self, x, y, is_foe):
        self.IMAGE_SIZE = 100

        self.PIXEL_PER_METER = (100 / 0.02)
        self.RUN_SPEED_KMPH = 0.05
        self.RUN_SPEED_MPM = (self.RUN_SPEED_KMPH * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * self.PIXEL_PER_METER)

        self.RUN_TIME_PER_ACTION = 0.5
        self.RUN_ACTION_PER_TIME = 1.0 / self.RUN_TIME_PER_ACTION
        self.RUN_FRAMES_PER_ACTION = 6

        self.ATTACK_TIME_PER_ACTION = 1
        self.ATTACK_ACTION_PER_TIME = 1.0 / self.ATTACK_TIME_PER_ACTION
        self.ATTACK_FRAMES_PER_ACTION = 3
        self.attack_init_time = 0

        self.DYING_TIME_PER_ACTION = 4
        self.DYING_ACTION_PER_TIME = 1.0 / self.DYING_TIME_PER_ACTION
        self.DYING_FRAMES_PER_ACTION = 2
        self.dying_init_time = 0

        self.max_hp = 80
        self.hp = 80
        self.damage = 20
        self.range = self.PIXEL_PER_METER * 0.03
        self.sight = self.PIXEL_PER_METER * 0.07
        self.speed = 0
        self.dir = 0

        self.x = x
        self.y = y
        self.target_x_temp = 0

        self.frame = 0
        self.time = 0
        self.init_time = 0

        self.target = None

        self.is_this_unit_can_attack_ground = True
        self.is_this_unit_can_attack_air = True

        self.is_air_unit = False

        self.is_foe = is_foe

        self.valid_target_list = []
        self.get_valid_target_list(self.is_this_unit_can_attack_air, self.is_this_unit_can_attack_ground)

        self.build_behavior_tree()

        hp_bar = HpBar(self.x, self.y, self.max_hp, self.max_hp, self.is_foe, self)
        self.hp_bar = hp_bar
        game_world.add_object(hp_bar, 4)

        if SpitterAnt.image is None:
            self.image = load_image('resource\\image\\unit\\spitter_ant.png')

        self.add_self()

        self.event_que = []
        self.cur_state = RunState

        if self.is_foe:
            self.dir = -1
        else:
            self.dir = 1

    def attack_target(self):
        projectile = ProjectileSpitterAnt(self.x, self.y, self.target, self.damage)
        game_world.add_object(projectile, 4)