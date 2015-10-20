from __future__ import division
import random
import config as cfg

class Board(object):
    def __init__(self, territory_str = None):
        self.territory_str = territory_str
        self.territory = None
        self.make_territory()
        self.reset()

    def reset(self, difficulty = None):
        if difficulty is not None:
            row_length, self.mines_left = cfg.LEVELS[difficulty]
            board_size = row_length ** 2
            choices = list(range(board_size))
            random.shuffle(choices)
            mines = choices[:self.mines_left]
            self.territory_str = ''
            for row in range(row_length):
                for col in range(row_length):
                    if row * row_length + col in mines:
                        self.territory_str += '1'
                    else:
                        self.territory_str += '0'
                self.territory_str += '\n'
        self.make_territory()
        self.dead = False

    def make_territory(self):
        if self.territory_str:
            self.territory = self.territory_str.splitlines()
            self.display = [[' ' for col in row] for row in self.territory]

    def has_mine(self, r, c):
        return True if self.territory[r][c] == '1' else False

    def mark_mine(self, r, c):
        self.display[r][c] = 'x'
        self.mines_left -= 1

    def unmark_mine(self, r, c):
        self.display[r][c] = ' '
        self.mines_left += 1

    def neighbors(self, r, c):
        potential = [[r - 1, c - 1], [r - 1, c], [r - 1, c + 1], [r, c - 1],
                     [r, c + 1], [r + 1, c - 1], [r + 1, c], [r + 1, c + 1]]
        return [pot for pot in potential if 0 <= pot[0] < len(self.territory)
                and 0 <= pot[1] < len(self.territory[r])]

    def uncovered_neighbors(self, r, c):
        return [nei for nei in self.neighbors(r, c)
                if self.display[nei[0]][nei[1]] == ' ']

    def neighbor_mines(self, r, c):
        return [nei for nei in self.neighbors(r, c)
                if self.territory[nei[0]][nei[1]] == '1']

    def mark_safe(self, r, c):
        if self.has_mine(r, c):
            self.dead = True
            self.display[r][c] = '!'
            return
        neighbor_m = self.neighbor_mines(r, c)
        self.display[r][c] = len(neighbor_m)
        if not neighbor_m:
            for neighbor in self.uncovered_neighbors(r, c):
                self.mark_safe(*neighbor)

    def check_win(self):
        for r, row in enumerate(self.display):
            for c, col in enumerate(row):
                if col == ' ':
                    return False
                if col == 'x' and self.territory[r][c] == '0':
                    return False
        return True
