from button import*

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

