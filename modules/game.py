
import pygame
from modules.screen import Screen
from modules.particles import Particles
from modules.grid import Grid

class Game():
    def __init__(self):
        self.screen = Screen()
        self.grid = Grid(self.screen.surface)
        self.particles = Particles()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18)
        self.rectArea = self.screen.rectArea
        self.stopRender = False
        self.exit = False
    
    def switchStopRender(self):
        if self.stopRender == True:
            self.stopRender = False
        elif self.stopRender == False:
            self.stopRender = True

    def reset(self):
        self.particles.particles = pygame.sprite.Group()
        self.particles.create(1, self.rectArea)

    def controls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
            if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
                self.exit = True
            if pygame.key.get_pressed()[pygame.K_1] == True:
                self.particles.create(1, self.rectArea)
            if pygame.key.get_pressed()[pygame.K_2] == True:
                self.grid.switchRenderBlocks()
            if pygame.key.get_pressed()[pygame.K_SPACE] == True:
                self.switchStopRender()
            if pygame.key.get_pressed()[pygame.K_r] == True:
                self.reset()

    def updateFps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps, 1, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, fps_text, (10,0))

    def updateParticleCount(self):
        particleText = self.font.render(str(self.particles.particleCount), 1, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, particleText, (30,0))

    def render(self):
        if self.stopRender:
            return
        self.screen.surface.fill("black")
        self.updateFps()
        self.updateParticleCount()

        self.grid.moveParticles(self.particles.particles)

        self.particles.update(self.screen.surface)
        self.particles.draw(self.screen.surface)
        self.grid.render()

        pygame.display.flip()

    def run(self):
        self.particles.create(1, self.rectArea)
        while not self.exit:
            self.clock.tick(60)
            self.controls()
            self.render()
