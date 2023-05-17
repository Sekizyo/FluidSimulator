
import sys
import pygame
from modules import STRESTEST, FONT
from modules.screen import Screen
from modules.particles import Particles
from modules.grid import Grid

class Game():
    def __init__(self):
        self.screen = Screen()
        self.rectArea = self.screen.rectArea
        self.grid = Grid(self.screen.surface)
        self.particles = Particles()

        self.fps = 10
        self.clock = pygame.time.Clock()
        
        self.stopRender = False
        self.exit = False
    
    def run(self):
        while not self.exit:
            self.clock.tick(self.fps)
            self.logic()
            self.render()

    def logic(self):
        self.controlsKeyboard()
        self.controlsMouse()

        if self.stopRender:
            return
            
        self.stresTest()
        self.grid.moveParticles(self.particles.particles)

    def stresTest(self):
        if STRESTEST:
            self.fps = 60
            self.particles.create(1)
            self.grid.renderDebug = False
            # print("particles: ", sys.getsizeof(self.particles.particles))
            # print("blocks: ", sys.getsizeof(self.grid.blocks))

    def controlsKeyboard(self):
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
            self.particles.reset()
            self.grid.refreshBlockDir()

    def controlsMouse(self):
        if pygame.mouse.get_pressed()[0]:
            self.particles.createAtPos(pygame.mouse.get_pos())
        elif pygame.mouse.get_pressed()[1]:
            self.grid.changeBlockDirections(pygame.mouse.get_pos())

    def render(self):
        if self.stopRender:
            return

        self.screen.surface.fill("black")

        self.updateFps()
        self.updateParticleCount()
        self.grid.render()

        pygame.display.flip()

    def switchStopRender(self):
        if self.stopRender == True:
            self.stopRender = False
        elif self.stopRender == False:
            self.stopRender = True

    def updateFps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = FONT.render(fps, 1, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, fps_text, (10,0))

    def updateParticleCount(self):
        particleText = FONT.render(str(self.particles.particleCount), 1, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, particleText, (30,0))


