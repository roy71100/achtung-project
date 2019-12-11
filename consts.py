from enum import Enum

import numpy as np

DEBUG_NO_PROJ = True
DEBUG_NO_CV = True
DEBUG_NO_CV = True

if (DEBUG_NO_CV):
    print("debug no cv on")
if (DEBUG_NO_PROJ):
    print("debug no proj on")

snake_step_size = 3
snake_turn_angle_size = 0.05

max_fps = 30
time_per_frame = 1.0 / max_fps

width = 700
height = 700

snake_radius = 5
open_step_num = 10
open_probability = 0.02

keys = [('a', 'd'), ('n', 'm'), ('o', 'p')]
colors = [(255, 0, 0), (255, 0, 255), (0, 0, 255), (120, 30, 200)]


class Move(Enum):
    RIGHT = 1
    LEFT = -1
    STRAIGHT = 0

    UNRIGHT = 10
    UNLEFT = -10

    FORWARD = 20
    BACKWARD = 21
    STOP = 30


