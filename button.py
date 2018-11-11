import game_world
import game_framework
import main_state
from pico2d import*

class IdleState:

    @staticmethod
    def enter(unit):
        pass

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        if unit.is_mouse_on_the_button():
            unit.add_event(MouseOnState)

    @staticmethod
    def draw(unit):
        unit.image.clip_draw(0, 100 * 2, 200, 100, unit.x, unit.y)


class MouseOnState:

    @staticmethod
    def enter(unit):
        pass


    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        if unit.is_mouse_on_the_button():
            if unit.clicked:
                unit.add_event(ClickedState)
        else:
            unit.add_event(IdleState)

    @staticmethod
    def draw(unit):
        unit.image.clip_draw(0, 100 * 1, 200, 100, unit.x, unit.y)


class ClickedState:


    @staticmethod
    def enter(unit):
        pass

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        if unit.clicked is False:
            if unit.is_mouse_on_the_button():
                print("clicked")
                unit.click_action()
                unit.add_event(MouseOnState)

            else:
                print("canceled")
                unit.add_event(IdleState)


    @staticmethod
    def draw(unit):
        unit.image.clip_draw(0, 100 * 0, 200, 100, unit.x, unit.y)


class Button:
    image = None

    def __init__(self, x, y):

        self.IMAGE_HEIGHT = 100
        self.IMAGE_WIDTH = 200

        self.event_que = []
        self.cur_state = IdleState
        self.clicked = False

        self.x = x
        self.y = y

        self.frame = 0
        self.init_time = 0
        if Button.image is None:
            self.image = load_image('button.png')

    def click_action(self):
        game_framework.change_state(main_state)

    def is_mouse_on_the_button(self):
        if game_world.x < self.x - self.IMAGE_WIDTH / 2:
            return False
        elif game_world.x > self.x + self.IMAGE_WIDTH / 2:
            return False
        elif game_world.y < self.y - self.IMAGE_HEIGHT / 2:
            return False
        elif game_world.y > self.y + self.IMAGE_HEIGHT / 2:
            return False

        return True

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self)
            self.cur_state = event
            self.cur_state.enter(self)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN:
            self.clicked = True
        elif event.type == SDL_MOUSEBUTTONUP:
            self.clicked = False

