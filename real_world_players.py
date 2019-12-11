from players import Player
from math import atan2
import cv2
from arduino_com import send_command
from ai_module import new_AI_player
from consts import Move
from players import OnPcHumanPlayer


class BasicRealWorldPlayer(Player):
    def __init__(self, game, num):
        super().__init__(game, num)

    def do_step(self):
        new_x, new_y = self.camera.get_location(self.num)
        # print(new_x, new_y)
        if new_x <= 0 or new_y <= 0 or new_x >=1 or new_y >= 1:
            return
        new_x = int(new_x * self.board.width)
        new_y = int(new_y * self.board.height)
        old_p = self.get_pos()
        pos_diff = (new_y - old_p.y, new_x - old_p.x)
        angle = atan2(*pos_diff)

        old_p.x = new_x
        old_p.y = new_y
        old_p.angle = angle


class RealWorldAI(BasicRealWorldPlayer):
    def __init__(self, game, num):
        super().__init__(game, num)
        self.AI = new_AI_player(game, num)
        self.last_move = None
        send_command(Move.FORWARD)

    def get_move(self):
        return self.AI.getMove()

    def do_step(self):
        super().do_step()
        move = self.AI.get_move()
        if self.last_move != move:
            if self.last_move == Move.RIGHT:
                send_command(Move.UNRIGHT)
            if self.last_move == Move.LEFT:
                send_command(Move.UNLEFT)
            send_command(move)


class RealWorldPCHuman(BasicRealWorldPlayer):
    def __init__(self, game, num):
        super().__init__(game, num)
        self.Human = OnPcHumanPlayer(game, num)
        self.last_move = None
        send_command(Move.FORWARD)

    def __del__(self):
        send_command(Move.STOP)

    def get_move(self):
        return self.Human.get_move()

    def do_step(self):
        super().do_step()
        move = self.Human.get_move()
        if self.last_move != move:
            if self.last_move == Move.RIGHT:
                send_command(Move.UNRIGHT)
            if self.last_move == Move.LEFT:
                send_command(Move.UNLEFT)
            send_command(move)
            self.last_move = move
