from projectile import*

class ProjectileSpitterAnt(Projectile):
    image = None

    def __init__(self, x, y, target, damage):
        self.IMAGE_SIZE = 25

        self.PIXEL_PER_METER = (100 / 0.02)
        self.RUN_SPEED_KMPH = 0.03
        self.RUN_SPEED_MPM = (self.RUN_SPEED_KMPH * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * self.PIXEL_PER_METER)

        self.EXPLODING_TIME_PER_ACTION = 0.3
        self.EXPLODING_ACTION_PER_TIME = 1.0 / self.EXPLODING_TIME_PER_ACTION
        self.EXPLODING_FRAMES_PER_ACTION = 4

        self.target = target
        self.obj_left, self.obj_bottom, self.obj_right, self.obj_top = self.target.get_bb(self)
        self.frame = 0
        self.init_time = 0


        self.x, self.y = x, y
        self.temp_x, self.temp_y = self.target.x , self.target.y
        self.dir = math.atan2(self.temp_y - self.y, self.temp_x - self.x)

        self.damage = damage

        self.event_que = []
        self.cur_state = FlyingState

        if ProjectileSpitterAnt.image is None:
            self.image = load_image('resource\\image\\projectile\\projectile_spitter_ant.png')



