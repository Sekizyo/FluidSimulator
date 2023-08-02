
import pygame
from modules import FONT
from modules.screen import Screen
from modules.grid import Grid

class Logic():
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
        if pygame.key.get_pressed()[pygame.K_r] == True:
            self.grid.reset()

    def controlsMouse(self):
        if pygame.mouse.get_pressed()[0]:
            self.grid.addParticle(pygame.mouse.get_pos())
        if pygame.mouse.get_pressed()[2]:
            self.grid.addWall(pygame.mouse.get_pos())

class Render():
    def render(self):
        self.screen.surface.fill("black")

        self.grid.renderGrid()
        self.updateFps()
        self.updateParticleCount()

        pygame.display.flip()

    def updateFps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = FONT.render(fps, 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, fps_text, (10,0))

    def updateParticleCount(self):
        particleText = FONT.render(str(self.grid.particleCount), 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, particleText, (50,0))
  
class Game(Logic, Render):
    def __init__(self, testRun=False):
        self.screen = Screen()
        self.grid = Grid(self.screen.surface)

        self.fps = 60
        self.avgFps = self.fps
        self.clock = pygame.time.Clock()

        self.testrun = testRun
        self.testCounter = 0

        self.exit = False

    def run(self):
        while not self.exit:
            self.clock.tick(self.fps)
            self.testRun()

            self.logic()
            self.render()

        return self.avgFps
    
    def testRun(self):
        if self.testrun:
            self.avgFps += self.clock.get_fps() 
            self.testCounter += 1
            self.grid.addParticle((500,500))
            if self.testCounter > 100:
                self.avgFps = self.avgFps//self.testCounter
                self.kill()

    def kill(self):
        self.exit = True
