import numpy as np
from cv2 import cv2

from consts import snake_radius, colors
from image_handeling import proj
from image_handeling.proj import show_projection

hole_color = (40, 40, 40)


class GameGui(object):
    name = "screen"

    def __init__(self, width, height):
        print (width,height)
        proj.calculate_projection(width, height)
        self.screen = 255 * np.ones((width, height, 3))
        self.screen[:,:,1] = 200

    def draw_board(self, board):
        # pass
        for p in board.player_pos:
            x, y = p.x, p.y
            if p.open_counter <= 0:
                cv2.circle(self.screen, (int(x), int(y)), snake_radius, colors[p.num], thickness=-1)
            else:
                cv2.circle(self.screen, (int(x), int(y)), snake_radius, hole_color, thickness=-1)


        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            exit()
        # cv2.imshow("screen", self.screen)
        show_projection(self.screen)