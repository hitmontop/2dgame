from pico2d import*
from unit import*

class Ant(Unit):
    image = None

    def __init__(self, x, y, is_foe):
        self.event_que = []
        self.cur_state = RunState


        self.hp = 100
        self.damage = 10
        self.range = 10
        self.sight = 1000
        self.velocity = 1



        self.x = x
        self.y = y


        self.attack_frame = 3
        self.dying_frame = 1

        self.frame = 0

        self.time = 0


        self.is_foe = is_foe

        if Ant.image == None:
            Ant.image = load_image('ant.png')

        self.target = None
        self.is_melee = True
        self.is_lock_on = False

