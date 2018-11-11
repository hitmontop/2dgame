from start_button import*
from quit_button import*

import main_state

HEIGHT = 800

name = "MainState"

ui_list = []

def enter():
    start_button = StartButton(600, 500)
    ui_list.append(start_button)
    quit_button = QuitButton(600, 300)
    ui_list.append(quit_button)

def exit():
    for o in ui_list:
        game_world.remove_object(o)

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
            for o in ui_list:
                o.handle_event(event)

        elif event.type == SDL_MOUSEBUTTONUP:
            for o in ui_list:
                o.handle_event(event)



def update():
    for o in ui_list:
        o.update()


def draw():
    clear_canvas()
    for o in ui_list:
        o.draw()

    update_canvas()

