from __future__ import division
import os, os.path
import pygame as pg
import config as cfg
import random

KEYMAPS = {pg.K_f: 'flag', pg.K_s: 'safe', pg.K_r: 'remove'}
COLORS = {0: cfg.GRAY, 1: cfg.NAVY, 2: cfg.BLUE,
          3: cfg.GREEN, 4: cfg.YELLOW, 5: cfg.ORANGE,
          6: cfg.RED, 7: cfg.VIOLET, 8: cfg.PINK, 'x': cfg.LIGHTGRAY,
          cfg.ERROR_CHAR: cfg.WHITE}

TEXT_COLORS = {'!': cfg.RED, 1: cfg.WHITE, 2: cfg.WHITE,
               3: cfg.BLACK, 4: cfg.BLACK, 5: cfg.BLACK,
               6: cfg.WHITE, 7: cfg.WHITE, 8: cfg.BLACK,
               'pre game': cfg.WHITE, 'post game': cfg.BLACK,
               'status': cfg.WHITE}

SELECTED = {True: cfg.RED, False: cfg.WHITE}

BG_COLORS = {'safe': cfg.WHITE, 'flag': cfg.PINK}

LEVELS = {0: (9, 10) , 1: (16, 40), 2: (22, 99)}

class Board(object):
    def __init__(self, territory_str = None):
        self.territory_str = territory_str
        self.territory = None
        self.make_territory()
        self.reset()

    def reset(self, difficulty = None):
        if difficulty is not None:
            row_length, self.mines_left = LEVELS[difficulty]
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

class MinesweeperCLI(object):
    def __init__(self, board = None, header = ''):
        self.board = board
        self.playing = False
        self.header = header

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

