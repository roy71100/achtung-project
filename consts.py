from enum import Enum

snake_step_size = 3
snake_turn_angle_size = 0.05

max_fps = 30
time_per_frame = 1 / max_fps

width = 1000
height = 550

snake_radius = 5
open_step_num = 10
open_probability = 0.02

keys = [('a', 'd'), ('n', 'm'), ('o', 'p')]
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (120, 30, 200)]


class Move(Enum):
    RIGHT = 1
    LEFT = -1
    STRAIGHT = 0

