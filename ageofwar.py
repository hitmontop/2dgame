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

    def update(self):
        if self.is_foe:
            if unit.search_for_enemy():
                if self.x - self.range > self.target.x or self.target.x > self.x + self.range:
                    self.x = self.x - self.speed
            else:
                self.x = self.x - self.speed
        else:
            if unit.search_for_enemy():
                if self.x - self.range > self.target.x or self.target.x > self.x + self.range:
                    self.x = self.x + self.speed
            else:
                self.x = self.x + self.speed


    def search_for_enemy(self):
        if self.is_foe:
            for i in player_units:
                if self.x - self.sight < i.x < self.x + self.sight:
                    self.target = i
                    return True
        else:
            for i in computer_units:
                if self.x - self.sight < i.x < self.x + self.sight:
                    self.target = i
                    return True


    def attack(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)



class ant(unit):
    def __init__(self, x, y, is_foe):
        self.hp = 100
        self.dmg = 10
        self.sight = 6000
        self.range = 10
        self.speed = 1
        self.x, self.y = x, y
        self.is_foe = is_foe

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

player_units.append(ant(200, 200, False))
computer_units.append(ant(600, 400, True))
player_units.append(ant(100, 300, False))


# game main loop
running = True
while running:
    handle_events()

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




# finalization
close_canvas()