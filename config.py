"""
This file contains all the constants used by the minesweeper python files.
"""
# RGB COLOR CODES:
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
NAVY     = (   0,   0, 127)
VIOLET   = ( 255,   0, 255)
PINK     = ( 255, 180, 180)
YELLOW   = ( 255, 255,   0)
GRAY     = ( 100, 100, 100)
LIGHTGRAY= ( 200, 200, 200)
ORANGE   = ( 255, 127,   0)

# PYGAME GAMEBOARD FEATURES:
WIDTH = 770
HEIGHT = 770
STATUS_BAR_HEIGHT = 20
STATUS_BAR_COLOR = BLACK
FRAME_RATE = 60
WELCOME_MESSAGE = 'Welcome to Minesweeper! Choose a level'
WIN_MESSAGE = 'You win! Press ENTER to return to the menu.'
DEAD_MESSAGE = 'Oops! You hit a mine. Press ENTER to return to menu.'
INTRO_BACKGROUND = NAVY
POSTGAME_BACKGROUND = YELLOW
TEXT_COLOR = WHITE
MAIN_TEXT_FONT = 'Calibri'
MAIN_TEXT_SIZE = 30
STATUS_TEXT_FONT = 'Calibri'
STATUS_TEXT_SIZE = 15
GAME_TITLE = 'Minesweeper'
HIDDEN_COLOR = WHITE
LINE_COLOR = BLACK
LINE_THICKNESS = 3
BEST_TIMES_FILE = 'best_times.txt'

# BOARD DISPLAY CHARACTERS:
MINE_CHAR = 'x'
HIDDEN_CHAR = ' '
ERROR_CHAR = '!'

# COLOR MAPPINGS:
COLORS = {0: GRAY, 1: NAVY, 2: BLUE,
          3: GREEN, 4: YELLOW, 5: ORANGE,
          6: RED, 7: VIOLET, 8: PINK, 'x': LIGHTGRAY,
          ERROR_CHAR: WHITE}

TEXT_COLORS = {'!': RED, 1: WHITE, 2: WHITE,
               3: BLACK, 4: BLACK, 5: BLACK,
               6: WHITE, 7: WHITE, 8: BLACK,
               'pre game': WHITE, 'post game': BLACK,
               'status': WHITE}

SELECTED = {True: RED, False: WHITE}

BG_COLORS = {'safe': WHITE, 'flag': PINK}

# LEVEL DEFINITIONS
# {level: (board width in squares, number of mines)}
LEVELS = {0: (9, 10) , 1: (16, 40), 2: (23, 99), 3: (26, 150)}
