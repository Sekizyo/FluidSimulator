
import pygame
from modules.screen import Screen
from modules.ball import Balls

class Game():
    def __init__(self):
        self.screen = Screen()
        self.balls = Balls()
        self.exit = False

    def controls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
            if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
                self.exit = True

    def render(self):
        self.screen.surface.fill("black")
        self.balls.render(self.screen.surface)
        pygame.display.update()

    def run(self):
        while not self.exit:
            self.controls()
            self.render()