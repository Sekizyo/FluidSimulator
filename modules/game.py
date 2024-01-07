
import pygame
from modules.__config__ import FONT
from modules.screen import Screen
from modules.grid import Grid

class Render():
    def render(self) -> None:
        self.screen.surface.fill("black")

        self.grid.render()
        self.updateFps()
        self.updateParticleCounter()
        self.updateParticleMass()

        pygame.display.flip()

    def updateFps(self) -> None:
        fps = str(int(self.clock.get_fps()))
        fps_text = FONT.render(f"Fps: {fps}", 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, fps_text, (10,0))

    def updateParticleCounter(self) -> None:
        particleText = FONT.render(f"Particles: {str(round(self.grid.particleCounter, 4))}", 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, particleText, (80,0))

    def updateParticleMass(self) -> None:
        particleText = FONT.render(f"Mass: {str((round(self.grid.matrix.sum(), 4)))}", 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, particleText, (200,0))

class Logic():
    def logic(self) -> None:
        self.controlsKeyboard()
        self.controlsMouse()

        self.grid.logic()

    def controlsKeyboard(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True

        if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
            self.exit = True
        if pygame.key.get_pressed()[pygame.K_r] == True:
            self.grid.reset()

    def controlsMouse(self) -> None:
        if pygame.mouse.get_pressed()[0]:
            self.grid.addParticle(pygame.mouse.get_pos())
        if pygame.mouse.get_pressed()[2]:
            self.grid.addWall(pygame.mouse.get_pos())

class Tests():
    def testRun(self, test=False) -> None:
        if test:
            self.avgFps += self.clock.get_fps() 
            self.testCounter += 1
            
            self.grid.addParticle((500,500))
            if self.testCounter > 1000:
                self.avgFps = self.avgFps//self.testCounter
                self.kill()

    def kill(self) -> None:
        self.exit = True

class Game(Render, Logic, Tests):
    def __init__(self, testRun: bool=False) -> None:
        self.screen = Screen()
        self.grid = Grid(self.screen.surface)

        self.fps = 200
        self.avgFps = self.fps
        self.clock = pygame.time.Clock()

        self.isTestRun = testRun
        self.testCounter = 0
        self.exit = False

    def run(self) -> int:
        while not self.exit:
            self.clock.tick(self.fps)
            self.testRun(self.isTestRun)

            self.logic()
            self.render()

        return self.avgFps
