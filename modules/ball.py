import pygame
from random import randint, random
from modules import WIDTH, HEIGHT

class Balls():
    def __init__(self):
        self.ballCount = 0
        self.balls = []

    # def createBallsRandom(self, amount):
    #     for i in range(amount):
    #         self.createBall()
    #         self.balls[i].x = 100
    #         self.balls[i].y = 100
    #         self.balls[i].speed = 1
    #         self.balls[i].direction = [0.25, 0]

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
        self.x = 100
        self.y = 100
        self.radius = 5

        self.position = self.vec(100, 100)
        self.direction = self.vec(0, 0)
        self.velocity = self.vec(0,0)
        self.acceleration = self.vec(0, 0)

        self.mass = self.radius*1.25
        self._speedLimit = 10
        self.color = "red"

    def setDirection(self, x=0, y=0):

        newX = self.direction[0] + x
        newY = self.direction[1] + y
        
        if newX > 1:
            newX = 1
        if newX < -1:
            newX = -1

        if newY > 1:
            newY = 1
        if newY < -1:
            newY = -1
        
        self.direction = [newX, newY]
        

    def changeSpeed(self, amount=0):
        newSpeed = self.speed + amount
        if newSpeed > self._speedLimit:
            self.speed = self._speedLimit
        elif newSpeed < 0:
            self.speed = 0
        else:
            self.speed = newSpeed

    def moveBy(self, x=0, y=0):
        self.moveTo(self.x+x, self.y+y)
        
    def moveTo(self, x, y):
        self.x = x
        self.y = y

    def render(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)
