WIDTH = 500
HEIGHT = 500

BLOCKSIZE = 30
WIDTHBLOCKS = WIDTH//BLOCKSIZE
HEIGHTBLOCKS = HEIGHT//BLOCKSIZE

import pygame
pygame.init()
FONT = pygame.font.SysFont("Arial", 18)

STRESTEST = False
if STRESTEST:
    BLOCKSIZE = 1
    WIDTHBLOCKS = WIDTH//BLOCKSIZE
    HEIGHTBLOCKS = HEIGHT//BLOCKSIZE


def run():
    from modules.game import Game
    game = Game()
    game.run()