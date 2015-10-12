import os

class Board(object):
    def __init__(self, territory_str = None):
        self.territory_str = territory_str
        self.territory = None
        self.make_territory(territory_str)
        self.display = [[' ' for col in row] for row in self.territory]
        self.dead = False

    def make_territory(self, territory_str):
        if territory_str:
            self.territory = territory_str.splitlines()

    def has_mine(self, r, c):
        return True if self.territory[r][c] == '1' else False

    def mark_mine(self, r, c):
        self.display[r][c] = 'x'

    def unmark_mine(self, r, c):
        self.display[r][c] = ' '

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

class MinesweeperCLI(object):
    def __init__(self, board = None, header = ''):
        self.board = board
        self.playing = False
        self.header = header
        self.game_loop()

    def game_loop(self):
        while not (self.board and self.board.territory):
            print 'You must load a map first.'
            self.game_menu()
        while not self.playing:
            self.game_menu()
        while self.playing:
            self.display_board()
            self.get_next_move()
            if self.board.check_win():
                self.game_win()
            if self.board.dead:
                self.game_lose()

    def game_menu(self):
        reply = raw_input('Choose an action: (l)oad map, (p)lay, (q)uit ')
        if reply == 'l':
            self.input_map()
        elif reply == 'p':
            self.playing = True
            self.game_loop()
        elif reply == 'q':
            quit()
        else:
            print "Invalid Entry. Must be 'l', 'p', or 'q'."
            self.game_menu()

    def game_win(self):
        print 'Congratulations! You won!'
        self.playing = False
        self.game_menu()

    def game_lose(self):
        print 'Oops! You hit a mine! Game over.'
        self.playing = False
        new_board = Board(self.board.territory_str)
        self.__init__(new_board, self.header)

    def input_map(self):
        reply = None
        choices = os.listdir(os.getcwd())
        choices = [choice[3:-4] for choice in choices if choice.startswith('map')]
        print 'Available maps:',
        for choice in choices:
            print choice + ',',
        print
        reply = raw_input('Enter a map number, (q)uit, or return to (m)enu: ')
        if reply == 'm':
            self.game_menu()
        elif reply == 'q':
            quit()
        elif reply in choices:
            self.load_map(reply)
        else:
            print "Invalid Entry. Must be a valid map number, 'q', or 'm'."
            self.input_map()

    def initialize_board(self, territory_str):
        self.board = Board(territory_str)
        cols = [str(i) for i in range(len(self.board.territory[0]))]
        self.header = '  ' + ''.join(cols)

    def load_map(self, number, extension = '.txt'):
        filename = 'map' + number + extension
        territory_str = ''
        with open(filename, 'r') as file_obj:
            territory_str = file_obj.read()
        if territory_str:
            self.initialize_board(territory_str)
        else:
            print filename + 'not found.'
        self.game_menu()

    def display_board(self):
        cols = [i for i in range(len(self.board.territory[0]))]
        print self.header
        for r, row in enumerate(self.board.display):
            print str(r) + ' ' + ''.join([str(r) for r in row])

    def get_next_move(self):
        print 'Choose a square to act upon'
        row = self.input_row()
        col = self.input_col()
        move = self.input_move()
        if move == 'mine':
            print 'Flagging a mine at ({},{}).'.format(row, col)
            self.board.mark_mine(row, col)
        elif move == 'safe':
            print 'Marking a safe zone at ({},{}).'.format(row, col)
            self.board.mark_safe(row, col)
        elif move == 'remove':
            print 'Removing flag from ({},{}).'.format(row, col)
            self.board.unmark_mine(row, col)
        else:
            print 'there is a bug in get_next_move()'

    def input_row(self):
        row = raw_input('Enter a row number: ')
        choices = [str(i) for i in range(len(self.board.territory))]
        if row == 'q':
            self.game_menu()
        elif row not in choices:
            print 'Invalid entry. Must be in {choices}'.format(choices = choices)
            return self.input_row()
        else:
            return int(row)

    def input_col(self):
        col = raw_input('Enter a column number: ')
        choices = [str(i) for i in range(len(self.board.territory[0]))]
        if col == 'q':
            self.game_menu()
        elif col not in choices:
            print 'Invalid entry. Must be in {choices}'.format(choices = choices)
            return self.input_col()
        else:
            return int(col)

    def input_move(self):
        move = raw_input('(f)lag a mine there, (r)emove a flag, or (d)eclare it safe? ')
        if move == 'f':
            return 'mine'
        elif move == 'd':
            return 'safe'
        elif move == 'r':
            return 'remove'
        elif move == 'q':
            self.game_menu()
        else:
            print "Invalid entry. Must be 'f', 'r', or 'd'."
            return self.input_move()

def main():
    game = MinesweeperCLI()

if __name__ == '__main__':
    main()
