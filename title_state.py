from button import*
import main_state
from background import Background

HEIGHT = 800

name = "MainState"

def enter():
    game_world.add_layer(6)

    #background = Background()
    #game_world.add_object(background, 0)

    start_button = StartButton(600, 500)
    quit_button = QuitButton(600, 300)

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
    for game_object in game_world.all_objects():
        game_object.update()

def draw():
    clear_canvas()

    for game_object in game_world.all_objects():
        game_object.draw()

    update_canvas()

