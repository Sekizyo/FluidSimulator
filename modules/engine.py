
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
            self.updateMatrixMass()
            self.updatePressureCoeff()
            self.updateVelocityCoeff()
            self.updateDecayRate()
            self.updatePauseNotification()

        pygame.display.flip()

    def updateFps(self) -> None:
        fps = str(int(self.clock.get_fps()))
        fpsText = self.font.render(f"Fps: {fps}", 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, fpsText, (10,0))

    def updateParticleCounter(self) -> None:
        particles = str(self.matrix.particleCounter)
        particleText = self.font.render(f"Particles: {particles}", 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, particleText, (80,0))

    def updateMatrixMass(self) -> None:
        mass = str(round(self.matrix.matrix.sum(), 2))
        massText = self.font.render(f"Mass: {mass}", 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, massText, (180,0))

    def updatePressureCoeff(self) -> None:
        pressure = str(round(self.matrix.pressureCoeff, 2))
        pressureText = self.font.render(f"Pressure: {pressure}", 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, pressureText, (10, 50))

    def updateVelocityCoeff(self) -> None:
        velocity = str(round(self.matrix.velocityCoeff, 2))
        velocityText = self.font.render(f"Velocity: {velocity}", 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, velocityText, (10, 75))

    def updateDecayRate(self) -> None:
        rate = str(round(self.matrix.decayRate, 3))
        rateText = self.font.render(f"Decay: {rate}", 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, rateText, (10, 100))
    
    def updatePauseNotification(self) -> None:
        particleText = self.font.render(f"Pause: {self.paused}", 100, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, particleText, (10,125))

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

                if event.key == pygame.K_u:
                    self.matrix.increaseDecayRate()

                if event.key == pygame.K_j:
                    self.matrix.decreaseDecayRate()

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
