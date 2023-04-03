
import pygame
from modules.screen import Screen
from modules.ball import Balls
from modules.physics import Physics

class Game():
    def __init__(self):
        self.screen = Screen()
        self.physics = Physics()
        self.balls = Balls()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18)
        self.exit = False
    
    def controls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
            if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
                self.exit = True
            if pygame.key.get_pressed()[pygame.K_1] == True:
                self.balls.clearBalls()
                self.balls.createBallsRandom(10)

    def updateFps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps, 1, pygame.Color("coral"))
        pygame.Surface.blit(self.screen.surface, fps_text, (10,0))

    def render(self):
        self.screen.surface.fill("black")
        self.updateFps()
        self.balls.render(self.screen.surface)
        pygame.display.update()

    def run(self):
        self.balls.createBallsRandom(10000)
        while not self.exit:
            self.clock.tick(60)
            self.controls()
            self.physics.gravityForBalls(self.balls)
            self.render()