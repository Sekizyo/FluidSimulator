
import pygame
from modules import WIDTH, HEIGHT
class Screen():
    def __init__(self):
        pygame.init()

        canvas = pygame.display.set_mode((WIDTH, HEIGHT))
        
        pygame.display.set_caption("My Board")