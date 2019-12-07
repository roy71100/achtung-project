from consts import *
import keyboard


class Player(object):
    def __init__(self, board, num):
        self.num = num
        self.board = board

    def get_move(self):
        pass


class OnPcHumanPlayer(Player):

    def __init__(self, board, num):
        super().__init__(board, num)

    def get_move(self):
        if keyboard.is_pressed(keys[self.num][0]):
            return Move.LEFT
        elif keyboard.is_pressed(keys[self.num][1]):
            return Move.RIGHT
        return Move.STRAIGHT
