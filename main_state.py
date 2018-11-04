from background import*
from ant import*
from spitterant import*
from base import*
import random

name = "MainState"
init_time = 0
num, num2 = 1, 1
cnt =0
background = None

def enter():
    global background, init_time

    init_time = get_time()

    background = Background()
    game_world.add_object(background, 0)

    base = Base(50, 230, False)
    game_world.add_object(base, 1)
    base = Base(1150, 230, True)
    game_world.add_object(base, 2)

def exit():
    game_world.clear()

def pause():
    pass

def resume():
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and SDLK_ESCAPE:
            game_framework.quit()
        else:
            pass


def update():
    global num, num2, init_time, cnt

    for game_object in game_world.all_objects():
        game_object.update()

    if get_time() - init_time > 0.8 and cnt <= 18:
        init_time = get_time()
        cnt += 1
        num = random.randint(0, 1)
        num2 = random.randint(0, 1)

        if num == 0:
            if num2 == 0:
                ant = Ant(random.randint(1000, 1100), random.randint(150, 200), True)
                game_world.add_object(ant, 2)
            else:
                spitter_ant = SpitterAnt(random.randint(1000, 1100), random.randint(150, 200), True)
                game_world.add_object(spitter_ant, 2)

        else:
            if num2 == 0:
                ant = Ant(random.randint(100, 200), random.randint(150, 200), False)
                game_world.add_object(ant, 1)
            else:
                spitter_ant = SpitterAnt(random.randint(100, 200), random.randint(150, 200), False)
                game_world.add_object(spitter_ant, 1)



def draw():
    clear_canvas()

    for game_object in game_world.all_objects():
        game_object.draw()

    update_canvas()
