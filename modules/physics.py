import pygame
from modules import WIDTH, HEIGHT

class Physics():
    def __init__(self):
        self.vec = pygame.math.Vector2 
        self.gravityForce = 0.1
        self.gravityVector = self.vec(0, self.gravityForce)
        self.reflectionSlowDown = 2.1
        self.acceleration = 0.5
        self.frictionForce = -0.12
    
    def gravityForBalls(self, balls):
        for ball in balls.balls:
            self.gravity(ball)

    def gravity(self, ball):
        self.calcMovement(ball)
        self.checkBoundries(ball)

    def calcMovement(self, ball):
        ball.acceleration = ball.vec(ball.direction.x, self.gravityForce)
        ball.acceleration.x += ball.velocity.x * self.frictionForce

        ball.velocity += ball.acceleration
        ball.position += ball.velocity + 0.5 * ball.acceleration

    def checkBoundries(self, ball):
        if ball.position.x > WIDTH:
            ball.position.x = WIDTH
            self.colisionX(ball)

        if ball.position.x < 0:
            ball.position.x = 0
            self.colisionX(ball)

        if ball.position.y > WIDTH:
            ball.position.y = WIDTH
            self.colisionY(ball)

        if ball.position.y < 0:
            ball.position.y = 0
            self.colisionY(ball)

    def colisionX(self, ball):
            self.setVelocityX(ball, True)
            self.setDirectionX(ball, True)

    def colisionY(self, ball):
            self.setVelocityX(ball, False)
            self.setVelocityY(ball, True)
            self.setDirectionX(ball, False)

    def setVelocityX(self, ball, reflect=True):
        if reflect:
           ball.velocity.x = -(ball.velocity.x/self.reflectionSlowDown)
        else:
           ball.velocity.x = (ball.velocity.x/self.reflectionSlowDown)

    def setVelocityY(self, ball, reflect=True):
        if reflect:
           ball.velocity.y = -(ball.velocity.y/self.reflectionSlowDown)
        else:
           ball.velocity.y = (ball.velocity.y/self.reflectionSlowDown)
        
    def setDirectionX(self, ball, reflect=True):
        if reflect:
           ball.direction.x = -(ball.direction.x/self.reflectionSlowDown)
        else:
           ball.direction.x = (ball.direction.x/self.reflectionSlowDown)
        