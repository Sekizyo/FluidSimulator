
import pygame
from modules.screen import Screen
from modules.particles import Particles
from modules.physics import Physics

class Game():
    def __init__(self):
        self.screen = Screen()
        self.particles = Particles()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18)
        self.rectArea = self.screen.rectArea
        self.exit = False
    
    def controls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
            if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
                self.exit = True
            if pygame.key.get_pressed()[pygame.K_1] == True:
                self.particles.create(1, self.rectArea)

    def updateFps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps, 1, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, fps_text, (10,0))

    def render(self):
        self.screen.surface.fill("black")
        self.updateFps()

        self.particles.move()
        self.particles.colision()
        self.particles.update(self.rectArea)
        self.particles.draw(self.screen.surface)

        pygame.display.flip()

    def run(self):
        self.particles.create(1, self.rectArea)
        while not self.exit:
            self.clock.tick(60)
            self.controls()
            self.render()
