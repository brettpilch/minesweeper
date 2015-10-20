from minesweeperPG import MinesweeperPygame
import helpers as hp

def main():
    game = MinesweeperPygame(hp.load_map('1'))
    game.game_loop()

if __name__ == '__main__':
    main()
