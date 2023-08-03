
import pygame
from modules.__config__ import WIDTH, HEIGHT
class Screen():
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.surface = pygame.display.set_mode((self.width, self.height))