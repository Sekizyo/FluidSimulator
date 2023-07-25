WIDTH = 1000
HEIGHT = 1000

BLOCKSIZE = 50
WIDTHBLOCKS = WIDTH//BLOCKSIZE
HEIGHTBLOCKS = HEIGHT//BLOCKSIZE

import pygame
pygame.init()
FONT = pygame.font.SysFont("Arial", 18)

STRESTEST = True
if STRESTEST:
    BLOCKSIZE = 10
    WIDTHBLOCKS = WIDTH//BLOCKSIZE
    HEIGHTBLOCKS = HEIGHT//BLOCKSIZE

def run():
    from modules.game import Game
    game = Game()
    game.run()