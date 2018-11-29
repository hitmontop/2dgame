import game_world
import game_framework
import main_state

from pico2d import*
import unit_list

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
        pass

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        if unit.is_inactive():
            unit.add_event(InactiveState)

        elif game_world.clicked is False:
            if unit.is_mouse_on_the_button():
                unit.press_sound.play()
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

        self.x = 0
        self.y = 0

        self.mouseover_sound = load_wav('resource\\sound\\mouseover.wav')
        self.mouseover_sound.set_volume(32)
        self.press_sound = load_wav('resource\\sound\\press.wav')
        self.press_sound.set_volume(100)

        self.frame = 0
        self.init_time = 0
        self.add_self()

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



class QuitButton(Button):
    image = None

    def __init__(self, x, y):
        super().__init__()
        self.IMAGE_HEIGHT = 150
        self.IMAGE_WIDTH = 300
        self.x, self.y = x, y

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
        super().__init__()
        self.IMAGE_HEIGHT = 150
        self.IMAGE_WIDTH = 300
        self.x, self.y = x, y

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


class AntGenerateButton(Button):
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

        if AntGenerateButton.image is None:
            self.image = load_image('resource\\image\\button\\generate_button.png')

    def click_action(self):
        game_world.money -= unit_list.Ant.cost
        main_state.player_base.generate_unit(ant)

    def is_inactive(self):
        if game_world.money < unit_list.Ant.cost:
            return True
        return False


class SpitterAntGenerateButton(Button):
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

        if SpitterAntGenerateButton.image is None:
            self.image = load_image('resource\\image\\button\\generate_button.png')

    def click_action(self):
        game_world.money -= unit_list.SpitterAnt.cost
        main_state.player_base.generate_unit(spitter_ant)

    def is_inactive(self):
        if game_world.money < unit_list.SpitterAnt.cost:
            return True
        return False

class QueenAntGenerateButton(Button):
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

        if QueenAntGenerateButton.image is None:
            self.image = load_image('resource\\image\\button\\generate_button.png')

    def click_action(self):
        game_world.money -= unit_list.QueenAnt.cost
        main_state.player_base.generate_unit(queen_ant)

    def is_inactive(self):
        if game_world.money < unit_list.QueenAnt.cost:
            return True
        return False

class BeeGenerateButton(Button):
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

        if BeeGenerateButton.image is None:
            self.image = load_image('resource\\image\\button\\generate_button.png')

    def click_action(self):
        game_world.money -= unit_list.Bee.cost
        main_state.player_base.generate_unit(bee)

    def is_inactive(self):
        if game_world.money < unit_list.Bee.cost:
            return True
        return False

class JumpSpiderGenerateButton(Button):
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

        if JumpSpiderGenerateButton.image is None:
            self.image = load_image('resource\\image\\button\\generate_button.png')

    def click_action(self):
        game_world.money -= unit_list.JumpSpider.cost
        main_state.player_base.generate_unit(jump_spider)

    def is_inactive(self):
        if game_world.money < unit_list.JumpSpider.cost:
            return True
        return False

class BazookaBugGenerateButton(Button):
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

        if BazookaBugGenerateButton.image is None:
            self.image = load_image('resource\\image\\button\\generate_button.png')

    def click_action(self):
        game_world.money -= unit_list.JumpSpider.cost
        main_state.player_base.generate_unit(bazooka_bug)

    def is_inactive(self):
        if game_world.money < unit_list.JumpSpider.cost:
            return True
        return False

class BombardDragonFlyGenerateButton(Button):
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

        if BombardDragonFlyGenerateButton.image is None:
            self.image = load_image('resource\\image\\button\\generate_button.png')

    def click_action(self):
        game_world.money -= unit_list.BombardDragonFly.cost
        main_state.player_base.generate_unit(bombard_dragonfly)

    def is_inactive(self):
        if game_world.money < unit_list.BombardDragonFly.cost:
            return True
        return False