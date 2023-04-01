
import pygame
from modules import WIDTH, HEIGHT
class Screen():
    def __init__(self):
        pygame.init()
        self.width = WIDTH
        self.height = HEIGHT
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface((self.width, self.height))
        # self.font = pygame.font.SysFont("arial.ttf", 30)