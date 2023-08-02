import pygame
import numpy
from math import dist
from random import randrange

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
                    moves.append((x1, y1))
        return moves
    
    def getValuesFromPos(self, pos):
        values = []
        for x, y in pos:
            values.append(self.blocks[y][x])
        return values
    
    def getAverageForList(self, list):
        return sum(list) / len(list)    

class Diffusion(Moves):
    def update(self, blocks):
        for y, col in enumerate(blocks):
            for x, block in enumerate(col):
                if block >= 1:
                    neighboursPos = self.getMoves((x, y), 1)
                    values = self.getValuesFromPos(neighboursPos)
                    avg = self.getAverageForList(values)
                    for x, y in neighboursPos:
                        self.blocks[y][x] = avg

class Render():
    def render(self, blockRect, blocks):
        for y, col in enumerate(blockRect):
            for x, rect in enumerate(col):
                nparticles = blocks[y][x]
                color = self.getColor(nparticles)
                pygame.draw.rect(self.surface, color, rect)

    def getColor(self, nparticles):
        delta = nparticles
        if delta > 255: 
            return [255, 255, 255]
        else:
            return [delta, delta, delta]

class Grid(Render, Diffusion):
    def __init__(self, surface):
        self.surface = surface
        self.size = BLOCKSIZE

        self.blocks = []
        self.blockRect = []
        
        self.particleCount = 0
        self.createBlocks()

    def addParticleToBlockByPos(self, mouse):
        x, y = self.getGridPosFromPos(mouse)
        self.blocks[y][x] += 10000
        self.particleCount += 10000

    def createBlocks(self):
        for y in range(HEIGHTBLOCKS):
            tempX = []
            tempXRect = []
            for x in range(WIDTHBLOCKS):
                tempX.append(0)
                tempXRect.append(pygame.Rect(x*self.size, y*self.size, self.size, self.size))
                
            self.blocks.append(tempX)
            self.blockRect.append(tempXRect)

    def renderGrid(self):
        self.render(self.blockRect, self.blocks)

    def loop(self):
        self.update(self.blocks)

    def reset(self):
        self.blocks = []
        self.blocksRect = []

        self.particleCount = 0

        self.createBlocks()
