from pico2d import*

import game_framework
import game_world

from background import Background
from background import Background2
from background import Background3

from indicator import MoneyIndicator

from camera import Camera
from base_player import PlayerBase
from base_computer import ComputerBase

import button
import button_toggle
import pause_state


import random


import unit_list
import unit_functions

name = "MainState"

canvas_width = 0
canvas_height = 0

player_base = None
computer_base = None
camera = None

background = None
font = None
timer = 0
moeny_indicator = None

def enter():
    game_world.money =200

    get_canvas_w_d()

    game_world.add_layer(6)

    button_toggle.SunFlowerGenerateButton(50, 750)
    button.AntGenerateButton(150, 750)
    button.BeeGenerateButton(250,750)
    button.SpitterAntGenerateButton(350, 750)
    button.BazookaBugGenerateButton(450, 750)
    button.BombardDragonFlyGenerateButton(550, 750)
    button.QueenAntGenerateButton(650, 750)
    button.WaspGenerateButton(750, 750)
    button_toggle.TurretGenerateButton(850, 750)
    button.BeetleGenerateButton(950, 750)

    button.PauseButton(canvas_width - 50, canvas_height -50)



    global background, font, player_base, computer_base, camera, moeny_indicator
    font = load_font('ENCR10B.TTF', 16)

    background = Background()


    camera = Camera()
    game_world.add_object(camera, 5)

    background.set_center_object(camera)
    camera.set_background(background)

    background2 = Background2()
    background2.set_center_object(background)

    background3 = Background3()
    background3.set_center_object(background)

    game_world.add_object(background3, 0)
    game_world.add_object(background2, 0)
    game_world.add_object(background, 0)

    player_base = PlayerBase(50, unit_functions.GROUND_HEIGHT)
    computer_base = ComputerBase(background.w - 50, unit_functions.GROUND_HEIGHT)

    moeny_indicator = MoneyIndicator()

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

            game_world.x, game_world.y = event.x, canvas_height - 1 - event.y


        elif event.type == SDL_MOUSEBUTTONDOWN:
            game_world.clicked = True


        elif event.type == SDL_MOUSEBUTTONUP:
            game_world.clicked = False




def update():
    global timer

    for game_object in game_world.all_objects():
        game_object.update()
    game_world.sort_unit_layer()



def pause():
    pass


def resume():
    pass


def draw():
    clear_canvas()

    for game_object in game_world.all_objects():
        game_object.draw()


    update_canvas()


def get_canvas_w_d():
    global canvas_width, canvas_height

    canvas_height = get_canvas_height()
    canvas_width = get_canvas_width()