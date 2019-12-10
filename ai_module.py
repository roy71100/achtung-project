import math
from math import pi, cos, sin, copysign
from consts import *
from players import VirtualPlayer


def new_AI_player(board, num):
    return AdvancedAI2(board, num)


class BasicAI(VirtualPlayer):
    def __init__(self, board, num):
        super().__init__(board, num)
        self.momentum = 0

    def get_move(self):
        if self.momentum != 0:
            move = int(self.momentum / math.fabs(self.momentum))
            self.momentum -= move
            return Move(move)

        search_angle = 0.8
        search_range = 200
        momentum = 10
        p = self.board.player_pos[self.num]

        for r in range(10, search_range):
            x = int(p.x + r * math.cos(p.angle - search_angle))
            y = int(p.y + r * math.sin(p.angle - search_angle))
            if not (not 0 < x < width or not 0 < y < height):
                if self.board.board[x][y] != -1:
                    print("detected")
                    self.momentum += momentum
                    return Move.RIGHT

            x = int(p.x + r * math.cos(p.angle + search_angle))
            y = int(p.y + r * math.sin(p.angle + search_angle))
            if not (not 0 < x < width or not 0 < y < height):
                if self.board.board[x][y] != -1:
                    print("detected")
                    self.momentum -= momentum

                    return Move.LEFT

            x = int(p.x + r * math.cos(p.angle))
            y = int(p.y + r * math.sin(p.angle))
            if not (not 0 < x < width or not 0 < y < height):
                if self.board.board[x][y] != -1:
                    print("detected")
                    self.momentum += momentum

                    return Move.RIGHT

        # return Move(randint(0,2)-1)
        return Move.STRAIGHT


class AdvancedAI(VirtualPlayer):
    def __init__(self, board, num):
        super().__init__(board, num)
        self.momentum = 0

    def get_move(self):
        search_angle = pi
        search_range = 200
        mmnt_bonus = 3
        max_mmnt = 15

        for factor in [x / 10 for x in [-10, -9, -8, -3, -2.5,  -2, -1, 1, 2, 2.5, 3, 5, 8, 9, 10]]:
            self.collision_maneuver(search_range, search_angle * factor, - copysign(mmnt_bonus, factor))
        self.flanking_maneuver()

        self.momentum = max(min(int(self.momentum), max_mmnt), -max_mmnt)

        if self.momentum != 0:
            move = copysign(1, self.momentum)
            self.momentum -= move
            return Move(move)
        return Move.STRAIGHT

    '''
    Checks whether a maneuver is required to avoid collision in given direction.
    If so, changes self's momentum and returns a steer command accordingly. Move.RIGHT returned iff no danger was found.
    :param search_range: range to search for dangers.
    :param search_angle: angle to search for dangers in.
    :param momentum: desired momentum change if danger is found.
    :return: steer command of type Move
    '''
    def collision_maneuver(self, search_range, search_angle, momentum, r_min=10):
        p = self.get_pos()
        for r in range(r_min, int(search_range)):
            x0 = int(p.x + r * cos(p.angle + search_angle)) % width
            y0 = int(p.y + r * sin(p.angle + search_angle)) % height
            for pixel in [self.board.board[x % width][y % height]
                          for x in range(x0-1, x0+2) for y in range(y0-1, y0+2)]:
                if pixel != -1:
                    self.momentum += (1 - r / search_range) * momentum
                    return

    def flanking_maneuver(self):
        ops = self.board.player_pos
        for p in ops:
            if p != self.get_pos():
                self.flanking_maneuver_on_opponent(p)

    def flanking_maneuver_on_opponent(self, other_pos):
        mmnt_bonus = 15
        max_dist = 250
        param2 = 0.1
        param3 = 0.4

        p = self.get_pos()

        self_angle = p.angle
        self_spd_vec = (cos(self_angle), sin(self_angle))

        other_angle = other_pos.angle
        other_spd_vec = (cos(other_angle), sin(other_angle))

        dist_vec = (other_pos.x - p.x, other_pos.y - p.y)
        dist = sum([coor ** 2 for coor in dist_vec]) ** 0.5
        if 10 < dist < max_dist:
            # print(f'dv{dist_vec}')
            mult = sum([self_spd_vec[i] * dist_vec[i] for i in range(2)]) / dist
            # print(f'mult\t{mult:.3f}')

            if mult < - param2:
                vec_mult = self_spd_vec[0] * other_spd_vec[1] - self_spd_vec[1] * other_spd_vec[0]
                if abs(vec_mult) < param3:
                    self.momentum += - copysign(mmnt_bonus, vec_mult)
                    # print(f'flanking {Move(- math.copysign(1, vec_mult))}\tmult={mult:.2f}')


