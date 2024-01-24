
import pygame

from modules.__config__ import MAXFPS
from modules.screen import Screen
from modules.matrix import Matrix

class Render():
    def __init__(self) -> None:
        super(Render, self).__init__()
        self.font = pygame.font.SysFont("Arial", 18)
        self.paused = False
        self.hudHidden = False

    def render(self) -> None:
        self.screen.surface.fill("black")

        self.matrix.render()
        if not self.hudHidden:
            self.updateFps()
            self.updateParticleCounter()
            self.updatePressureCoeff()
            self.updateVelocityCoeff()
            self.updatePauseNotification()

        pygame.display.flip()

    def updateFps(self) -> None:
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(f"Fps: {fps}", 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, fps_text, (10,0))

    def updateParticleCounter(self) -> None:
        particles = str(self.matrix.particleCounter)
        particleText = self.font.render(f"Particles: {particles}", 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, particleText, (80,0))

    def updatePressureCoeff(self) -> None:
        pressure = str(round(self.matrix.pressureCoeff, 1))
        pressureText = self.font.render(f"PressureCoeff: {pressure}", 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, pressureText, (10, 50))

    def updateVelocityCoeff(self) -> None:
        velocity = str(round(self.matrix.velocityCoeff, 1))
        velocityText = self.font.render(f"VelocityCoeff: {velocity}", 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, velocityText, (10, 75))
    
    def updatePauseNotification(self) -> None:
        particleText = self.font.render(f"Pause: {self.paused}", 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, particleText, (10,25))

class Logic():
    def update(self) -> None:
        self.controlsKeyboard()
        self.controlsMouse()
        if not self.paused:
            self.matrix.update()

    def controlsKeyboard(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit = True
                
                if event.key == pygame.K_r:
                    self.matrix.reset()
                
                if event.key == pygame.K_i:
                    self.hudHidden = not self.hudHidden

                if event.key == pygame.K_p:
                    self.paused = not self.paused

                if event.key == pygame.K_w:
                    self.matrix.isRain = not self.matrix.isRain

                if event.key == pygame.K_t:
                    self.matrix.increaseVelocityCoeff()

                if event.key == pygame.K_g:
                    self.matrix.decreaseVelocityCoeff()

                if event.key == pygame.K_y:
                    self.matrix.increasePreassureCoeff()

                if event.key == pygame.K_h:
                    self.matrix.decreasePreassureCoeff()

    def controlsMouse(self) -> None:
        if pygame.mouse.get_pressed()[0]:
            self.matrix.addParticle(pygame.mouse.get_pos())

class Test():
    def __init__(self):
        super(Test, self).__init__()
        self.avgFps = 0
        self.testCounter = 0

    def runTest(self) -> None:
        if self.isTestRun:
            self.avgFps += self.clock.get_fps() 
            self.testCounter += 1
            
            self.matrix.addParticle((500,500))
            if self.testCounter > 1000:
                self.avgFps = self.avgFps//self.testCounter
                self.kill()

    def kill(self) -> None:
        self.exit = True

class Engine(Render, Logic, Test):
    def __init__(self, isTestRun: bool=False) -> None:
        super(Engine, self).__init__()
        self.screen = Screen()
        self.matrix = Matrix(self.screen.surface)

        self.fps = MAXFPS
        self.clock = pygame.time.Clock()
        self.isTestRun = isTestRun
        self.exit = False

    def run(self) -> int:
        while not self.exit:
            self.clock.tick(self.fps)
            self.runTest()

            self.update()
            self.render()

        return self.avgFps
