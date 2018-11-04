from unit import*
from projectilespitterant import*

class SpitterAnt(Unit):
    image = None
    font = None

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

        self.DYING_TIME_PER_ACTION = 1
        self.DYING_ACTION_PER_TIME = 1.0 / self.DYING_TIME_PER_ACTION
        self.DYING_FRAMES_PER_ACTION = 2

        self.event_que = []
        self.cur_state = RunState

        self.max_hp = 80
        self.hp = 80
        self.damage = 10
        self.range = self.PIXEL_PER_METER * 0.05
        self.sight = self.PIXEL_PER_METER * 0.1
        self.velocity = self.RUN_SPEED_PPS

        self.x = x
        self.y = y

        self.frame = 0
        self.time = 0
        self.init_time = 0

        self.is_foe = is_foe
        self.is_lock_on = False
        self.target = None
        self.is_melee = True
        self.is_safe_to_go = False

        if SpitterAnt.image is None:
            self.image = load_image('spitter_ant.png')

        if SpitterAnt.font is None:
            self.font = load_font('ENCR10B.TTF', 16)

    def deal_damage_to_target(self):
        proj = ProjectileSpitterAnt(self.x, self.y, self.target)
        game_world.add_object(proj, 3)