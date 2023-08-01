import pygame
import numpy
from math import dist

from modules import BLOCKSIZE, WIDTHBLOCKS, HEIGHTBLOCKS, FONT

class Position():
    def checkBounds(self, pos):
        x, y = pos
        if (0 <= x < WIDTHBLOCKS) and (0 <= y < HEIGHTBLOCKS):
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

        for x in range(-depth,depth+1):
            Y = int((depth*depth-x*x)**0.5)
            for y in range(-Y,Y+1):
                
                x1 = x+startPosX
                y1 = y+startPosY

                if (0 <= x1 < WIDTHBLOCKS) and (0 <= y1 < HEIGHTBLOCKS):
                    moves.append(self.blocks[y1][x1])
        return moves

class Diffusion(Moves):
    def update(self, blocks):
        for y, col in enumerate(blocks):
            for x, block in enumerate(col):
                if block >= 1:
                    neighbours = self.getMoves((x, y), 2)
                    avg = self.getAverageForBlocks(neighbours)
                    if avg >= block:
                        for neighbour in neighbours:
                            neighbour = avg

    def getAverageForBlocks(self, blocks):
        avg = 0
        for block in blocks:
            avg += block
        return avg / len(blocks)           

class Render():
    def render(self, blockRect, blocks):
        for y, col in enumerate(blockRect):
            for x, rect in enumerate(col):
                nparticles = blocks[y][x]
                color = self.getColor(nparticles)
                print(rect)
                pygame.draw.rect(self.surface, color, rect)

    def getColor(self, nparticles):
        return [100, 100, 100]

class Grid(Render, Diffusion):
    def __init__(self, surface):
        self.blocks = numpy.arange(WIDTHBLOCKS*HEIGHTBLOCKS).reshape(HEIGHTBLOCKS, WIDTHBLOCKS)
        self.blockRect = numpy.arange(WIDTHBLOCKS*HEIGHTBLOCKS).reshape(HEIGHTBLOCKS, WIDTHBLOCKS)
        self.surface = surface
        self.particleCount = 0
        self.size = BLOCKSIZE
        self.createBlocks()

    def addParticleToBlockByPos(self, mouse):
        gridPos = self.getGridPosFromPos(mouse)
        block = self.getBlockByGridPos(gridPos)
        block.particles += 10000
        self.particleCount += 10000

    def createBlocks(self):
        tempY = []
        tempYRect = []
        for y in range(HEIGHTBLOCKS):
            tempX = []
            tempXRect = []
            for x in range(WIDTHBLOCKS):
                tempX.append(0)
                tempXRect.append(pygame.Rect(x*self.size, y*self.size, self.size, self.size))
            tempY.append(tempX)
            tempYRect.append(tempXRect)

        self.blocks = tempY
        self.blocksRect = tempYRect

    def renderGrid(self):
        self.render(self.blockRect, self.blocks)

    def loop(self):
        self.update(self.blocks)

    def reset(self):
        self.particleCount = 0
        for col in self.blocks:
            col = []
