import pygame
pygame.init()

def run():
    from modules.engine import Engine
    engine = Engine()
    engine.run()