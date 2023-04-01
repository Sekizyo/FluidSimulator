import pygame
from modules import WIDTH, HEIGHT

class Balls():
    def __init__(self):
        self.ballCount = 0
        self.balls = []

    def createBalls(self, count):
        for _ in range(count):
            createBall()

    def createBall(self):
        self.balls.append(Ball())

    def draw(self):
        for ball in balls():
            ball.draw()

class Ball():
    def __init__(self):
        self.x = 0
        self.y = 0
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


    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
