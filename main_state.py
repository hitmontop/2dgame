from pico2d import*
import game_framework
import game_world

from background import*
from ant import*

name = "MainState"

background = None

def enter():
    global background
    background = Background()
    ant = Ant()


    game_world.add_object(background, 0)
    game_world.add_object(ant, 1)

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
    for game_object in game_world.all_objects():
        game_object.update()

def draw():
    clear_canvas()

    for game_object in game_world.all_objects():
        game_object.draw()

    update_canvas()
