from indicator import PauseMark
import button
import game_framework
import game_world
import main_state
from pico2d import*

from indicator import VictoryMark
HEIGHT = 800

name = "WinState"

restart_button = None
vitory_mark = None

def enter():
    global restart_button, vitory_mark
    restart_button = button.RestartButton(main_state.canvas_width//2, main_state.canvas_height//2 - 200)
    vitory_mark = VictoryMark(main_state.canvas_width // 2, main_state.canvas_height // 2)

def exit():
    game_world.clear()

def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

        elif event.type == SDL_MOUSEMOTION:
            game_world.x, game_world.y = event.x, HEIGHT - 1 - event.y

        elif event.type == SDL_MOUSEBUTTONDOWN:
            game_world.clicked = True

        elif event.type == SDL_MOUSEBUTTONUP:
            game_world.clicked = False



def update():
    restart_button.update()
def draw():
    clear_canvas()

    for game_object in game_world.all_objects():
        game_object.draw()

    update_canvas()