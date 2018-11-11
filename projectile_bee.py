from projectile import*

class ProjectileBee(Projectile):
    image = None

    def __init__(self, x, y, target, damage):
        self.IMAGE_SIZE = 25

        self.PIXEL_PER_METER = (100 / 0.02)
        self.RUN_SPEED_KMPH = 0.4
        self.RUN_SPEED_MPM = (self.RUN_SPEED_KMPH * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * self.PIXEL_PER_METER)

        self.EXPLODING_TIME_PER_ACTION = 0.3
        self.EXPLODING_ACTION_PER_TIME = 1.0 / self.EXPLODING_TIME_PER_ACTION
        self.EXPLODING_FRAMES_PER_ACTION = 4

        self.i = 0
        self.target = target
        self.frame = 0
        self.init_time = 0

        self.velocity = self.RUN_SPEED_PPS
        self.x, self.y = x, y
        self.destination_x, self.destination_y = target.x, target.y

        self.damage = damage

        self.event_que = []
        self.cur_state = FlyingState

        if ProjectileBee.image is None:
            self.image = load_image('projectile_bee.png')



