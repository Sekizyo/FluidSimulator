import pygame
from modules import WIDTH, HEIGHT

class Balls():
    def __init__(self):
        self.ballCount = 0
        self.balls = []
        # self.createBall()

    def createBalls(self, count=1):
        for _ in range(count):
            self.createBall()

    def createBall(self):
        self.balls.append(Ball())
        self.ballCount += 1

    def render(self, surface):
        for ball in self.balls:
            ball.render(surface)

class Ball(Balls):
    def __init__(self):
        self.x = 100
        self.y = 100
        self.radius = 1
        self.color = "red"
    
    def moveTo(self, x, y):
        global WIDTH
        global HEIGHT

        if x > WIDTH or y > HEIGHT:
            self.x = WIDTH
            self.y = HEIGHT
        elif x < 0 or y < 0:
            self.x = 0
            self.y = 0
        else:
            self.x = x
            self.y = y


    def render(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
