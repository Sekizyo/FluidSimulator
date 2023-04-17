
import pygame
from modules import STRESTEST, FONT
from modules.screen import Screen
from modules.particles import Particles
from modules.grid import Grid

class Game():
    def __init__(self):
        self.screen = Screen()
        self.fps = 10
        self.grid = Grid(self.screen.surface)
        self.particles = Particles()
        self.clock = pygame.time.Clock()
        self.rectArea = self.screen.rectArea
        self.stopRender = False
        self.exit = False
    
    def switchStopRender(self):
        if self.stopRender == True:
            self.stopRender = False
        elif self.stopRender == False:
            self.stopRender = True

    def reset(self):
        self.particles.particles = []
        self.particles.particleCount = 0
        self.particles.create(1)

    def stresTest(self):
        if STRESTEST:
            self.fps = 60
            self.particles.create(1)

    def controls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
            if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
                self.exit = True
            if pygame.key.get_pressed()[pygame.K_1] == True:
                self.particles.create(1)
            if pygame.key.get_pressed()[pygame.K_2] == True:
                self.grid.switchRenderDebug()
            if pygame.key.get_pressed()[pygame.K_SPACE] == True:
                self.switchStopRender()
            if pygame.key.get_pressed()[pygame.K_r] == True:
                self.reset()

    def updateFps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = FONT.render(fps, 1, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, fps_text, (10,0))

    def updateParticleCount(self):
        particleText = FONT.render(str(self.particles.particleCount), 1, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, particleText, (30,0))

    def render(self):
        if self.stopRender:
            return
        self.screen.surface.fill("black")
        self.updateFps()
        self.updateParticleCount()

        self.grid.moveParticles(self.particles.particles)
        self.grid.render()

        pygame.display.flip()

    def run(self):
        self.particles.create(1)
        while not self.exit:
            self.clock.tick(self.fps)
            self.stresTest()
            self.controls()
            self.render()
