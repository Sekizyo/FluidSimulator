
import pygame
from modules.__config__ import FONT, MAXFPS
from modules.screen import Screen
from modules.matrix import Matrix

class Render():
    def render(self) -> None:
        self.screen.surface.fill("black")

        self.matrix.render()
        self.updateFps()
        self.updateParticleCounter()

        pygame.display.flip()

    def updateFps(self) -> None:
        fps = str(int(self.clock.get_fps()))
        fps_text = FONT.render(f"Fps: {fps}", 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, fps_text, (10,0))

    def updateParticleCounter(self) -> None:
        particleText = FONT.render(f"Particles: {str(round(self.matrix.particleCounter, 4))}", 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, particleText, (80,0))

class Logic():
    def logic(self) -> None:
        self.controlsKeyboard()
        self.controlsMouse()

        self.matrix.logic()

    def controlsKeyboard(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.exit = True
        if pygame.key.get_pressed()[pygame.K_r]:
            self.matrix.reset()

    def controlsMouse(self) -> None:
        if pygame.mouse.get_pressed()[0]:
            self.matrix.addParticle(pygame.mouse.get_pos())

class Tests():
    def testRun(self, test=False) -> None:
        if test:
            self.avgFps += self.clock.get_fps() 
            self.testCounter += 1
            
            self.matrix.addParticle((500,500))
            if self.testCounter > 1000:
                self.avgFps = self.avgFps//self.testCounter
                self.kill()

    def kill(self) -> None:
        self.exit = True

class Game(Render, Logic, Tests):
    def __init__(self, testRun: bool=False) -> None:
        self.screen = Screen()
        self.matrix = Matrix(self.screen.surface)

        self.fps = MAXFPS
        self.clock = pygame.time.Clock()
        self.exit = False

        self.isTestRun = testRun
        self.avgFps = self.fps
        self.testCounter = 0

    def run(self) -> int:
        while not self.exit:
            self.clock.tick(self.fps)
            self.testRun(self.isTestRun)

            self.logic()
            self.render()

        return self.avgFps
