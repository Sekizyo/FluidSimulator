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

    def getBlockByGridPos(self, pos):
        if self.checkBounds(pos):
            x, y = pos
            return self.blocks[y][x]
        else:
            return None
        
    def getBlockByGridPos1(self, pos):
        if self.checkBounds(pos):
            x, y = pos
            return self.blocks[y][x]
        else:
            return None

    def getDistance(self, objA, objB):
        return math.dist(objA, objB)

class Moves(Position):
    def createMoves(self, block, depth=1):
        moves = []
        neighbours = self.getMoves(block.gridPos, depth)

        for neighbour in neighbours:
            if self.checkBounds(neighbour):
                moves.append(neighbour)

        return moves
    
    def getBlocksFromMoves(self, moves):
        blocks = []
        for move in moves:
            blocks.append(self.getBlockByGridPos(move))
        return blocks

    def getMoves(self, pos, depth=1):
        moves = []
        startPosX, startPosY = pos

        X = int(depth)
        for x in range(-X,X+1):
            Y = int((depth*depth-x*x)**0.5)
            for y in range(-Y,Y+1):
                moves.append([x+startPosX, y+startPosY])
        return moves

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
        moves = self.createMoves(center, radius, False)
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

class Particles(Direction):
    def __init__(self):
        self.particleCount = 0
        self.particles = []

    def reset(self, blocks):
        self.particleCount = 0
        self.particles = []
        self.refreshBlockDir(blocks)

class Diffusion(Moves):
    def update(self, blocks):
        for col in blocks:
            for block in col:
                if block.particles:
                    neighboursGridPos = self.createMoves(block)
                    neighbours = self.getBlocksFromMoves(neighboursGridPos)
                    avg = self.getAverageForBlocks(neighbours)
                    block.particles = avg
                    for i, neighbour in enumerate(neighbours):
                        neighbour.particles = avg

    def getTotalMass(self):
        mass = 0
        for col in self.blocks:
            for block in col:
                mass += block.particles
        
        return mass

    def getAverageForBlocks(self, blocks):
        avg = 0
        for block in blocks:
            avg += block.particles
        return avg / len(blocks)           

    def sortNeighboursByParticleCount(self, list):
        blocks = self.getBlocksFromMoves(list)
        blocks.sort(key=lambda x: x.particles)
        return blocks
    
class Render():
    def switchRenderDebug(self):
        if self.renderDebug == True:
            self.renderDebug = False
        elif self.renderDebug == False:
            self.renderDebug = True

    def render(self, blocks):
        for col in blocks:
            for block in col:
                if self.renderDebug:
                    block.updateColor()
                    # pygame.draw.rect(self.surface, block.color, block.rect, 1)
                
                    # idText = FONT.render(str(block.gridPos), 1, block.color)
                    # pygame.Surface.blit(self.surface, idText, (block.rect[0]+(block.size//4), block.rect[1]+(block.size//2-10)))
                    
                    particlesText = FONT.render(str(block.particles), 1, block.color)
                    pygame.Surface.blit(self.surface, particlesText, (block.rect[0]+(block.size//4), block.rect[1]+(block.size//2-10)))
   
class Grid(Render, Diffusion, Particles):
    def __init__(self, surface):
        self.blocks = np.arange(WIDTHBLOCKS*HEIGHTBLOCKS).reshape(HEIGHTBLOCKS, WIDTHBLOCKS)
        self.renderDebug = True
        self.surface = surface
        self.particleCount = 0
        self.createBlocks()

    def addParticleToBlockByPos(self, mouse):
        gridPos = self.getGridPosFromPos(mouse)
        block = self.getBlockByGridPos(gridPos)
        block.particles += 1
        self.particleCount += 1

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
        self.render(self.blocks)

    def loop(self):
        self.update(self.blocks)

    def reset(self):
        self.particleCount = 0
        for col in self.blocks:
            for block in col:
                block.particles = 0
class Block():
    def __init__(self, x=0, y=0, size=1, direction = [0, 1]):
        self.gridPos = (x, y)
        self.rect = pygame.Rect(x*size, y*size, size, size)
        self.color = [255,255,255]
        self.size = size
        self.particles = 0
        self.maxParticles = 255

    def updateColor(self):
        delta = self.color[0]-self.particles
        if delta > 0: 
            self.color[0] = delta
