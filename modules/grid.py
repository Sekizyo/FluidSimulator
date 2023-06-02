import pygame
from random import random, randrange
import numpy as np
import math

from random import randint
from modules import BLOCKSIZE, WIDTHBLOCKS, HEIGHTBLOCKS, FONT

class Position():
    def checkBounds(self, pos):
        x, y = pos
        if (0 <= x <= WIDTHBLOCKS-1) and (0 <= y <= HEIGHTBLOCKS-1):
            return True
        return False

    def getGridPosFromPos(self, pos):
        x, y = pos
        return x//BLOCKSIZE, y//BLOCKSIZE

    def getBlockByGridPos(self, pos, blocks):
        if self.checkBounds(pos):
            x, y = pos
            return blocks[y][x]
        else:
            return None

    def getDistance(self, objA, objB):
        return math.dist(objA, objB)

class Moves(Position):
    def createMoves(self, block, blocks, depth=1, excludeOccupied=True):
        moves = []
        neighbours = self.getMoves(block.gridPos, depth)

        for neighbour in neighbours:
            if self.checkBounds(neighbour):
                if self.checkIfOccupied(neighbour, blocks, excludeOccupied): 
                    moves.append(neighbour)
                else:
                    moves.append(neighbour)

        return moves

    def getMoves(self, pos, depth=1):
        moves = []
        startPosX, startPosY = pos

        X = int(depth)
        for x in range(-X,X+1):
            Y = int((depth*depth-x*x)**0.5)
            for y in range(-Y,Y+1):
                moves.append([x+startPosX, y+startPosY])
        return moves

    def checkIfOccupied(self, pos, blocks, excludeOccupied=True):
        x, y = pos
        if excludeOccupied and blocks[y][x].particleID == None:
            return True
        else:
            return False

class Direction(Moves):
    def normalize(self, value):
        if value >= 1:
            value = 1
        elif 0 <= value < 1:
            value = 0
        elif -1 <= value < 0:
            value = -1
        elif -1 > value:
            value = -1

        return value

    def refreshBlockAssigment(self, blocks):
        for col in blocks:
            for block in col:
                block.particleID = None

    def refreshBlockDir(self, blocks):
        for col in blocks:
            for block in col:
                block.direction = [0,1]

    def changeBlockDirections(self, mouse):
        gridPos = self.getGridPosFromPos(mouse)
        block = self.getBlockByGridPos(gridPos)
        self.changeBlocksDirectionsInRadius(block)

    def changeBlocksDirectionsInRadius(self, center, blocks, radius = 3):
        moves = self.createMoves(center, blocks, radius, False)
        for gridPos in moves:
            self.changeBlockDirection(gridPos, center, blocks)

    def changeBlockDirection(self, gridPos, center, blocks, possitive=True):
        block = self.getBlockByGridPos(gridPos, blocks)
        
        blockX, blockY = block.gridPos
        centerX, centerY = center.gridPos
        if possitive:
            dirX = blockX - centerX
            dirY = blockY - centerY
        else:
            dirX = centerX - blockX
            dirY = centerY - blockY
            
        block.direction[0] = self.normalize(block.direction[0] + dirX)
        block.direction[1] = self.normalize(block.direction[1] + dirY)

class Particle(pygame.sprite.Sprite):
    def __init__(self, id, gridPos, direction=[0,1], vel=1):
        super().__init__()
        self.id = id

        self.gridPos = gridPos
        self.direction = direction
        self.vel = 1

class Particles(Direction):
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

    def reset(self, blocks):
        self.particleCount = 0
        self.particles = []
        self.refreshBlockDir(blocks)
        self.create(1)

    def moveParticles(self, blocks):
        self.refreshBlockAssigment(blocks)
        for particle in self.particles:
            moves = self.createMoves(particle, blocks, 1, True)
            self.moveParticle(particle, moves, blocks)

    def moveParticle(self, particle, moves, blocks):
        positionStart = particle.gridPos
        block = self.getBlockByGridPos(positionStart, blocks)
        position = [positionStart[0] + block.direction[0], positionStart[1] + block.direction[1]]
        if self.checkBounds(position):
            if position in moves:
                self.assignParticleToBlockByPos(particle, position, blocks)
                self.changeBlocksDirectionsInRadius(block, blocks)
        else:
            self.assignParticleToBlockByPos(particle, positionStart, blocks)
            self.changeBlocksDirectionsInRadius(block, blocks)

    def assignParticleToBlockByPos(self, particle, position, blocks):
        particle.gridPos = position
        block = self.getBlockByGridPos(position, blocks)
        block.particleID = particle.id

class Render():
    def __init__(self, surface):
        self.renderDebug = True
        self.surface = surface

    def switchRenderDebug(self):
        if self.renderDebug == True:
            self.renderDebug = False
        elif self.renderDebug == False:
            self.renderDebug = True

    def render(self, blocks):
        for col in blocks:
            for block in col:
                if block.particleID:
                    pygame.draw.rect(self.surface, (100,100,100), block.rect, 0)
                
                if self.renderDebug:
                    pygame.draw.rect(self.surface, block.color, block.rect, 1)
                
                    startPos, endPos = self.getPressureArrowVector(block)
                    pygame.draw.line(self.surface, block.color, startPos, endPos, 1)

                    idText = FONT.render(str(block.gridPos), 1, block.color)
                    pygame.Surface.blit(self.surface, idText, (block.rect[0]+(block.size//4), block.rect[1]+(block.size//2-10)))
   
    def getPressureArrowVector(self, block):
        startPos = [block.rect[0] + block.size//2 , block.rect[1] + block.size//2]
        
        direction = block.direction
        strenght = block.pressureStrenght

        endPos = [startPos[0]+(direction[0]*strenght) , startPos[1]+(direction[1]*strenght)]

        return startPos, endPos

class Grid():
    def __init__(self, surface):
        self.render = Render(surface)
        self.particles = Particles()
        
        self.blocks = np.arange(WIDTHBLOCKS*HEIGHTBLOCKS).reshape(HEIGHTBLOCKS, WIDTHBLOCKS)
        self.createBlocks()

    def createBlocks(self):
        tempY = []
        for y in range(HEIGHTBLOCKS):
            tempX = []
            for x in range(WIDTHBLOCKS):
                block = Block(x, y, BLOCKSIZE)
                tempX.append(block)
            tempY.append(tempX)
        self.blocks = tempY

    def renderGrid(self):
        self.render.render(self.blocks)

    def reset(self):
        self.particles.reset(self.blocks)

    def loop(self):
        self.particles.moveParticles(self.blocks)

class Block():
    def __init__(self, x=0, y=0, size=1, direction = [0, 1]):
        self.gridPos = (x, y)
        self.rect = pygame.Rect(x*size, y*size, size, size)
        self.color = (255,255,255)
        self.size = size
        self.particleID = None
        self.direction = direction
        self.pressureStrenght = 10