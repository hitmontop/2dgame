import pico2d
import title_state
import game_framework

pico2d.open_canvas(1200, 800, sync=True)
game_framework.run(title_state)
pico2d.close_canvas()
