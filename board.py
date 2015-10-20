"""
The Board class for a minesweeper game.
"""

from __future__ import division
import random
import config as cfg

class Board(object):
    """
    This class creates a data structure to contain data about the location
    of mines and which squares have been marked by the player. It includes
    methods to change the state of the game board (mark a square safe or
    flag a mine there), load a new board, create a random board, and check
    if the game has been won.
    """
    def __init__(self, territory_str = None):
        """
        If a string is supplied, create a board from that string.
        Otherwise, create a random board.
        """
        self.territory_str = territory_str
        self.territory = None
        self.make_territory()
        self.reset()

    def reset(self, difficulty = None):
        """
        Create a random board using the paramaters associated with the
        given difficulty level.
        """
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
        """
        Convert a territory string into a list of strings,
        the data structure used to keep track of game state.
        """
        if self.territory_str:
            self.territory = self.territory_str.splitlines()
            self.display = [[' ' for col in row] for row in self.territory]

    def has_mine(self, r, c):
        """
        Return True if the square at row r, column c contains a mine.
        """
        return True if self.territory[r][c] == '1' else False

    def mark_mine(self, r, c):
        """
        Declare that the square at row r, column c contains a mine.
        """
        self.display[r][c] = 'x'
        self.mines_left -= 1

    def unmark_mine(self, r, c):
        """
        Undeclare a mine in the sqaure at row r, column c.
        """
        self.display[r][c] = ' '
        self.mines_left += 1

    def neighbors(self, r, c):
        """
        Return the row and column number for each square that is adjacent
        to the square at row r, column c.
        """
        potential = [[r - 1, c - 1], [r - 1, c], [r - 1, c + 1], [r, c - 1],
                     [r, c + 1], [r + 1, c - 1], [r + 1, c], [r + 1, c + 1]]
        return [pot for pot in potential if 0 <= pot[0] < len(self.territory)
                and 0 <= pot[1] < len(self.territory[r])]

    def covered_neighbors(self, r, c):
        """
        Return only the neighbors that have not yet been marked by the player.
        """
        return [nei for nei in self.neighbors(r, c)
                if self.display[nei[0]][nei[1]] == ' ']

    def neighbor_mines(self, r, c):
        """
        Return a list of neighbor squares that contain mines.
        """
        return [nei for nei in self.neighbors(r, c)
                if self.territory[nei[0]][nei[1]] == '1']

    def mark_safe(self, r, c):
        """
        Declare that the square at row r, column c does not contain a mine.
        If wrong, the player loses.
        If correct, the number of neighboring mines is displayed in the square.
        If their are no neighboring mines, the process is repeated in
        all neighboring squares that have not been marked yet.
        """
        if self.has_mine(r, c):
            self.dead = True
            self.display[r][c] = '!'
            return
        neighbor_m = self.neighbor_mines(r, c)
        self.display[r][c] = len(neighbor_m)
        if not neighbor_m:
            for neighbor in self.covered_neighbors(r, c):
                self.mark_safe(*neighbor)

    def check_win(self):
        """
        Return True if all squares have been correctly marked.
        """
        for r, row in enumerate(self.display):
            for c, col in enumerate(row):
                if col == ' ':
                    return False
                if col == 'x' and self.territory[r][c] == '0':
                    return False
        return True
