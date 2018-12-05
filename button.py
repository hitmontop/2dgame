import game_world
import game_framework
import main_state

from pico2d import*
import unit_list

ant, spitter_ant, bee, queen_ant, beetle, bazooka_bug, bombard_dragonfly, wasp = range(8)

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
    font = None
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

        if Button.font is None:
            Button.font = load_font('ENCR10B.TTF', 20)

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
            QuitButton.image = load_image('resource\\image\\button\\quit_button.png')

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
            StartButton.image = load_image('resource\\image\\button\\start_button.png')

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
        self.cost = unit_list.Ant.cost

        if self.is_inactive():
            self.cur_state = InactiveState
        else:
            self.cur_state = IdleState

        self.x, self.y = x, y

        if AntGenerateButton.image is None:
            AntGenerateButton.image = load_image('resource\\image\\button\\ant_button.png')

    def click_action(self):
        if len(main_state.unit_builder.waiting_line) < 7 :
            game_world.money -= unit_list.Ant.cost
            main_state.unit_builder.waiting_line.append([unit_list.ant, unit_list.Ant.BUILD_TIME])


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
        self.cost = unit_list.SpitterAnt.cost

        if self.is_inactive():
            self.cur_state = InactiveState
        else:
            self.cur_state = IdleState

        self.x, self.y = x, y

        if SpitterAntGenerateButton.image is None:
            SpitterAntGenerateButton.image = load_image('resource\\image\\button\\spitter_ant_button.png')

    def click_action(self):
        if len(main_state.unit_builder.waiting_line) < 7 :
            game_world.money -= unit_list.SpitterAnt.cost
            main_state.unit_builder.waiting_line.append([unit_list.spitter, unit_list.SpitterAnt.BUILD_TIME])

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
        self.cost = unit_list.QueenAnt.cost

        if self.is_inactive():
            self.cur_state = InactiveState
        else:
            self.cur_state = IdleState

        self.x, self.y = x, y

        if QueenAntGenerateButton.image is None:
            QueenAntGenerateButton.image = load_image('resource\\image\\button\\queen_button.png')

    def click_action(self):
        if len(main_state.unit_builder.waiting_line) < 7 :
            game_world.money -= unit_list.QueenAnt.cost
            main_state.unit_builder.waiting_line.append([unit_list.queen, unit_list.QueenAnt.BUILD_TIME])

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
        self.cost = unit_list.Bee.cost

        if self.is_inactive():
            self.cur_state = InactiveState
        else:
            self.cur_state = IdleState

        self.x, self.y = x, y

        if BeeGenerateButton.image is None:
            BeeGenerateButton.image = load_image('resource\\image\\button\\bee_button.png')

    def click_action(self):
        if len(main_state.unit_builder.waiting_line) < 7:
            game_world.money -= unit_list.Bee.cost
            main_state.unit_builder.waiting_line.append([unit_list.bee, unit_list.Bee.BUILD_TIME])


    def is_inactive(self):
        if game_world.money < unit_list.Bee.cost:
            return True
        return False

class BeetleGenerateButton(Button):
    image = None

    def __init__(self, x, y):
        super().__init__()
        self.IMAGE_HEIGHT = 80
        self.IMAGE_WIDTH = 80
        self.cost = unit_list.Beetle.cost

        if self.is_inactive():
            self.cur_state = InactiveState
        else:
            self.cur_state = IdleState

        self.x, self.y = x, y

        if BeetleGenerateButton.image is None:
            BeetleGenerateButton.image = load_image('resource\\image\\button\\beetle_button.png')

    def click_action(self):
        if len(main_state.unit_builder.waiting_line) < 7:
            game_world.money -= unit_list.Beetle.cost
            main_state.unit_builder.waiting_line.append([unit_list.beetle, unit_list.Beetle.BUILD_TIME])


    def is_inactive(self):
        if game_world.money < unit_list.Beetle.cost:
            return True
        return False

class BazookaBugGenerateButton(Button):
    image = None

    def __init__(self, x, y):
        super().__init__()
        self.IMAGE_HEIGHT = 80
        self.IMAGE_WIDTH = 80
        self.cost = unit_list.BazookaBug.cost

        if self.is_inactive():
            self.cur_state = InactiveState
        else:
            self.cur_state = IdleState

        self.x, self.y = x, y

        if BazookaBugGenerateButton.image is None:
            BazookaBugGenerateButton.image = load_image('resource\\image\\button\\bazooka_button.png')

    def click_action(self):
        if len(main_state.unit_builder.waiting_line) < 7:
            game_world.money -= unit_list.BazookaBug.cost
            main_state.unit_builder.waiting_line.append([unit_list.bazooka, unit_list.BazookaBug.BUILD_TIME])

    def is_inactive(self):
        if game_world.money < unit_list.BazookaBug.cost:
            return True
        return False

class BombardDragonFlyGenerateButton(Button):
    image = None

    def __init__(self, x, y):
        super().__init__()
        self.IMAGE_HEIGHT = 80
        self.IMAGE_WIDTH = 80
        self.cost = unit_list.BombardDragonFly.cost

        if self.is_inactive():
            self.cur_state = InactiveState
        else:
            self.cur_state = IdleState

        self.x, self.y = x, y

        if BombardDragonFlyGenerateButton.image is None:
            BombardDragonFlyGenerateButton.image = load_image('resource\\image\\button\\dragon_button.png')

    def click_action(self):
        if len(main_state.unit_builder.waiting_line) < 7:
            game_world.money -= unit_list.BombardDragonFly.cost
            main_state.unit_builder.waiting_line.append([unit_list.dragon, unit_list.BombardDragonFly.BUILD_TIME])


    def is_inactive(self):
        if game_world.money < unit_list.BombardDragonFly.cost:
            return True
        return False

class WaspGenerateButton(Button):
    image = None

    def __init__(self, x, y):
        super().__init__()
        self.IMAGE_HEIGHT = 80
        self.IMAGE_WIDTH = 80
        self.cost = unit_list.Wasp.cost

        if self.is_inactive():
            self.cur_state = InactiveState
        else:
            self.cur_state = IdleState

        self.x, self.y = x, y

        if WaspGenerateButton.image is None:
            WaspGenerateButton.image = load_image('resource\\image\\button\\wasp_button.png')

    def click_action(self):
        if len(main_state.unit_builder.waiting_line) < 7:
            game_world.money -= unit_list.Wasp.cost
            main_state.unit_builder.waiting_line.append( [unit_list.wasp, unit_list.Wasp.BUILD_TIME])


    def is_inactive(self):
        if game_world.money < unit_list.Wasp.cost:
            return True
        return False


import pause_state
class PauseButton(Button):
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

        if PauseButton.image is None:
            PauseButton.image = load_image('resource\\image\\button\\pause_button.png')

    def click_action(self):
        game_framework.push_state(pause_state)

    def is_inactive(self):
        return False

class ResumeButton(Button):
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

        if ResumeButton.image is None:
            ResumeButton.image = load_image('resource\\image\\button\\resume_button.png')

    def click_action(self):
        game_framework.pop_state()

    def is_inactive(self):
        return False


class RestartButton(Button):
    image = None

    def __init__(self, x, y):
        super().__init__()
        self.IMAGE_HEIGHT = 100
        self.IMAGE_WIDTH = 200

        if self.is_inactive():
            self.cur_state = InactiveState
        else:
            self.cur_state = IdleState

        self.x, self.y = x, y

        if RestartButton.image is None:
            RestartButton.image = load_image('resource\\image\\button\\restart_button.png')

    def click_action(self):
        game_framework.change_state(main_state)

    def is_inactive(self):
        return False
