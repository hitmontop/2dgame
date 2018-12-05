from pico2d import*
import unit_functions
import game_world
import main_state

import random
import game_framework

class Indicator_1:
    def __init__(self):
        self.image = load_image('resource\\image\\indicator\\sun_hologram.png')
        self.red_cell = load_image('resource\\image\\indicator\\red.png')
        self.green_cell = load_image('resource\\image\\indicator\\green.png')

        self.image.opacify(0.5)
        self.red_cell.opacify(0.5)
        self.green_cell.opacify(0.5)

        self.IMAGE_SIZE = self.red_cell.h

        self.x = main_state.camera.x - main_state.canvas_width //2  + game_world.x
        self.true_y = unit_functions.GROUND_HEIGHT_FOR_INDICATORS
        self.y = self.true_y + random.randint(0, 40)
        self.add_self()
        self.is_collied = False
        self.image.opacify(0.5)



    def get_bb(self):
        return self.x - (self.IMAGE_SIZE) // 2, \
               self.y - (self.IMAGE_SIZE) // 2, \
               self.x + (self.IMAGE_SIZE) // 2, \
               self.y + (self.IMAGE_SIZE) // 2

    def collide(self, a, obj):
        obj_left, obj_bottom, obj_right, obj_top = obj.get_bb()
        this_left, this_bottom, this_right, this_top = a.get_bb()

        if obj_left > this_right: return False
        if obj_bottom > this_top: return False
        if obj_right < this_left: return False
        if obj_top < this_bottom: return False
        return True

    def add_self(self):
        game_world.add_object(self, 5)

    def draw(self):
        cx, cy = unit_functions.get_cx_cy(self.x, self.true_y)

        self.image.draw(cx, cy, self.IMAGE_SIZE, self.IMAGE_SIZE)
        if self.is_collied is False:
            self.green_cell.draw(cx, cy, self.IMAGE_SIZE, self.IMAGE_SIZE)
        else:
            self.red_cell.draw(cx, cy, self.IMAGE_SIZE, self.IMAGE_SIZE)

    def update(self):
        self.x = main_state.camera.x - main_state.canvas_width //2  + game_world.x
        self.x =clamp (200, self.x, main_state.background.w//2 + 500)

        self.is_collied = False
        for obj in game_world.plants_checking_layer:
            if self.collide(self, obj):
                self.is_collied = True
                break

    def handle_event(self, event):
        pass

class Indicator_2:
    def __init__(self):
        self.image = load_image('resource\\image\\indicator\\turret_hologram.png')
        self.red_cell = load_image('resource\\image\\indicator\\red.png')
        self.green_cell = load_image('resource\\image\\indicator\\green.png')

        self.image.opacify(0.5)
        self.red_cell.opacify(0.5)
        self.green_cell.opacify(0.5)

        self.IMAGE_SIZE = self.red_cell.h

        self.x = main_state.camera.x - main_state.canvas_width //2  + game_world.x
        self.true_y = unit_functions.GROUND_HEIGHT_FOR_INDICATORS
        self.y = self.true_y + random.randint(0, 40)
        self.add_self()
        self.is_collied = False
        self.image.opacify(0.5)



    def get_bb(self):
        return self.x - (self.IMAGE_SIZE) // 2, \
               self.y - (self.IMAGE_SIZE) // 2, \
               self.x + (self.IMAGE_SIZE) // 2, \
               self.y + (self.IMAGE_SIZE) // 2

    def collide(self, a, obj):
        obj_left, obj_bottom, obj_right, obj_top = obj.get_bb()
        this_left, this_bottom, this_right, this_top = a.get_bb()

        if obj_left > this_right: return False
        if obj_bottom > this_top: return False
        if obj_right < this_left: return False
        if obj_top < this_bottom: return False
        return True

    def add_self(self):
        game_world.add_object(self, 5)

    def draw(self):
        cx, cy = unit_functions.get_cx_cy(self.x, self.true_y)

        self.image.draw(cx, cy, self.IMAGE_SIZE, self.IMAGE_SIZE)
        if self.is_collied is False:
            self.green_cell.draw(cx, cy, self.IMAGE_SIZE, self.IMAGE_SIZE)
        else:
            self.red_cell.draw(cx, cy, self.IMAGE_SIZE, self.IMAGE_SIZE)

    def update(self):
        self.x = main_state.camera.x - main_state.canvas_width //2  + game_world.x
        self.x =clamp (200, self.x, main_state.background.w//2 + 500)

        self.is_collied = False
        for obj in game_world.plants_checking_layer:
            if self.collide(self, obj):
                self.is_collied = True
                break

    def handle_event(self, event):
        pass

class PauseMark:
    def __init__(self):
        self.image = load_image('resource\\image\\pause_mark.png')
        self.IMAGE_SIZE = self.image.w//2
        self.x, self.y = main_state.canvas_width //2 , main_state.canvas_height//2
        self.frame = 0
        self.add_self()

        self.BLINK_TIME_PER_ACTION = 1
        self.BLINK_ACTION_PER_TIME = 1.0 / self.BLINK_TIME_PER_ACTION
        self.BLINK_FRAMES_PER_ACTION = 2


    def add_self(self):
        game_world.add_object(self, 5)

    def draw(self):
        self.image.clip_draw(int(self.frame) * self.IMAGE_SIZE, self.IMAGE_SIZE * 0, self.IMAGE_SIZE,
                             self.IMAGE_SIZE, self.x, self.y)


    def update(self):
        self.frame = (self.frame + self.BLINK_FRAMES_PER_ACTION *
                      self.BLINK_ACTION_PER_TIME * game_framework.frame_time) % self.BLINK_FRAMES_PER_ACTION

    def handle_event(self, event):
        pass

class VictoryMark:
    def __init__(self,x,y):
        self.image = load_image('resource\\image\\victory.png')
        self.IMAGE_SIZE = self.image.w//2
        self.x, self.y = main_state.canvas_width //2 , main_state.canvas_height//2
        self.frame = 0
        self.add_self()

        self.BLINK_TIME_PER_ACTION = 1
        self.BLINK_ACTION_PER_TIME = 1.0 / self.BLINK_TIME_PER_ACTION
        self.BLINK_FRAMES_PER_ACTION = 2


    def add_self(self):
        game_world.add_object(self, 5)

    def draw(self):
        self.image.clip_draw(int(self.frame) * self.IMAGE_SIZE, self.IMAGE_SIZE * 0, self.IMAGE_SIZE,
                             self.IMAGE_SIZE, self.x, self.y)


    def update(self):
        self.frame = (self.frame + self.BLINK_FRAMES_PER_ACTION *
                      self.BLINK_ACTION_PER_TIME * game_framework.frame_time) % self.BLINK_FRAMES_PER_ACTION

    def handle_event(self, event):
        pass

class DefeatMark:
    def __init__(self,x,y):
        self.image = load_image('resource\\image\\defeat.png')
        self.IMAGE_SIZE = self.image.w//2
        self.x, self.y = main_state.canvas_width //2 , main_state.canvas_height//2
        self.frame = 0
        self.add_self()

        self.BLINK_TIME_PER_ACTION = 1
        self.BLINK_ACTION_PER_TIME = 1.0 / self.BLINK_TIME_PER_ACTION
        self.BLINK_FRAMES_PER_ACTION = 2


    def add_self(self):
        game_world.add_object(self, 5)

    def draw(self):
        self.image.clip_draw(int(self.frame) * self.IMAGE_SIZE, self.IMAGE_SIZE * 0, self.IMAGE_SIZE,
                             self.IMAGE_SIZE, self.x, self.y)


    def update(self):
        self.frame = (self.frame + self.BLINK_FRAMES_PER_ACTION *
                      self.BLINK_ACTION_PER_TIME * game_framework.frame_time) % self.BLINK_FRAMES_PER_ACTION

    def handle_event(self, event):
        pass


class MoneyIndicator:
    def __init__(self):
        self.cx, self.cy = 80, 650

        self.image = load_image('resource\\image\\sun_resource.png')
        self.IMAGE_SIZE = self.image.w
        self.x = main_state.camera.x - main_state.canvas_width //2 + self.cx
        self.y = main_state.camera.y - main_state.canvas_height //2 + self.cy
        self.add_self()

        self.font = load_font('ENCR10B.TTF', 30)




    def add_self(self):
        game_world.add_object(self, 5)

    def draw(self):
        self.image.draw(self.cx, self.cy, self.IMAGE_SIZE, self.IMAGE_SIZE)
        self.font.draw(self.cx+ 50, self.cy, '%d' % game_world.money, (255, 255, 0))

    def update(self):
        self.x = main_state.camera.x - main_state.canvas_width //2 + 100
        self.y = main_state.camera.y - main_state.canvas_height //2 + 600


    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.x - (self.IMAGE_SIZE) // 2, \
               self.y - (self.IMAGE_SIZE) // 2, \
               self.x + (self.IMAGE_SIZE) // 2, \
               self.y + (self.IMAGE_SIZE) // 2


class UnitBuilder:
    def __init__(self):
        self.image = load_image('resource\\image\\indicator\\icon.png')
        self.IMAGE_SIZE = self.image.h
        self.x = 250
        self.y = 650
        self.add_self()
        self.font = load_font('ENCR10B.TTF', 30)

        self.build_time = 0
        self.waiting_line = []
        self.builder = []

    def waiting_line_build(self):
        for i in range(7):
            WaitingLine(i)

    def add_self(self):
        game_world.add_object(self, 5)

    def draw(self):
        if len(self.builder) == 0:
            self.image.clip_draw(0, 0, self.IMAGE_SIZE, self.IMAGE_SIZE, self.x, self.y)
        else:
            self.image.clip_draw(self.IMAGE_SIZE * ((self.builder[0])[0] +1), 0, self.IMAGE_SIZE, self.IMAGE_SIZE, self.x, self.y)
            self.font.draw(self.x+ 40, self.y + 10, '%3.1f' % self.build_time, (255,255,0) )

    def update(self):
        if len(self.builder) == 0 and ( (len(self.waiting_line) == 0) is False):
            obj = self.waiting_line.pop(0)
            self.builder.append(obj)
            self.build_time = obj[1]

        if (len(self.builder) == 0 ) is False:
            self.build_time -= game_framework.frame_time
            if self.build_time < 0:
                obj = self.builder.pop()
                main_state.player_base.generate_unit(obj[0])

    def handle_event(self, event):
        pass



class WaitingLine:
    image = None
    def __init__(self , num):
        if WaitingLine.image is None:
            WaitingLine.image = load_image('resource\\image\\indicator\\icon.png')
        self.number = num
        self.IMAGE_SIZE = self.image.h
        self.x = main_state.unit_builder.x + (main_state.unit_builder.IMAGE_SIZE //2) + 20 + self.number * 40
        self.y = main_state.unit_builder.y - 20
        self.add_self()

        self.master = main_state.unit_builder.waiting_line

    def add_self(self):
        game_world.add_object(self, 5)

    def draw(self):
        if len(self.master) < self.number + 1:
            self.image.clip_draw(0, 0, self.IMAGE_SIZE, self.IMAGE_SIZE, self.x, self.y, self.IMAGE_SIZE//2, self.IMAGE_SIZE//2)
        else:
            self.image.clip_draw(self.IMAGE_SIZE * (self.master[self.number][0] + 1) , 0, self.IMAGE_SIZE, self.IMAGE_SIZE, self.x, self.y, self.IMAGE_SIZE//2, self.IMAGE_SIZE//2)

    def update(self):
        pass

    def handle_event(self, event):
        pass