
import sys
import pygame
from modules import STRESTEST, FONT
from modules.screen import Screen
from modules.grid import Grid

class Game():
    def __init__(self):
        self.screen = Screen()
        self.grid = Grid(self.screen.surface)

        self.fps = 5
        self.clock = pygame.time.Clock()
        
        self.stopRender = False
        self.exit = False
    
    def run(self):
        while not self.exit:
            self.clock.tick(self.fps)
            self.stresTest()
            self.logic()
            self.render()

    def stresTest(self):
        if STRESTEST:
            self.fps = 60
            self.grid.renderDebug = False
            # print("particles: ", sys.getsizeof(self.particles.particles))
            # print("blocks: ", sys.getsizeof(self.grid.blocks))

    def logic(self):
        self.controlsKeyboard()
        self.controlsMouse()

        self.grid.loop()

    def controlsKeyboard(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True

        if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
            self.exit = True
        # if pygame.key.get_pressed()[pygame.K_1] == True:
        #     self.grid.particles.create(1)
        if pygame.key.get_pressed()[pygame.K_2] == True:
            self.grid.switchRenderDebug()
        if pygame.key.get_pressed()[pygame.K_r] == True:
            self.grid.reset()

    def controlsMouse(self):
        if pygame.mouse.get_pressed()[0]:
            self.grid.addParticleToBlockByPos(pygame.mouse.get_pos())
        if pygame.mouse.get_pressed()[1]:
            self.grid.dierction.changeBlockDirections(pygame.mouse.get_pos())

    def render(self):
        self.screen.surface.fill("black")

        self.grid.renderGrid()
        self.updateFps()
        self.updateParticleCount()
        self.updateParticleMass()

        pygame.display.flip()

    def updateFps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = FONT.render(fps, 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, fps_text, (10,0))

    def updateParticleCount(self):
        particleText = FONT.render(str(self.grid.particleCount), 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, particleText, (50,0))

    def updateParticleMass(self):
        particleText = FONT.render(str(self.grid.getTotalMass()), 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, particleText, (100,0))
