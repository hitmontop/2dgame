from pico2d import *
import random

open_canvas()


# game object class
class unit:
    def __init__(self):
        self.hp, self.dmg, self.range, self.speed, self.x, self.y, self.acc, self.frame

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        unit.move()


    def find_enemy_unit(self):
        pass

    def move(self):
        self.x = self.x + self.speed

    def frame_update(self):
        pass

    def engage(self):
        pass

    def death(self):
        pass

class ant(unit):
    def __init__(self):
        self.hp = 100
        self.dmg = 10
        self.range = 5
        self.speed = 1
        self.x, self.y = 100, 100

        self.image = load_image('ball21X21.png')






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
enemy_units = []
frendly_units = []

frendly_units.append(ant())



# game main loop
running = True
while running:
    handle_events()

    '''for boy in team:
        boy.update()
    for ball in balls:
        ball.update()'''

    for unit in frendly_units:
        unit.update()

    clear_canvas()
    '''grass.draw()
    for boy in team:
        boy.draw()
    for ball in balls:
        ball.draw()'''

    for unit in frendly_units:
        unit.draw()

    update_canvas()

    delay(0.05)




# finalization
close_canvas()