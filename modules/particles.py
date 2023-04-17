import pygame
from random import randint, random, randrange
from modules import WIDTH, HEIGHT

class Particles():
    def __init__(self):
        self.particleCount = 0
        self.particles = pygame.sprite.Group()
        self.grid = []

    def create(self, amount, rectArea):
        self.particleCount += 1
        hue = randrange(360)
        radius, velocity = 5, 1
        pos_rect = rectArea.inflate(-radius * 2, -radius * 2)
        for i in range(amount):
            x = randrange(pos_rect.left, pos_rect.right)
            y = randrange(pos_rect.top, pos_rect.bottom)
            dir = pygame.math.Vector2(1, 0).rotate(randrange(360))
            particle = Particle(len(self.particles)+1, hue, (x, y), radius, dir, velocity)
            self.particles.add(particle)

    def draw(self, surface):
        self.particles.draw(surface)

    def update(self, rectArea):
        self.particles.update(rectArea)
    def render(self, rectArea):
        self.particles.update(rectArea)

class Particle(pygame.sprite.Sprite):
    def __init__(self,id, hue, pos, radius, dir, vel):
        super().__init__()
        self.id = id
        self.pos = pygame.math.Vector2(pos)
        self.gridPos = (self.pos.x, self.pos.y)
        self.dir = pygame.math.Vector2(dir)
        self.vel = vel
        self.radius = radius
        self.rect = pygame.Rect(self.gridPos[0], self.gridPos[1], radius*2, radius*2)
        self.image = pygame.Surface((radius*2, radius*2))
        self.changeColor(hue)

    def changeColor(self, hue):
        self.hue = hue
        self.color = pygame.Color(0)
        self.color.hsla = (self.hue, 100, 50, 100)
        self.image.set_colorkey((0, 0, 0))
        self.image.fill(0)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)

    def move(self):
        self.pos += self.dir * self.vel

    def render(self, surface):
        self.rect = pygame.Rect(self.gridPos[0], self.gridPos[1], self.radius*2, self.radius*2)
        pygame.draw.rect(surface, self.color, self.rect, 1)
