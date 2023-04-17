WIDTH = 500
HEIGHT = 500
BLOCKSIZE = 50
WIDTHBLOCKS = WIDTH//BLOCKSIZE
HEIGHTBLOCKS = HEIGHT//BLOCKSIZE


def run():
    from modules.game import Game
    game = Game()
    game.run()