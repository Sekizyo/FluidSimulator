WIDTH = 1000
HEIGHT = 1000

BLOCKSIZE = 10

DEPTH = 1
PARTICLESPERCLICK = 100

WIDTHBLOCKS = WIDTH//BLOCKSIZE
HEIGHTBLOCKS = HEIGHT//BLOCKSIZE

import pygame
pygame.init()
FONT = pygame.font.SysFont("Arial", 18)

def run():
    from modules.game import Game
    game = Game()
    game.run()