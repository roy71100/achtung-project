from players import Player
from math import atan2


class BasicRealWorldPlayer(Player):
    def __init__(self, board, num):
        super().__init__(board, num)

    def update_position(self):
        new_x, new_y = vision.getPlace(self.num)
        old_p = self.get_pos()
        pos_diff = (new_y - old_p.y, new_x - old_p.x)
        angle = atan2(*pos_diff)

        old_p.x = new_x
        old_p.y = new_y
        old_p.angle = angle
