
import pygame
from modules.screen import Screen
from modules.ball import Balls
from modules.physics import Physics

class Game():
    def __init__(self):
        self.screen = Screen()
        self.physics = Physics()
        self.balls = Balls()
        self.exit = False
    
    def createTestBalls(self, amount=5):
        self.balls.createBallsRandom(amount)

    def controls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
            if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
                self.exit = True

    def render(self):
        self.screen.surface.fill("black")
        self.balls.render(self.screen.surface)
        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()
        self.balls.createBall()
        while not self.exit:
            clock.tick(20)
            self.controls()
            self.physics.gravityForBalls(self.balls)
            self.render()