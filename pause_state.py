from indicator import PauseMark
import button
import game_framework
import game_world
import main_state
from pico2d import*

HEIGHT = 800

name = "PauseState"

pause_mark = None
resume_button =None

def enter():
    global pause_mark, resume_button
    pause_mark = PauseMark()
    resume_button = button.ResumeButton(main_state.canvas_width -50, main_state.canvas_height-50)

def exit():
    game_world.remove_object(pause_mark)
    game_world.remove_object(resume_button)

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
    pause_mark.update()
    resume_button.update()

def draw():
    clear_canvas()

    for game_object in game_world.all_objects():
        game_object.draw()

    update_canvas()
