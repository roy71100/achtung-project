from players import Player
from math import atan2
import cv
from arduino_com import send_command
from ai_module import new_AI_player
from consts import Move

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


class RealWorldAI(BasicRealWorldPlayer):
    def __init__(self, board, num):
        super.__init__(board, num)
        self.AI = new_AI_player(board, num)
        self.last_move = None
        send_command(Move.FORWARD)

    def get_move(self):
        return self.AI.getMove()

    def update_position(self):
        super().update_position()
        move = self.AI.get_move()
        if self.last_move != move:
            if self.last_move == Move.RIGHT:
                send_command(Move.UNRIGHT)
            if self.last_move == Move.LEFT:
                send_command(Move.UNLEFT)
            send_command(move)





