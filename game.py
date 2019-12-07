import math
import time
from itertools import product
from random import randint, random
from consts import *
import pygame
from players import OnPcHumanPlayer
from ai_module import new_AI_player


class PlayerPos(object):
    def __init__(self, num, board_width, board_height):
        self.board_height = board_height
        self.board_width = board_width
        self.x = 0
        self.y = 0
        self.angle = 0
        self.num = num
        self.open_counter = 0

    def move(self, move):
        self.angle += move.value * snake_turn_angle_size  # maybe error here!!!!
        self.x = ((math.cos(self.angle)) * snake_step_size + self.x) % self.board_width
        self.y = ((math.sin(self.angle)) * snake_step_size + self.y) % self.board_height

        self.open_counter -= 1
        if random() < open_probability:
            self.open_counter = open_step_num

    def put_random_pos(self, width, height):
        self.angle = randint(0, 360) / 57.0  # 114=360/2pi
        self.x = randint(0, width - 1)
        self.y = randint(0, height - 1)


class Board(object):
    def __init__(self, width=1000, height=700, player_num=3):
        self.height = height
        self.width = width
        self.player_num = player_num
        self.board = [[-1 for i in range(height)] for j in range(width)]
        self.player_pos = [PlayerPos(i, width, height) for i in range(player_num)]

    def move(self, moves):
        for num, m in moves:
            p = self.player_pos[num]
            # print(p.x, p.y)
            if p.open_counter <= 0:
                self.board[int(p.x)][int(p.y)] = p.num
            p.move(m)

    def restart(self):
        for i in range(self.width):
            for j in range(self.height):
                self.board[i][j] = -1
        for p in self.player_pos:
            p.put_random_pos(self.width, self.height)


class GameGui(object):
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))

    def draw_board(self, board):
        pygame.event.get()
        for p in board.player_pos:
            x, y = p.x, p.y
            if p.open_counter <= 0:
                pygame.draw.circle(self.screen, colors[p.num], (int(x), int(y)), snake_radius)
            else:
                pygame.draw.circle(self.screen, (40, 40, 40), (int(x), int(y)), snake_radius)
        pygame.display.flip()


class Game:
    def __init__(self, player_num=3):
        self.board = Board(width=width, height=height, player_num=player_num)
        self.players = [OnPcHumanPlayer(self.board, i) for i in range(player_num - 2)]
        self.players.append(new_AI_player(self.board, player_num - 2))
        self.players.append(new_AI_player(self.board, player_num - 1))
        self.score = [0 for i in range(player_num)]
        self.gameGui = GameGui(width, height)

        self.circle_points = []
        for x, y in product(range(int(snake_radius / 2), int(snake_radius) + 1), repeat=2):
            if x ** 2 + y ** 2 <= snake_radius ** 2:
                self.circle_points += [(x, y), (x, -y), (-x, y), (-x, -y)]

    def play_round(self):
        self.restart_round()
        alive = [*range(len(self.players))]
        while len(alive) > 1:
            t = time.time()

            self.gameGui.draw_board(self.board)

            moves = [(i, self.players[i].get_move()) for i in alive]
            self.board.move(moves)
            dead = self.check_dead(alive)

            if dead:
                for i in dead:
                    alive.remove(i)

            passed_time = time.time() - t
            if passed_time < time_per_frame:
                time_to_wait = time_per_frame - passed_time
                pygame.time.delay(int(1000 * time_to_wait))

        if len(alive) > 0:
            print(f'Game over, Player {alive[0]} won!')
        else:
            print(f'Error - no players left alive')

    def restart_round(self):
        self.board.restart()

    def check_dead(self, alive):
        dead = []
        for i in alive:
            p = self.board.player_pos[i]
            if p.open_counter <= 0:
                for x, y in self.circle_points:
                    # a bit inefficient but i don't think it has big impact

                    # peice of code that is bugged ): dont think it is smart to waist more time here
                    # if math.fabs(math.atan(y/x) - p.angle) < (6.28 / 3)\
                    #         or math.fabs(math.atan(y/x) - p.angle - 6.28) < (6.28 / 3):

                    x = int(p.x + x + snake_radius * math.cos(p.angle))
                    y = int(p.y + y + snake_radius * math.sin(p.angle))
                    if not 0 < x < width or not 0 < y < height:
                        continue
                    if self.board.board[x][y] != -1:
                        print("player " + str(p.num) + " has fallen.")
                        dead.append(p.num)
                        break
        return dead

    def run(self):
        self.play_round()