class MinesweeperPygame(object):
    def __init__(self, board):
        pg.init()
        size = (cfg.WIDTH, cfg.HEIGHT + cfg.STATUS_BAR_HEIGHT)
        self.screen = pg.display.set_mode(size)
        pg.display.set_caption(cfg.GAME_TITLE)
        self.board = board
        self.clock = pg.time.Clock()
        self.done = False
        self.status = 'pre game'
        self.message = cfg.WELCOME_MESSAGE
        self.best_message = ''
        self.font = pg.font.SysFont(cfg.MAIN_TEXT_FONT, cfg.MAIN_TEXT_SIZE,
                                    False, False)
        self.status_font = pg.font.SysFont(cfg.STATUS_TEXT_FONT,
                                           cfg.STATUS_TEXT_SIZE, False, False)
        self.set_square_size()
        self.click_status = 'safe'
        self.selection = 0
        self.time = 0
        self.load_best_times()

    def load_best_times(self):
        try:
            with open(cfg.BEST_TIMES_FILE) as file_obj:
                times = file_obj.readlines()
                self.best_times = [time.strip('\n') for time in times]
        except IOError:
            self.best_times = ['100:00','100:00','100:00']
        if not self.best_times:
            self.best_times = ['100:00','100:00','100:00']

    def set_square_size(self):
        self.square_width = cfg.WIDTH / len(self.board.territory[0])
        self.square_height = cfg.HEIGHT / len(self.board.territory)

    def game_loop(self):
        """
        Draw the game board and wait for player movements.
        Display welcome message between games.
        """
        while not self.done:
            if self.status == 'in game':
                self.time += 1
                self.get_game_input()
                self.draw_board()
                self.check_status()
            elif self.status == 'pre game':
                self.draw_intro()
                self.get_intro_input()
            elif self.status == 'post game':
                self.draw_postgame()
                self.get_intro_input()
            pg.display.flip()
            self.clock.tick(cfg.FRAME_RATE)
        pg.quit()

    def check_status(self):
        if self.board.dead:
            self.message = cfg.DEAD_MESSAGE
            self.status = 'post game'
            self.click_status = 'safe'
        elif self.board.check_win():
            self.update_best_times()
            self.message = cfg.WIN_MESSAGE
            self.status = 'post game'
            self.click_status = 'safe'

    def update_best_times(self):
        old_best = string_to_time(self.best_times[self.selection])
        if self.time < old_best:
            new_best = time_to_string(self.time)
            self.best_times[self.selection] = new_best
            self.best_message = 'New record time: {}'.format(new_best)
            with open(cfg.BEST_TIMES_FILE, 'wb+') as file_obj:
                file_obj.write('\n'.join(self.best_times))


    def get_intro_input(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if self.status == 'pre game':
                        self.status = 'in game'
                        self.board.reset(self.selection)
                        self.set_square_size()
                        self.time = 0
                        self.best_message = ''
                    elif self.status == 'post game':
                        self.status = 'pre game'
                        self.message = cfg.WELCOME_MESSAGE
                if self.status == 'pre game':
                    if event.key == pg.K_DOWN:
                        self.selection = (self.selection + 1) % 3
                    elif event.key == pg.K_UP:
                        self.selection = (self.selection - 1) % 3

    def draw_intro(self):
        self.screen.fill(cfg.INTRO_BACKGROUND)
        text = self.font.render(self.message, True, TEXT_COLORS[self.status])
        xval = cfg.WIDTH / 2 - text.get_width() / 2
        yval = cfg.HEIGHT / 2 - 4 * text.get_height()
        self.screen.blit(text, [xval, yval])
        easy_message = 'EASY (10 mines) (best time: {})'.format(self.best_times[0])
        easy = self.font.render(easy_message, True, SELECTED[self.selection == 0])
        xval = cfg.WIDTH / 2 - easy.get_width() / 2
        yval = cfg.HEIGHT / 2 - 2 * easy.get_height()
        self.screen.blit(easy, [xval, yval])
        medium_message = 'MEDIUM (40 mines) (best time: {})'.format(self.best_times[1])
        medium = self.font.render(medium_message, True, SELECTED[self.selection == 1])
        xval = cfg.WIDTH / 2 - medium.get_width() / 2
        yval = cfg.HEIGHT / 2
        self.screen.blit(medium, [xval, yval])
        hard_message = 'HARD (99 mines) (best time: {})'.format(self.best_times[2])
        hard = self.font.render(hard_message, True, SELECTED[self.selection == 2])
        xval = cfg.WIDTH / 2 - hard.get_width() / 2
        yval = cfg.HEIGHT / 2 + 2 * hard.get_height()
        self.screen.blit(hard, [xval, yval])


    def draw_postgame(self):
        text = self.font.render(self.message, True, TEXT_COLORS[self.status])
        xval = cfg.WIDTH / 2 - text.get_rect().width / 2
        yval = cfg.HEIGHT - text.get_rect().height
        pg.draw.rect(self.screen, cfg.POSTGAME_BACKGROUND,
                     [xval, yval, text.get_width(), text.get_height()])
        self.screen.blit(text, [xval, yval])
        if self.best_message:
            text = self.font.render(self.best_message, True, TEXT_COLORS[self.status])
            xval = cfg.WIDTH / 2 - text.get_rect().width / 2
            yval = cfg.HEIGHT / 2 - text.get_rect().height / 2
            pg.draw.rect(self.screen, cfg.POSTGAME_BACKGROUND,
                         [xval, yval, text.get_width(), text.get_height()])
            self.screen.blit(text, [xval, yval])

    def get_game_input(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.click_status = 'flag'
            elif event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.click_status = 'safe'
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                self.evaluate_click(mouse_x, mouse_y)

    def evaluate_click(self, mouse_x, mouse_y):
        row = int(mouse_y / self.square_height)
        col = int(mouse_x / self.square_width)
        if (0 <= row < len(self.board.territory) and
            0 <= col < len(self.board.territory[0])):
            if self.click_status == 'safe':
                self.board.mark_safe(row, col)
            elif self.click_status == 'flag':
                if self.board.display[row][col] == 'x':
                    self.board.unmark_mine(row, col)
                elif self.board.display[row][col] == cfg.HIDDEN_CHAR:
                    self.board.mark_mine(row, col)

    def draw_board(self):
        self.screen.fill(BG_COLORS[self.click_status])
        for r, row in enumerate(self.board.display):
            for c, col in enumerate(row):
                xval = c * self.square_width + 1
                yval = r * self.square_height + 1
                if col not in [cfg.HIDDEN_CHAR]:
                    color = COLORS[col]
                    pg.draw.rect(self.screen, color,
                                 [xval, yval, self.square_width,
                                  self.square_height])
                    if col == 'x':
                        self.draw_flag(xval, yval)
                    elif col == cfg.ERROR_CHAR:
                        self.draw_error(xval, yval)
                if col in list(range(1, 9)):
                    text = self.font.render(str(col), True, TEXT_COLORS[col])
                    x = xval + 0.5 * self.square_width - text.get_width() / 2
                    y = yval + 0.5 * self.square_height - text.get_height() / 2
                    self.screen.blit(text, [x, y])
                if r == len(self.board.display) - 1:
                    pg.draw.line(self.screen, cfg.LINE_COLOR, [c * self.square_width, 0],
                         [c * self.square_width, cfg.HEIGHT], cfg.LINE_THICKNESS)
            pg.draw.line(self.screen, cfg.LINE_COLOR, [0, r * self.square_height],
                         [cfg.WIDTH, r * self.square_height], cfg.LINE_THICKNESS)
        pg.draw.rect(self.screen, cfg.STATUS_BAR_COLOR,
                     [0, cfg.HEIGHT, cfg.WIDTH, cfg.STATUS_BAR_HEIGHT])
        status_message = 'MINES LEFT: ' + str(self.board.mines_left)
        mines_text = self.status_font.render(status_message,
                                      True, TEXT_COLORS['status'])
        self.screen.blit(mines_text, [0, cfg.HEIGHT])
        time = time_to_string(self.time)
        time_text = self.status_font.render(time, True, TEXT_COLORS['status'])
        self.screen.blit(time_text, [cfg.WIDTH - time_text.get_width(), cfg.HEIGHT])

    def draw_flag(self, x, y):
        xval = x + self.square_width / 4
        yval = y + self.square_height / 4
        pg.draw.rect(self.screen, cfg.RED, [xval, yval, self.square_width / 2, self.square_height / 2])
        xval = x + self.square_width / 3
        yval = y + self.square_height / 3
        pg.draw.rect(self.screen, cfg.BLACK, [xval, yval, self.square_width / 3, self.square_height / 3])

    def draw_error(self, x, y):
        pg.draw.line(self.screen, cfg.RED, [x + self.square_width / 4, y + self.square_height / 4],
                     [x + 3 * self.square_width / 4, y + 3 * self.square_height / 4], 15)
        pg.draw.line(self.screen, cfg.RED, [x + self.square_width / 4, y + 3 * self.square_height / 4],
                     [x + 3 * self.square_width / 4, y + self.square_height / 4], 15)

def time_to_string(time):
    total_seconds = time // cfg.FRAME_RATE
    minutes = str(total_seconds // 60)
    seconds = total_seconds % 60
    if seconds < 10:
        seconds = '0' + str(seconds)
    else:
        seconds = str(seconds)
    return minutes + ':' + seconds

def string_to_time(string):
    minutes, seconds = string.split(':')
    return (int(minutes) * 60 + int(seconds)) * cfg.FRAME_RATE

def load_map(number, extension = '.txt'):
    filename = 'map' + number + extension
    territory_str = ''
    with open(filename, 'r') as file_obj:
        territory_str = file_obj.read()
    if territory_str:
        return Board(territory_str)
    else:
        print filename + 'not found.'

def main():
    game = MinesweeperPygame(load_map('1'))
    game.game_loop()


if __name__ == '__main__':
    main()
