import numpy as np
from cv2 import cv2

from consts import snake_radius, colors
from proj import show_projection

hole_color = np.array([40, 40, 40])


class GameGui(object):
    name = "screen"

    def __init__(self, width, height):
        self.screen = 255 * np.ones((width, height, 3))

    def draw_board(self, board):
        for p in board.player_pos:
            x, y = p.x, p.y
            if p.open_counter <= 0:
                cv2.circle(self.screen, (int(x), int(y)), snake_radius, colors[p.num], thickness=-1)
            else:
                cv2.circle(self.screen, (int(x), int(y)), snake_radius, hole_color, thickness=-1)

        show_projection(self.screen)

        # printboard2(board.board)
