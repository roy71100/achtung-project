from consts import *
from math import cos, sin
from random import random
import keyboard


class Player:
    def __init__(self, board, num):
        self.num = num
        self.board = board

    def get_pos(self):
        return self.board.player_pos[self.num]

    def update_position(self):
        pass


class VirtualPlayer(Player):
    def __init__(self, board, num):
        super().__init__(board, num)

    def get_move(self):
        pass

    def update_position(self):
        move = self.get_move()
        p = self.get_pos()
        p.angle += move.value * snake_turn_angle_size  # maybe error here!!!!
        p.x = int(p.x + cos(p.angle) * snake_step_size) % p.board_width
        p.y = int(p.y + sin(p.angle) * snake_step_size) % p.board_height

        p.open_counter -= 1
        if random() < open_probability:
            p.open_counter = open_step_num


class OnPcHumanPlayer(VirtualPlayer):

    def __init__(self, board, num):
        super().__init__(board, num)

    def get_move(self):
        if keyboard.is_pressed(keys[self.num][0]):
            return Move.LEFT
        elif keyboard.is_pressed(keys[self.num][1]):
            return Move.RIGHT
        return Move.STRAIGHT
