import pygame
from random import randint, random
from modules import WIDTH, HEIGHT

class Balls():
    def __init__(self):
        self.ballCount = 0
        self.balls = []

    def createBallsRandom(self, amount):
        for i in range(amount):
            self.createBall()
            ball = self.balls[i]
            ball.position = ball.vec(randint(10,400), randint(10, 400))
            ball.velocity = ball.vec(random(), random())
            ball.acceleration = ball.vec(random(), random())
            ball.direction = ball.vec(-random(), random())

    def createBalls(self, amount=1):
        for _ in range(amount):
            self.createBall()

    def createBall(self):
        self.balls.append(Ball())
        self.ballCount += 1

    def clearBalls(self):
        self.balls.clear()
        self.ballCount = 0

    def render(self, surface):
        for ball in self.balls:
            ball.render(surface)

class Ball(Balls):
    def __init__(self):
        self.vec = pygame.math.Vector2 
        self.color = "red"

        self.radius = 3
        self.position = self.vec(0, 0)
        self.direction = self.vec(0, 0)
        self.velocity = self.vec(0,0)
        self.acceleration = self.vec(0, 0)

    def render(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)
