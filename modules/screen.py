
import pygame
from modules import WIDTH, HEIGHT
class Screen():
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface((self.width, self.height))
        self.rectArea = self.surface.get_rect().inflate(-40, -40)