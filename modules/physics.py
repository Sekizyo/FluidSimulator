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
            self.checkColisions(ball, balls.balls)
            self.gravity(ball)

    def gravity(self, ball):
        self.checkBoundries(ball)
        self.calcMovement(ball)

    def checkColisions(self, ballMain,  balls):
        for ball in balls:
            if ballMain.id != ball.id:
                ballMain.position = self.vec(round(ballMain.position.x), round(ballMain.position.y))
                ball.position = self.vec(round(ball.position.x), round(ball.position.y))

                if ballMain.position.distance_to(ball.position) < ballMain.radius*2-2:
                    print(f"Colision! between {ballMain.id} and {ball.id}")

                    nv = ball.position-ballMain.position
                    print(f"nv: {nv} ballMD: {ballMain.direction} ND: {ballMain.position.reflect(nv)}")

                    ballMain.direction = ballMain.position.reflect_ip(nv)
                    ball.direction = ball.position.reflect_ip(nv)

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
        