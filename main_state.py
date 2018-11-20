from background import*
from base import*
from buttons import*

name = "MainState"

player_base = None
computer_base = None

background = None
font = None
timer = 0

def enter():
    global background, font, player_base, computer_base
    font = load_font('ENCR10B.TTF', 16)

    background = Background()
    game_world.add_object(background, 0)

    player_base = Base(50, 230, False)
    computer_base = Base(1150, 230, True)

    spitter_ant = SpitterAnt(1100, random.randint(150, 200), True)
    ant = Ant(100, random.randint(150, 200), False)


def exit():
    game_world.clear()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()




def update():
    global timer

    for game_object in game_world.all_objects():
        game_object.update()

    timer -= game_framework.frame_time
    if timer <= 0:
        game_world.money += 1
        timer += 1




def draw():
    clear_canvas()

    for game_object in game_world.all_objects():
        game_object.draw()

    update_canvas()
