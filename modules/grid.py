import pygame
from random import randint
from modules import BLOCKSIZE, WIDTHBLOCKS, HEIGHTBLOCKS, FONT

class Grid():
    def __init__(self, surface):
        self.surface = surface

        self.blockSize = BLOCKSIZE
        self.widthBlocks = WIDTHBLOCKS
        self.heightBlocks = HEIGHTBLOCKS
        
        self.renderDebug = True
        self.blocks = []
        self.createBlocks()

    def createBlocks(self):
        tempY = []
        for y in range(self.heightBlocks):
            tempX = []
            for x in range(self.widthBlocks):
                block = Block(x, y, self.blockSize)
                tempX.append(block)
            tempY.append(tempX)
        self.blocks = tempY

    def switchRenderDebug(self):
        if self.renderDebug == True:
            self.renderDebug = False
        elif self.renderDebug == False:
            self.renderDebug = True

    def getPressureArrowVector(self, block):
        startPos = [block.rect[0] + block.size//2 , block.rect[1] + block.size//2]
        
        direction = block.direction
        strenght = 12

        endPos = [startPos[0]+(direction[0]*strenght) , startPos[1]+(direction[1]*strenght)]

        return startPos, endPos

    def render(self):
        for col in self.blocks:
            for block in col:
                if block.particleID:
                    pygame.draw.rect(self.surface, (100,100,100), block.rect, 0)
                
                elif self.renderDebug:
                    pygame.draw.rect(self.surface, block.color, block.rect, 1)
                
                    startPos, endPos = self.getPressureArrowVector(block)
                    pygame.draw.line(self.surface, block.color, startPos, endPos, 1)

                    idText = FONT.render(str(block.gridPos), 1, block.color)
                    pygame.Surface.blit(self.surface, idText, (block.rect[0]+(block.size//2), block.rect[1]+(block.size//2-10)))
                    
                    particleIDText = FONT.render(str(block.particleID), 1, (255,255,255))
                    pygame.Surface.blit(self.surface, particleIDText, (block.rect[0]+(block.size//2), block.rect[1]+(block.size//2+10)))

    def moveParticles(self, particles):
        self.refreshBlock()
        for particle in particles:
            moves = self.createMoves(particle)
            self.moveParticle(particle, moves)

    def refreshBlock(self):
        for col in self.blocks:
            for block in col:
                block.particleID = None
                block.direction = [0,0]

    def createMoves(self, block, depth=1, excludeOccupied=True):
        moves = []
        x, y = block.gridPos
        for i in range(1, depth+1):
            neighbours = [[x-i, y], [x+i, y], [x, y-i], [x, y+i], [x-i, y-i], [x+i, y-i], [x-i, y+i], [x+i, y+i], [x, y]]
            for neighbour in neighbours:
                neiX, neiY = neighbour
                if self.checkBounds(neighbour) and self.blocks[neiY][neiX].particleID == None:
                    moves.append(neighbour)
                elif excludeOccupied == False and self.checkBounds(neighbour):
                    moves.append(neighbour)

        return moves

    def getBlockByGridPos(self, pos):
        if self.checkBounds(pos):
            x, y = pos
            return self.blocks[y][x]
        else:
            return None

    def checkBounds(self, pos):
        x, y = pos
        if (0 <= x <= self.widthBlocks-1) and (0 <= y <= self.heightBlocks-1):
            return True
        return False

    def moveParticle(self, particle, moves):
        positionStart = particle.gridPos
        block = self.getBlockByGridPos(positionStart)
        position = [positionStart[0] + block.direction[0], positionStart[1] + block.direction[1]]
        if self.checkBounds(position):
            if position in moves:
                self.assignParticleToBlockByPos(particle, position)
                self.changeBlocksDirectionsInRadius(block)
        else:
            self.assignParticleToBlockByPos(particle, positionStart)
            self.changeBlocksDirectionsInRadius(block)
            
    def assignParticleToBlockByPos(self, particle, position):
            particle.gridPos = position
            block = self.getBlockByGridPos(position)
            block.particleID = particle.id

    def changeBlockDirections(self, mouse):
        gridPos = self.getGridPosFromPos(mouse)
        block = self.getBlockByGridPos(gridPos)
        self.changeBlocksDirectionsInRadius(block)

    def getGridPosFromPos(self, pos):
        x, y = pos
        return x//self.blockSize, y//self.blockSize

    def changeBlocksDirectionsInRadius(self, center, radius = 5):
        blocks = self.createMoves(center, radius, False)
        for gridPos in blocks:
            self.changeBlockDirection(gridPos, center)

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

    def changeBlockDirection(self, gridPos, center):
        block = self.getBlockByGridPos(gridPos)
        
        blockX, blockY = block.gridPos
        centerX, centerY = center.gridPos
        
        dirX = blockX - centerX
        dirY = blockY - centerY

        block.direction[0] = self.normalize(dirX)
        block.direction[1] = self.normalize(dirY)

class Block():
    def __init__(self, x=0, y=0, size=1, direction = [0, 0]):
        self.gridPos = (x, y)
        self.rect = pygame.Rect(x*size, y*size, size, size)
        self.color = (255,255,255)
        self.size = size
        self.particleID = None
        self.direction = direction
        self.pressureStrenght = 1