from background import*

name = 'TitleState'

background = None

def enter():
    global background
    background = Background()

def exit():
    pass

def handle_events():
    pass

def update():
    pass

def draw():
    background.draw()
