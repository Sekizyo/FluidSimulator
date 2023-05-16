import pygame
from random import random, randrange
from modules import STRESTEST, BLOCKSIZE, WIDTHBLOCKS, HEIGHTBLOCKS

class Particles():
    def __init__(self):
        self.particleCount = 0
        self.particles = []
        self.create()

    def create(self, amount=1):
        self.particleCount += amount

        for i in range(amount):
            gridPos = [randrange(0,WIDTHBLOCKS), randrange(0,HEIGHTBLOCKS)]

            particle = Particle(len(self.particles)+1, gridPos)

            self.particles.append(particle)
    
    def createAtPos(self, pos):
        x, y = pos
        gridPos = [x//BLOCKSIZE, y//BLOCKSIZE]
        particle = Particle(len(self.particles)+1, gridPos)

        self.particleCount += 1
        self.particles.append(particle)

    def reset(self):
        self.particleCount = 0
        self.particles = []
        self.create(1)

class Particle(pygame.sprite.Sprite):
    def __init__(self, id, gridPos, direction=[0,1], vel=1):
        super().__init__()
        self.id = id

        self.gridPos = gridPos
        self.direction = direction
        self.vel = 1
