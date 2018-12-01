import game_world
import game_framework
import main_state

from indicator import Indicator_1
from pico2d import*
import unit_list
import unit_functions

ant, spitter_ant, bee, queen_ant, jump_spider, bazooka_bug, bombard_dragonfly = range(7)

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

        elif unit.is_mouse_on_the_button() and game_world.clicked is False:
            unit.add_event(MouseOnState)

    @staticmethod
    def draw(unit):
        unit.image.clip_draw(0, unit.IMAGE_HEIGHT * 2, unit.IMAGE_WIDTH, unit.IMAGE_HEIGHT, unit.x, unit.y)


class MouseOnState:

    @staticmethod
    def enter(unit):
        unit.mouseover_sound.play()


    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        if unit.is_inactive():
            unit.add_event(InactiveState)

        elif unit.is_mouse_on_the_button():
            if game_world.clicked:
                unit.add_event(ClickedState)
        else:
            unit.add_event(IdleState)

    @staticmethod
    def draw(unit):
        unit.image.clip_draw(0, unit.IMAGE_HEIGHT * 1, unit.IMAGE_WIDTH, unit.IMAGE_HEIGHT, unit.x, unit.y)


class ClickedState:


    @staticmethod
    def enter(unit):
        unit.indicator = Indicator_1()

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        if unit.is_inactive():
            unit.add_event(InactiveState)

        elif game_world.clicked is False:
            unit.press_sound.play()
            unit.click_action()
            game_world.remove_object(unit.indicator)
            unit.add_event(MouseOnState)




    @staticmethod
    def draw(unit):
        unit.image.clip_draw(0, unit.IMAGE_HEIGHT * 0, unit.IMAGE_WIDTH, unit.IMAGE_HEIGHT, unit.x, unit.y)


class ToggleButton:
    def __init__(self):

        self.IMAGE_HEIGHT = 0
        self.IMAGE_WIDTH = 0

        self.event_que = []

        self.cur_state = IdleState

        self.x = 0
        self.y = 0

        self.mouseover_sound = load_wav('resource\\sound\\mouseover.wav')
        self.mouseover_sound.set_volume(32)
        self.press_sound = load_wav('resource\\sound\\press.wav')
        self.press_sound.set_volume(100)

        self.frame = 0
        self.init_time = 0
        self.add_self()
        self.indicator = None

    def add_self(self):
        game_world.add_object(self, 5)

    def click_action(self):
        pass

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

    def handle_event(self):
        pass



class TurretGenerateButton(ToggleButton):
    image = None

    def __init__(self, x, y):
        super().__init__()
        self.IMAGE_HEIGHT = 80
        self.IMAGE_WIDTH = 80

        if self.is_inactive():
            self.cur_state = InactiveState
        else:
            self.cur_state = IdleState

        self.x, self.y = x, y
        self.indicator = None

        if TurretGenerateButton.image is None:
            self.image = load_image('resource\\image\\button\\generate_button.png')

    def click_action(self):
        game_world.money -= unit_list.Turret.cost
        obj = unit_list.Bloom(self.indicator.x, self.indicator.y, False)

    def is_inactive(self):
        if game_world.money < unit_list.Turret.cost:
            return True
        return False
