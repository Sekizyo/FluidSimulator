import pygame
from random import randrange
from modules import BLOCKSIZE, WIDTHBLOCKS, HEIGHTBLOCKS

class Particles():
    def __init__(self):
        self.particleCount = 0
        self.particles = []

    def create(self, amount):
        self.particleCount += 1

        for i in range(amount):
            gridPos = [randrange(0,WIDTHBLOCKS), randrange(0,2)]
            dir = [randrange(-1, 1), randrange(-1, 1)]

            particle = Particle(len(self.particles)+1, gridPos)

            self.particles.append(particle)

class Particle(pygame.sprite.Sprite):
    def __init__(self, id, gridPos, dir=[0,1], vel=1):
        super().__init__()
        self.id = id

        self.gridPos = gridPos
        self.dir = dir
        self.vel = 1

    def move(self):
        self.gridPos[0] += int(self.dir[0] * self.vel)
        self.gridPos[1] += int(self.dir[1] * self.vel)
