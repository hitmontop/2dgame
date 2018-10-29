from pico2d import *
import random

open_canvas()


# game object class
class Unit:
    global cnt

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
        self.is_melee

    def update(self):
        if Unit.is_unit_out_of_screen():
            Unit.death()

        Unit.check_my_hp()

        if self.is_lock_on:
            if self.target.hp <= 0:
                self.is_lock_on = False

            if Unit.is_target_out_of_range_right() or Unit.is_target_out_of_range_left() == False:
                Unit.search_for_enemy_by_range()



        if self.is_lock_on:
            if self.x <= self.target.x:
                if Unit.is_target_out_of_range_right():
                    Unit.move_right()
                else:
                    Unit.attack(self.dmg)
            else:
                if Unit.is_target_out_of_range_left():
                    Unit.move_left()
                else:
                    Unit.attack(self.dmg)

        else:
            if Unit.search_for_enemy_by_sight():
                if self.x <= self.target.x:
                    if Unit.is_target_out_of_range_right():
                        Unit.move_right()
                    else:
                        Unit.attack(self.dmg)
                else:
                    if Unit.is_target_out_of_range_left():
                        Unit.move_left()
                    else:
                        Unit.attack(self.dmg)

            else:
                if self.is_foe:
                    Unit.move_left()
                else:
                    Unit.move_right()

    def is_unit_out_of_screen(self):
        if 0 > self.x or self.x > 800 or 0 > self.y or self.y > 600:
            return True

    def is_target_out_of_range_right(self):
        if self.x + self.range <= self.target.x:
            return True

    def is_target_out_of_range_left(self):
        if self.x - self.range >= self.target.x:
            return True

    def move_left(self):
        self.x = self.x - self.speed

    def move_right(self):
        self.x = self.x + self.speed

    def search_for_enemy_by_sight(self):
        min = 10000

        if self.is_foe:
            for i in player_units:
                if self.x - self.sight <= i.x <= self.x + self.sight:
                    if min > i.x:
                        min = i.x
                        self.target = i
                        self.is_lock_on = True

            if self.is_lock_on:
                return True

        else:
            for i in computer_units:
                if self.x - self.sight <= i.x <= self.x + self.sight:
                    if min > i.x:
                        min = i.x
                        self.target = i
                        self.is_lock_on = True

            if self.is_lock_on:
                return True

    def search_for_enemy_by_range(self):
        min= 10000
        if self.is_foe:
            for i in player_units:
                if self.x - self.range <= i.x <= self.x + self.range:
                    if min > i.x:
                        min = i.x
                        self.target = i
                        self.is_lock_on = True

            if self.is_lock_on:
                return True

        else:
            for i in computer_units:
                if self.x - self.range <= i.x <= self.x + self.range:
                    if min > i.x:
                        min = i.x
                        self.target = i
                        self.is_lock_on = True

            if self.is_lock_on:
                return True


    def attack(self, dmg):
        if self.is_melee:
            self.target.hp = self.target.hp - dmg
        else:
            if cnt % 10 == 0:
                Spitter_ant_projectile(self.x, self.y, self.target)



    def check_my_hp(self):
        if self.hp <= 0:
            Unit.death()

    def death(self):
        if self.is_foe:
            computer_units.remove(self)
        else:
            player_units.remove(self)

    def draw(self):
        self.image.draw(self.x, self.y)



class Ant(Unit):
    def __init__(self, x, y, is_foe):
        self.hp = 5000
        self.dmg = 10
        self.sight = 100
        self.range = 2
        self.speed = 1.5
        self.x, self.y = x, y

        self.is_foe = is_foe
        self.is_lock_on = False
        self.is_melee = True

        self.image = load_image('character.png')


class Spitter_ant(Unit):
    def __init__(self, x, y, is_foe):

        self.hp = 1500
        self.dmg = 1000
        self.sight = 300
        self.range = 100
        self.speed = 1.0
        self.x, self.y = x, y

        self.is_foe = is_foe
        self.is_lock_on = False
        self.is_melee = False

        self.image = load_image('ball41X41.png')



class Projectile:
    def __init__(self):
        self.speed
        self.x, self.y
        self.image
        self.target
        self.dmg
        self.destination_x, self.destination_y
        self.i = 0

    def update(self):
        self.destination_x, self.destination_y = self.target.x, self.target.y

        if self.i < 100:
            self.i = self.i + 2
            t = self.i / 100
            self.x = (1 - t) * self.x + t * self.destination_x
            self.y = (1 - t) * self.y + t * self.destination_y

        if self.i == 100:
            if self.target.hp > 0:
                self.target.hp = self.target.hp - self.dmg
            projectiles.remove(self)

    def draw(self):
        self.image.draw(self.x, self.y)




class Spitter_ant_projectile(Projectile):
    def __init__(self, x, y, target):

        self.target = target
        self.speed = 3.0
        self.i = 0
        self.dmg = 1000
        self.x, self.y = x, y
        self.destination_x, self.destination_y = self.target.x, self.target.y
        self.image = load_image('flame.png')

        projectiles.append(self)




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
projectiles = []

# game main loop

cnt = 0
running = True
while running:
    handle_events()

    if cnt % 100 == 0:
        computer_units.append(Spitter_ant(random.randint(10, 600), random.randint(200, 300), True))
    if cnt % 60 == 0:
        player_units.append(Ant(random.randint(10, 600), random.randint(200, 300), False))

    for Unit in player_units:
        Unit.update()
    for Unit in computer_units:
        Unit.update()
    for obj in projectiles:
        obj.update()

    clear_canvas()

    for Unit in player_units:
        Unit.draw()
    for Unit in computer_units:
        Unit.draw()
    for obj in projectiles:
        obj.draw()

    update_canvas()

    delay(0.01)
    cnt = cnt+1



# finalization
close_canvas()