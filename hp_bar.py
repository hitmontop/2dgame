from pico2d import*

import unit_functions

class IdleState:

    @staticmethod
    def enter(unit):
        pass

    @staticmethod
    def exit(unit):
        pass

    @staticmethod
    def do(unit):
        unit.x = unit.master.x
        unit.y = unit.master.y + 40
        unit.hp = unit.master.hp

    @staticmethod
    def draw(unit):
        cx, cy = unit_functions.get_cx_cy(unit.x, unit.y)

        if unit.is_foe:
            if (unit.hp / unit.max_hp) * 10 > 9:
                unit.image.clip_draw(50, 5 * 9, 50, 5, cx, cy)

            elif (unit.hp / unit.max_hp) * 10 > 8:
                unit.image.clip_draw(50, 5 * 8, 50, 5, cx, cy)

            elif (unit.hp / unit.max_hp) * 10 > 7:
                unit.image.clip_draw(50, 5 * 7, 50, 5, cx, cy)

            elif (unit.hp / unit.max_hp) * 10 > 6:
                unit.image.clip_draw(50, 5 * 6, 50, 5, cx, cy)

            elif (unit.hp / unit.max_hp) * 10 > 5:
                unit.image.clip_draw(50, 5 * 5, 50, 5, cx, cy)

            elif (unit.hp / unit.max_hp) * 10 > 4:
                unit.image.clip_draw(50, 5 * 4, 50, 5, cx, cy)

            elif (unit.hp / unit.max_hp) * 10 > 3:
                unit.image.clip_draw(50, 5 * 3, 50, 5, cx, cy)

            elif (unit.hp / unit.max_hp) * 10 > 2:
                unit.image.clip_draw(50, 5 * 2, 50, 5, cx, cy)

            elif (unit.hp / unit.max_hp) * 10 > 1:
                unit.image.clip_draw(50, 5 * 1, 50, 5, cx, cy)

            else:
                unit.image.clip_draw(50, 5 * 0, 50, 5, cx, cy)

        else:
            if (unit.hp / unit.max_hp) * 10 > 9:
                unit.image.clip_draw(0, 5 * 9, 50, 5, cx, cy)

            elif (unit.hp / unit.max_hp) * 10 > 8:
                unit.image.clip_draw(0, 5 * 8, 50, 5, cx, cy)

            elif (unit.hp / unit.max_hp) * 10 > 7:
                unit.image.clip_draw(0, 5 * 7, 50, 5, cx, cy)

            elif (unit.hp / unit.max_hp) * 10 > 6:
                unit.image.clip_draw(0, 5 * 6, 50, 5, cx, cy)

            elif (unit.hp / unit.max_hp) * 10 > 5:
                unit.image.clip_draw(0, 5 * 5, 50, 5, cx, cy)

            elif (unit.hp / unit.max_hp) * 10 > 4:
                unit.image.clip_draw(0, 5 * 4, 50, 5, cx, cy)

            elif (unit.hp / unit.max_hp) * 10 > 3:
                unit.image.clip_draw(0, 5 * 3, 50, 5, cx, cy)

            elif (unit.hp / unit.max_hp) * 10 > 2:
                unit.image.clip_draw(0, 5 * 2, 50, 5, cx, cy)

            elif (unit.hp / unit.max_hp) * 10 > 1:
                unit.image.clip_draw(0, 5 * 1, 50, 5, cx, cy)

            else:
                unit.image.clip_draw(0, 5 * 0, 50, 5, cx, cy)


class HpBar:

    image = None

    def __init__(self, x, y, max_hp, hp, is_foe, master):
        self.max_hp = max_hp
        self.hp = hp
        self.is_foe = is_foe
        self.x, self.y = x, y + 40
        self.master = master

        if HpBar.image is None:
            HpBar.image = load_image('resource\\image\\hp_bar.png')

        self.cur_state = IdleState

    def draw(self):
        self.cur_state.draw(self)

    def update(self):
        self.cur_state.do(self)