
from pico2d import*

from background import Background

from base_player import PlayerBase
from base_computer import ComputerBase

import button

import game_framework
import game_world



HEIGHT = 800

import random

name = "MainState"

player_base = None
computer_base = None

background = None
font = None
timer = 0

def enter():
    game_world.add_layer(6)

    button.AntGenerateButton(100, 700)
    button.SpitterAntGenerateButton(200, 700)
    button.BeeGenerateButton(300,700)
    button.QueenAntGenerateButton(400, 700)
    button.JumpSpiderGenerateButton(500, 700)
    button.BazookaBugGenerateButton(600, 700)


    global background, font, player_base, computer_base
    font = load_font('ENCR10B.TTF', 16)

    quit_button = button.QuitButton(800, 700)

    background = Background()
    game_world.add_object(background, 0)

    player_base = PlayerBase(50, 230)
    computer_base = ComputerBase(1150, 230)


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

            for o in game_world.search_objects(5):
                o.handle_event(event)


        elif event.type == SDL_MOUSEBUTTONUP:

            for o in game_world.search_objects(5):
                o.handle_event(event)




def update():
    global timer

    for game_object in game_world.all_objects():
        game_object.update()
    game_world.sort_unit_layer()

    timer -= game_framework.frame_time
    if timer <= 0:
        game_world.money += 10
        timer += 1




def draw():
    clear_canvas()

    for game_object in game_world.all_objects():
        game_object.draw()


    update_canvas()
