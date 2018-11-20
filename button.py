import game_world
import game_framework
import main_state

from pico2d import*
from ant import Ant

class InactiveState:
    @staticmethod
    def enter(unit):
        pass

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        if unit.is_inactive() is False:
            unit.add_event(IdleState)

    @staticmethod
    def draw(unit):
        unit.image.clip_draw(0, unit.IMAGE_HEIGHT * 3, unit.IMAGE_WIDTH, unit.IMAGE_HEIGHT, unit.x, unit.y)


class IdleState:

    @staticmethod
    def enter(unit):
        pass

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        if unit.is_inactive():
            unit.add_event(InactiveState)

        elif unit.is_mouse_on_the_button() and unit.clicked is False:
            unit.add_event(MouseOnState)

    @staticmethod
    def draw(unit):
        unit.image.clip_draw(0, unit.IMAGE_HEIGHT * 2, unit.IMAGE_WIDTH, unit.IMAGE_HEIGHT, unit.x, unit.y)


class MouseOnState:

    @staticmethod
    def enter(unit):
        pass


    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        if unit.is_inactive():
            unit.add_event(InactiveState)

        elif unit.is_mouse_on_the_button():
            if unit.clicked:
                unit.add_event(ClickedState)
        else:
            unit.add_event(IdleState)

    @staticmethod
    def draw(unit):
        unit.image.clip_draw(0, unit.IMAGE_HEIGHT * 1, unit.IMAGE_WIDTH, unit.IMAGE_HEIGHT, unit.x, unit.y)


class ClickedState:


    @staticmethod
    def enter(unit):
        pass

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        if unit.is_inactive():
            unit.add_event(InactiveState)

        elif unit.clicked is False:
            if unit.is_mouse_on_the_button():
                unit.click_action()
                unit.add_event(MouseOnState)

            else:
                unit.add_event(IdleState)


    @staticmethod
    def draw(unit):
        unit.image.clip_draw(0, unit.IMAGE_HEIGHT * 0, unit.IMAGE_WIDTH, unit.IMAGE_HEIGHT, unit.x, unit.y)


class Button:
    def __init__(self):

        self.IMAGE_HEIGHT = 0
        self.IMAGE_WIDTH = 0

        self.event_que = []

        self.cur_state = IdleState

        self.clicked = False

        self.x = 0
        self.y = 0

        self.frame = 0
        self.init_time = 0
        self.add_self()

    def add_self(self):
        game_world.add_object(self, 5)

    def click_action(self):
        game_framework.change_state(main_state)

    def is_inactive(self):
        return False

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



class QuitButton(Button):
    image = None

    def __init__(self, x, y):
        self.IMAGE_HEIGHT = 150
        self.IMAGE_WIDTH = 300

        self.event_que = []

        self.cur_state = IdleState

        self.clicked = False

        self.x = x
        self.y = y

        self.frame = 0
        self.init_time = 0
        self.add_self()

        if QuitButton.image is None:
            self.image = load_image('resource\\image\\button\\quit_button.png')

    def click_action(self):
        game_framework.quit()

    def is_mouse_on_the_button(self):
        if game_world.x < self.x - self.IMAGE_WIDTH / 2:
            return False
        elif game_world.x > self.x + self.IMAGE_WIDTH / 2:
            return False
        elif game_world.y < self.y - (self.IMAGE_HEIGHT - 60) / 2:
            return False
        elif game_world.y > self.y + (self.IMAGE_HEIGHT - 60) / 2:
            return False

        return True
















class StartButton(Button):
    image = None

    def __init__(self, x, y):

        self.IMAGE_HEIGHT = 150
        self.IMAGE_WIDTH = 300

        self.event_que = []

        self.cur_state = IdleState

        self.clicked = False

        self.x = x
        self.y = y

        self.frame = 0
        self.init_time = 0
        self.add_self()

        if StartButton.image is None:
            self.image = load_image('resource\\image\\button\\start_button.png')

    def click_action(self):
        game_framework.change_state(main_state)

    def is_mouse_on_the_button(self):
        if game_world.x < self.x - self.IMAGE_WIDTH / 2:
            return False
        elif game_world.x > self.x + self.IMAGE_WIDTH / 2:
            return False
        elif game_world.y < self.y - (self.IMAGE_HEIGHT - 60) / 2:
            return False
        elif game_world.y > self.y + (self.IMAGE_HEIGHT - 60) / 2:
            return False

        return True


class GenerateAntButton(Button):
    image = None

    def __init__(self, x, y):

        self.IMAGE_HEIGHT = 80
        self.IMAGE_WIDTH = 80

        self.event_que = []

        if self.is_inactive():
            self.cur_state = InactiveState
        else:
            self.cur_state = IdleState

        self.clicked = False

        self.x = x
        self.y = y

        self.frame = 0
        self.init_time = 0
        self.add_self()

        if GenerateAntButton.image is None:
            self.image = load_image('resource\\image\\button\\generate_button.png')

    def click_action(self):
        game_world.money -= Ant.cost

    def is_inactive(self):
        if game_world.money < Ant.cost:
            return True
        return False

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