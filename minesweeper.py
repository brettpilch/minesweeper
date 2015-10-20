"""
This is the main file for running the Minesweeper program.
To play the game, from the command line type:

    python minesweeper.py

"""

from minesweeperPG import MinesweeperPygame
import helpers as hp

def main():
    """
    Start a pygame version of minesweeper and enter the GUI event loop.
    """
    game = MinesweeperPygame(hp.load_map('1'))
    game.game_loop()

if __name__ == '__main__':
    main()
