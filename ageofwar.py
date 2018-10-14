from pico2d import *
import random

open_canvas()


# game object class
class unit:
    def __init__(self):
        self.hp
        self.dmg
        self.range
        self.speed
        self.x
        self.y
        self.sight
        self.is_foe
        self.target
        self.image
        self.is_lock_on = False

    def update(self):
        if 0 > self.x or self.x > 800 or 0 > self.y or self.y > 600:
            self.hp=0

        unit.check_my_hp()

        if self.is_lock_on:
            if self.x < self.target.x:
                if self.x + self.range < self.target.x:
                    self.x = self.x + self.speed
                else:
                    unit.attack(self.dmg)
            else:
                if self.x - self.range > self.target.x:
                    self.x = self.x - self.speed
                else:
                    unit.attack(self.dmg)

        else:
            if unit.search_for_enemy():
                if self.x < self.target.x:
                    if self.x - self.range < self.target.x:
                        self.x = self.x + self.speed
                    else:
                        unit.attack(self.dmg)
                else:
                    if self.x - self.range > self.target.x:
                        self.x = self.x - self.speed
                    else:
                        unit.attack(self.dmg)
            else:

                if self.is_foe:
                    self.x = self.x - self.speed
                    self.y = self.y + 0.5
                else:
                    self.x = self.x + self.speed
                    self.y = self.y + 0.5




    def search_for_enemy(self):
        min= 10000

        if self.is_foe:
            for i in player_units:
                if self.x - self.sight < i.x < self.x + self.sight:
                    if min > i.x:
                        min = i.x
                        self.target = i
                        self.is_lock_on = True

            if self.is_lock_on:
                return True

        else:
            for i in computer_units:
                if self.x - self.sight < i.x < self.x + self.sight:
                    if min > i.x:
                        min = i.x
                        self.target = i
                        self.is_lock_on = True

            if self.is_lock_on:
                return True


    def attack(self, dmg):
        self.target.hp = self.target.hp - dmg
        if self.target.hp <= 0:
            self.is_lock_on = False


    def check_my_hp(self):
        if self.hp <= 0:
            unit.death()

    def death(self):
        if self.is_foe:
            computer_units.remove(self)
        else:
            player_units.remove(self)


    def draw(self):
        self.image.draw(self.x, self.y)



class ant(unit):
    def __init__(self, x, y, is_foe):
        self.hp = 1500
        self.dmg = 10
        self.sight = 100
        self.range = 50
        self.speed = 3.0
        self.x, self.y = x, y
        self.is_foe = is_foe
        self.is_lock_on = False

        if self.is_foe:
            self.image = load_image('ball21X21.png')
        else:
            self.image = load_image('ball41X41.png')


'''
class Boy:
    def __init__(self):
        self.x, self.y = random.randint(100, 700), 90
        self.frame = random.randint(0, 7)
        self.image = load_image('run_animation.png')

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += 5

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
'''

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False



# initialization code
player_units = []
computer_units = []


# game main loop

cnt=0
running = True
while running:
    handle_events()

    if cnt % 50 == 0:
        computer_units.append(ant(random.randint(10,600), random.randint(200,300), True))
        player_units.append(ant(random.randint(10,600), random.randint(200,300), False))

    for unit in player_units:
        unit.update()
    for unit in computer_units:
        unit.update()
    clear_canvas()

    for unit in player_units:
        unit.draw()
    for unit in computer_units:
        unit.draw()

    update_canvas()

    delay(0.01)
    cnt = cnt+1



# finalization
close_canvas()