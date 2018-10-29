from pico2d import*
from unit import*

class Ant(Unit):

    def __init__(self):
        self.event_que = []
        self.cur_state = RunState


        self.hp = 100
        self.damage = 10
        self.range = 2
        self.sight = 30
        self.velocity = 0.3



        self.x = 300
        self.y = 200


        self.attack_frame = 3
        self.dying_frame = 1

        self.frame = 0

        self.timer = 0

        if type == 1:
            self.is_foe = False

        else:
            self.is_foe = True

        self.target = None
        self.image = load_image('ant.png')
        self.is_melee = True
        self.is_lock_on = False