
import main_state

GROUND_HEIGHT = 230
GROUND_HEIGHT_FOR_INDICATORS = 180
GROUND_HEIGHT_FOR_AIR_UNITS = 200
SKY_HEIGHT = 350
SKY_HEIGHT_BOMBARD = 600
SKY_HEIGHT_WASP = 450


def is_this_unit_dead(self):
    if self.hp <= 0:
        return True
    elif self.x < -200 or self.x > main_state.background.w + 200:
        self.hp = 0
        return True
    return False

def get_cx_cy(x, y):
    cx, cy = main_state.canvas_width // 2 - (
            main_state.background.window_left + main_state.canvas_width // 2 - x), main_state.canvas_height // 2 - (
                     main_state.background.window_bottom + main_state.canvas_height // 2 - y)
    return cx, cy