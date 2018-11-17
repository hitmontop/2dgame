from basic_air_unit import*
from projectile_bee import*

UNIT_LIST = 2


class Bee(BasicAirUnit):
    image = None

    def __init__(self, x, y, is_foe):
        self.IMAGE_SIZE = 100

        self.PIXEL_PER_METER = (100 / 0.02)
        self.RUN_SPEED_KMPH = 0.18
        self.RUN_SPEED_MPM = (self.RUN_SPEED_KMPH * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * self.PIXEL_PER_METER)

        self.RUN_TIME_PER_ACTION = 0.1
        self.RUN_ACTION_PER_TIME = 1.0 / self.RUN_TIME_PER_ACTION
        self.RUN_FRAMES_PER_ACTION = 2

        self.ATTACK_TIME_PER_ACTION = 1
        self.ATTACK_ACTION_PER_TIME = 1.0 / self.ATTACK_TIME_PER_ACTION
        self.ATTACK_FRAMES_PER_ACTION = 2

        self.DYING_TIME_PER_ACTION = 1
        self.DYING_ACTION_PER_TIME = 1.0 / self.DYING_TIME_PER_ACTION
        self.DYING_FRAMES_PER_ACTION = 1

        self.event_que = []
        self.cur_state = RunState

        self.max_hp = 80
        self.hp = 80
        self.damage = 20
        self.range = self.PIXEL_PER_METER * 0.05
        self.sight = self.PIXEL_PER_METER * 0.1
        self.velocity = self.RUN_SPEED_PPS

        self.x = x
        self.y = y
        self.target_x_temp = 0

        self.frame = 0
        self.init_time = 0

        self.target = None

        self.is_this_unit_can_attack_ground = True
        self.is_this_unit_can_attack_air = True

        self.is_air_unit = True

        self.is_foe = is_foe
        self.is_this_unit_targeting_enemy = False
        self.is_safe_to_go = False

        self.valid_target_list = []

        hp_bar = HpBar(self.x, self.y, self.max_hp, self.max_hp, self.is_foe, self)
        self.hp_bar = hp_bar
        game_world.add_object(hp_bar, 4)

        if Bee.image is None:
            self.image = load_image('resource\\image\\unit\\bee.png')

    def attack_target(self):
        projectile = ProjectileBee(self.x, self.y, self.target, self.damage)
        game_world.add_object(projectile, 4)
