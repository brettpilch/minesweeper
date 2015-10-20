from __future__ import division
import config as cfg
import pygame as pg
import helpers as hp

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
            self.best_times = ['100:00' for i in range(len(cfg.LEVELS))]
        if not self.best_times:
            self.best_times = ['100:00' for i in range(len(cfg.LEVELS))]
        while len(self.best_times) < len(cfg.LEVELS):
            self.best_times.append('100:00')

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
        old_best = hp.string_to_frames(self.best_times[self.selection], cfg.FRAME_RATE)
        if self.time < old_best:
            new_best = hp.frames_to_string(self.time, cfg.FRAME_RATE)
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
                        self.selection = (self.selection + 1) % len(cfg.LEVELS)
                    elif event.key == pg.K_UP:
                        self.selection = (self.selection - 1) % len(cfg.LEVELS)

    def draw_intro(self):
        self.screen.fill(cfg.INTRO_BACKGROUND)
        text = self.font.render(self.message, True, cfg.TEXT_COLORS[self.status])
        xval = cfg.WIDTH / 2 - text.get_width() / 2
        yval = cfg.HEIGHT / 2 - 4 * text.get_height()
        self.screen.blit(text, [xval, yval])
        easy_message = 'EASY (10 mines) (best time: {})'.format(self.best_times[0])
        easy = self.font.render(easy_message, True, cfg.SELECTED[self.selection == 0])
        xval = cfg.WIDTH / 2 - easy.get_width() / 2
        yval = cfg.HEIGHT / 2 - 2 * easy.get_height()
        self.screen.blit(easy, [xval, yval])
        medium_message = 'MEDIUM (40 mines) (best time: {})'.format(self.best_times[1])
        medium = self.font.render(medium_message, True, cfg.SELECTED[self.selection == 1])
        xval = cfg.WIDTH / 2 - medium.get_width() / 2
        yval = cfg.HEIGHT / 2
        self.screen.blit(medium, [xval, yval])
        hard_message = 'HARD (99 mines) (best time: {})'.format(self.best_times[2])
        hard = self.font.render(hard_message, True, cfg.SELECTED[self.selection == 2])
        xval = cfg.WIDTH / 2 - hard.get_width() / 2
        yval = cfg.HEIGHT / 2 + 2 * hard.get_height()
        self.screen.blit(hard, [xval, yval])
        insane_message = 'INSANE (150 mines) (best time: {})'.format(self.best_times[3])
        insane = self.font.render(insane_message, True, cfg.SELECTED[self.selection == 3])
        xval = cfg.WIDTH / 2 - insane.get_width() / 2
        yval = cfg.HEIGHT / 2 + 4 * insane.get_height()
        self.screen.blit(insane, [xval, yval])


    def draw_postgame(self):
        text = self.font.render(self.message, True, cfg.TEXT_COLORS[self.status])
        xval = cfg.WIDTH / 2 - text.get_rect().width / 2
        yval = cfg.HEIGHT - text.get_rect().height
        pg.draw.rect(self.screen, cfg.POSTGAME_BACKGROUND,
                     [xval, yval, text.get_width(), text.get_height()])
        self.screen.blit(text, [xval, yval])
        if self.best_message:
            text = self.font.render(self.best_message, True, cfg.TEXT_COLORS[self.status])
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
            if self.click_status == 'safe' and self.board.display[row][col] == cfg.HIDDEN_CHAR:
                self.board.mark_safe(row, col)
            elif self.click_status == 'flag':
                if self.board.display[row][col] == 'x':
                    self.board.unmark_mine(row, col)
                elif self.board.display[row][col] == cfg.HIDDEN_CHAR:
                    self.board.mark_mine(row, col)

    def draw_board(self):
        self.screen.fill(cfg.BG_COLORS[self.click_status])
        for r, row in enumerate(self.board.display):
            for c, col in enumerate(row):
                xval = c * self.square_width + 1
                yval = r * self.square_height + 1
                if col not in [cfg.HIDDEN_CHAR]:
                    color = cfg.COLORS[col]
                    pg.draw.rect(self.screen, color,
                                 [xval, yval, self.square_width,
                                  self.square_height])
                    if col == 'x':
                        self.draw_flag(xval, yval)
                    elif col == cfg.ERROR_CHAR:
                        self.draw_error(xval, yval)
                if col in list(range(1, 9)):
                    text = self.font.render(str(col), True, cfg.TEXT_COLORS[col])
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
                                      True, cfg.TEXT_COLORS['status'])
        self.screen.blit(mines_text, [0, cfg.HEIGHT])
        time = hp.frames_to_string(self.time, cfg.FRAME_RATE)
        time_text = self.status_font.render(time, True, cfg.TEXT_COLORS['status'])
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
                     [x + 3 * self.square_width / 4, y + 3 * self.square_height / 4], 10)
        pg.draw.line(self.screen, cfg.RED, [x + self.square_width / 4, y + 3 * self.square_height / 4],
                     [x + 3 * self.square_width / 4, y + self.square_height / 4], 10)
