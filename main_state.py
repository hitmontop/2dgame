from background import*
from ant import*
from spitterant import*
from base import*
import random

name = "MainState"
init_time = 0
coin_time = 0
coin = 0
num, num2 = 1, 1
cnt = 0
background = None
font = None

def enter():
    global background, init_time, coin_time, font
    font = load_font('ENCR10B.TTF', 16)
    init_time = get_time()
    coin_time = get_time()

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
    global coin
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            print("a")
            if coin >= 50:
                coin -= 50
                ant = Ant(random.randint(100, 200), random.randint(150, 200), False)
                game_world.add_object(ant, 1)

        elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
            print("s")
            if coin >= 50:
                coin -= 50
                spitter_ant = SpitterAnt(random.randint(100, 200), random.randint(150, 200), False)
                game_world.add_object(spitter_ant, 1)



def update():
    global num, num2, init_time, cnt, coin_time, coin

    for game_object in game_world.all_objects():
        game_object.update()

    if get_time() - coin_time > 0.1:
        coin_time = get_time()
        coin += 2

    if get_time() - init_time > 3:
        init_time = get_time()
        num2 = random.randint(0, 1)
        cnt += 1

        if num2 == 0:
            ant = Ant(random.randint(1000, 1100), random.randint(150, 200), True)
            game_world.add_object(ant, 2)
        else:
            spitter_ant = SpitterAnt(random.randint(1000, 1100), random.randint(150, 200), True)
            game_world.add_object(spitter_ant, 2)



def draw():
    clear_canvas()

    for game_object in game_world.all_objects():
        game_object.draw()

    font.draw(50, 80, 'money = %d' % coin, (255, 255, 0))

    update_canvas()
