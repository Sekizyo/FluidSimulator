import pygame
pygame.init()

def run():
    from modules.game import Game
    game = Game()
    game.run()