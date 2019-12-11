import keyboard as keyboard

from consts import *
from math import cos, sin
from random import random



class Player:
    def __init__(self, game, num):
        self.num = num
        self.board = game.board
        self.camera = game.camera

    def get_pos(self):
        return self.board.player_pos[self.num]

    def do_step(self):
        pass


class VirtualPlayer(Player):
    def __init__(self, game, num):
        super().__init__(game, num)

    def get_move(self):
        pass

    def do_step(self, move=None):
        if move is None:
            move = self.get_move()
        p = self.get_pos()
        p.angle += move.value * snake_turn_angle_size  # maybe error here!!!!
        p.x = int(p.x + cos(p.angle) * snake_step_size) % p.board_width
        p.y = int(p.y + sin(p.angle) * snake_step_size) % p.board_height

        p.open_counter -= 1
        if random() < open_probability:
            p.open_counter = open_step_num

        return move


class OnPcHumanPlayer(VirtualPlayer):

    def __init__(self, game, num):
        super().__init__(game, num)
        self.flag = False  # todo remove flag

    def get_move(self):
        if keyboard.is_pressed('w') and not self.flag:
            print('w pressed')
            self.flag = True
        if keyboard.is_pressed(keys[self.num][0]):
            return Move.LEFT
        elif keyboard.is_pressed(keys[self.num][1]):
            return Move.RIGHT
        elif keyboard.is_pressed('s') or not self.flag:  # todo remove this
            return Move.STOP
        return Move.FORWARD
