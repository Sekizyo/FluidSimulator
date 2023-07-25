import pygame
import numpy as np
from math import dist

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
        
class Moves(Position):
    def getMoves(self, pos, depth=1):
        moves = []
        startPosX, startPosY = pos

        X = int(depth)
        for x in range(-X,X+1):
            Y = int((depth*depth-x*x)**0.5)
            for y in range(-Y,Y+1):
                if self.checkBounds((x+startPosX, y+startPosY)):
                    moves.append(self.blocks[y+startPosY][x+startPosX])
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

class Diffusion(Moves):
    def update(self, blocks):
        for col in blocks:
            for block in col:
                if block.particles >= 1:
                    neighbours = self.getMoves(block.gridPos, 2)
                    avg = self.getAverageForBlocks(neighbours)
                    if avg >= 1:
                        for neighbour in neighbours:
                            neighbour.particles = avg

    def getAverageForBlocks(self, blocks):
        avg = 0
        for block in blocks:
            avg += block.particles
        return avg / len(blocks)           

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
                    idText = FONT.render(str(block.gridPos), 1, block.color)
                    pygame.Surface.blit(self.surface, idText, (block.rect[0]+(block.size//4), block.rect[1]+(block.size//2-10)))
                    
                    particlesText = FONT.render(str(round(block.particles, 2)), 1, block.color)
                    pygame.Surface.blit(self.surface, particlesText, (block.rect[0]+(block.size//4), block.rect[1]+(block.size//2-10)))
                else:
                    block.updateColor()
                    pygame.draw.rect(self.surface, block.color, block.rect)

class Grid(Render, Diffusion):
    def __init__(self, surface):
        self.blocks = np.arange(WIDTHBLOCKS*HEIGHTBLOCKS).reshape(HEIGHTBLOCKS, WIDTHBLOCKS)
        self.renderDebug = False
        self.surface = surface
        self.particleCount = 0
        self.createBlocks()

    def addParticleToBlockByPos(self, mouse):
        gridPos = self.getGridPosFromPos(mouse)
        block = self.getBlockByGridPos(gridPos)
        block.particles += 10000
        self.particleCount += 10000

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
                block.color = [0,0,0]
                
class Block():
    def __init__(self, x=0, y=0, size=1, direction = [0, 1]):
        self.gridPos = (x, y)
        self.rect = pygame.Rect(x*size, y*size, size, size)
        self.color = [0,0,0]
        self.size = size
        self.particles = 0
        self.maxParticles = 255

    def updateColor(self):
        delta = self.particles
        if delta < 255: 
            self.color = [delta, delta, delta]
