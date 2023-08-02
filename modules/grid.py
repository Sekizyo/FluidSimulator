import pygame

from modules import BLOCKSIZE, WIDTHBLOCKS, HEIGHTBLOCKS, DEPTH, PARTICLESPERCLICK

class Position():
    def checkBounds(self, pos):
        x, y = pos
        if (0 <= x < WIDTHBLOCKS) and (0 <= y < HEIGHTBLOCKS):
            return True
        return False

    def getGridPosFromPos(self, pos):
        x, y = pos
        return x//BLOCKSIZE, y//BLOCKSIZE

class Moves(Position):
    def getMoves(self, x, y, depth=1):
        moves = []
        startPosX, startPosY = x, y

        for x in range(-depth,depth+1):
            Y = int((depth*depth-x*x)**0.5)
            for y in range(-Y,Y+1):
                
                x1 = x+startPosX
                y1 = y+startPosY

                if (0 <= x1 < WIDTHBLOCKS) and (0 <= y1 < HEIGHTBLOCKS) and self.blocks != -1:
                    moves.append((x1, y1))
        return moves
    
    def getValuesFromPos(self, pos):
        values = []
        for x, y in pos:
            val = self.blocks[y][x]
            if val >= 0:
                values.append(self.blocks[y][x])
        return values
    
    def getAverageForList(self, list):
        return sum(list) / len(list)    

class Diffusion(Moves):
    def updateBlock(self, block, x, y):
        if block >= 1:
            neighboursPos = self.getMoves(x, y, DEPTH)
            values = self.getValuesFromPos(neighboursPos)
            avg = self.getAverageForList(values)
            for x, y in neighboursPos:

                if self.blocks[y][x] != -1:
                    self.blocks[y][x] = avg

    def update(self, blocks):
        for y, col in enumerate(blocks):
            for x, block in enumerate(col):
                self.updateBlock(block, x, y)

class Render():
    def getColor(self, nparticles):
        delta = nparticles
        if delta > 255: 
            return [255, 255, 255]
        else:
            return [delta, delta, delta]
        
    def render(self, blockRect, blocks):
        for y, col in enumerate(blockRect):
            for x, rect in enumerate(col):
                nparticles = blocks[y][x]
                if nparticles >= 0:
                    color = self.getColor(nparticles)
                    pygame.draw.rect(self.surface, color, rect)
                else:
                    pygame.draw.rect(self.surface, [255, 0, 0], rect)

class Grid(Render, Diffusion):
    def __init__(self, surface):
        self.surface = surface
        self.size = BLOCKSIZE

        self.blocks = []
        self.blockRect = []
        
        self.particleCount = 0
        self.createBlocks()

    def createBlocks(self):
        for y in range(HEIGHTBLOCKS):
            tempX = []
            tempXRect = []
            for x in range(WIDTHBLOCKS):
                tempX.append(0)
                tempXRect.append(pygame.Rect(x*self.size, y*self.size, self.size, self.size))
                
            self.blocks.append(tempX)
            self.blockRect.append(tempXRect)

    def addParticle(self, mouse):
        x, y = self.getGridPosFromPos(mouse)
        self.blocks[y][x] += PARTICLESPERCLICK
        self.particleCount += PARTICLESPERCLICK

    def addWall(self, mouse):
        x, y = self.getGridPosFromPos(mouse)
        self.blocks[y][x] = -1

    def renderGrid(self):
        self.render(self.blockRect, self.blocks)

    def loop(self):
        self.update(self.blocks)

    def reset(self):
        self.blocks = []
        self.blockRect = []
        self.particleCount = 0

        self.createBlocks()