import pygame
from modules import WIDTH, HEIGHT

class Physics():
    def __init__(self):
        self.vec = pygame.math.Vector2 
        self.gravityForce = 0.1
        self.gravityVector = self.vec(0, self.gravityForce)
        self.reflectionSlowDown = 1
        self.acceleration = 0.5
        self.frictionForce = -0.12
    
    def gravityForBalls(self, balls):
        for ball in balls.balls:
            self.gravity(ball)

    def gravity(self, ball):
        ball.acceleration = ball.vec(0, self.gravityForce)
            

        ball.acceleration.x += ball.velocity.x * self.frictionForce

        ball.velocity += ball.acceleration
        ball.position += ball.velocity + 0.5 * ball.acceleration
        
        if ball.position.x > WIDTH:
            ball.position.x = 0
        if ball.position.x < 0:
            ball.position.x = WIDTH

        print(ball.position.y, ball.velocity.y)

        if ball.position.y >= 500:
            ball.velocity.y = -ball.velocity.y + (self.reflectionSlowDown*1.5)


        
        



        