class AdvancedAI2(BasicAI):
    def __init__(self, board, num):
        super().__init__(board, num)
        self.momentum = 0

    def get_move(self):
        search_angle = pi
        search_range = 200
        mmnt_bonus = 3
        max_mmnt = 15

        for factor in [x / 10 for x in [-9, -8, -3, -2.5,  -2, -1, 1, 2, 2.5, 3, 5, 8, 9]]:
            self.collision_maneuver(search_range, search_angle * factor, - copysign(mmnt_bonus, factor))
        self.flanking_maneuver()

        self.momentum = max(min(int(self.momentum), max_mmnt), -max_mmnt)

        if self.momentum != 0:
            move = copysign(1, self.momentum)
            self.momentum -= move
            return Move(move)
        return Move.STRAIGHT

    '''
    Checks whether a maneuver is required to avoid collision in given direction.
    If so, changes self's momentum and returns a steer command accordingly. Move.RIGHT returned iff no danger was found.
    :param search_range: range to search for dangers.
    :param search_angle: angle to search for dangers in.
    :param momentum: desired momentum change if danger is found.
    :return: steer command of type Move
    '''
    def collision_maneuver(self, search_range, search_angle, momentum, r_min=10):
        p = self.get_pos()
        for r in range(r_min, int(search_range)):
            x0 = int(p.x + r * cos(p.angle + search_angle)) % width
            y0 = int(p.y + r * sin(p.angle + search_angle)) % height
            for pixel in [self.board.board[x % width][y % height]
                          for x in range(x0-1, x0+2) for y in range(y0-1, y0+2)]:
                if pixel != -1:
                    self.momentum += (1 - r / search_range) * momentum
                    return

    def flanking_maneuver(self):
        ops = self.board.player_pos
        for p in ops:
            if p != self.get_pos():
                self.flanking_maneuver_on_opponent(p)

    def flanking_maneuver_on_opponent(self, other_pos):
        mmnt_bonus = 15
        max_dist = 250
        param2 = 0.1
        param3 = 0.4

        p = self.get_pos()

        self_angle = p.angle
        self_spd_vec = (cos(self_angle), sin(self_angle))

        other_angle = other_pos.angle
        other_spd_vec = (cos(other_angle), sin(other_angle))

        dist_vec = (other_pos.x - p.x, other_pos.y - p.y)
        dist = sum([coor ** 2 for coor in dist_vec]) ** 0.5
        if 10 < dist < max_dist:
            # print(f'dv{dist_vec}')
            mult = sum([self_spd_vec[i] * dist_vec[i] for i in range(2)]) / dist
            # print(f'mult\t{mult:.3f}')

            if mult < - param2:
                vec_mult = self_spd_vec[0] * other_spd_vec[1] - self_spd_vec[1] * other_spd_vec[0]
                if abs(vec_mult) < param3:
                    self.momentum += - copysign(mmnt_bonus, vec_mult)
                    # print(f'flanking {Move(- math.copysign(1, vec_mult))}\tmult={mult:.2f}')

    def find_open_spaces(self):
        resolution = 10
        x_size = int(self.board.width / resolution)
        y_size = int(self.board.height / resolution)
        board_chunks = [[-1 for _ in range(x_size)] for _ in range(y_size)]

    # def find_open_spaces_rec(self):

