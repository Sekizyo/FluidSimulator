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
        self.blocksCount = 0
        self.blocks = []
        self.createBlocks()

    def switchRenderDebug(self):
        if self.renderDebug == True:
            self.renderDebug = False
        elif self.renderDebug == False:
            self.renderDebug = True

    def getPressureArrowVector(self, block):
        startPos = [block.rect[0] + block.size//2 , block.rect[1] + block.size//2]
        blockTemp = self.blockSize//2

        if block.direction == 1:
            endPos = [startPos[0] , startPos[1]-blockTemp]
        elif block.direction == 2:
            endPos = [startPos[0]+blockTemp , startPos[1]-blockTemp]
        elif block.direction == 3:
            endPos = [startPos[0]+blockTemp , startPos[1]]
        elif block.direction == 4:
            endPos = [startPos[0]+blockTemp , startPos[1]+blockTemp]
        elif block.direction == 5:
            endPos = [startPos[0] , startPos[1]+blockTemp]
        elif block.direction == 6:
            endPos = [startPos[0]-blockTemp , startPos[1]+blockTemp]
        elif block.direction == 7:
            endPos = [startPos[0]-blockTemp , startPos[1]]
        elif block.direction == 8:
            endPos = [startPos[0]-blockTemp, startPos[1]-blockTemp]

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
                
    def createBlocks(self):
        tempY = []
        for y in range(self.heightBlocks):
            tempX = []
            for x in range(self.widthBlocks):
                id = len(self.blocks)+1
                block = Block(id, x, y, self.blockSize, randint(1,8))
                self.blocksCount += 1
                tempX.append(block)
            tempY.append(tempX)
        self.blocks = tempY

    def tempClearHighlight(self):
        for col in self.blocks:
            for block in col:
                block.highlight = False

    def tempClearBlockID(self):
        for col in self.blocks:
            for block in col:
                block.particleID = None

    def getBlockByGridPos(self, pos):
        x, y = pos
        if x < 0 or y < 0 or x >= self.widthBlocks or y >= self.heightBlocks: 
            return None
        return self.blocks[y][x]
            
    def getNeighbourBlocks(self, block):
        x, y = block.gridPos
        neighbours = [(x-1,y), (x+1, y), (x, y-1), (x, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y+1)]
        neighboursCopy = neighbours.copy()

        for neighbour in neighbours:
            neighbourX, neighbourY = neighbour
            newBlock = self.getBlockByGridPos(neighbour)

            if not newBlock:
                neighboursCopy.remove(neighbour)

        return neighboursCopy

    def getFreeMovesFromMoves(self, moves):
        movesCopy = moves.copy()
        for move in moves:
            x, y = move
            block = self.blocks[y][x]
            if block.particleID:
                movesCopy.remove(move)

        return movesCopy

    def getPossibleMovesByPosition(self, position):
        block = self.getBlockByGridPos(position)
        moves = self.getNeighbourBlocks(block)
        possibleMoves = self.getFreeMovesFromMoves(moves)
        return possibleMoves

    def assignParticleToBlock(self, particle):
        block = self.getBlockByGridPos(particle.gridPos)
        block.particleID = particle.id
            
    def assignParticlesToBlocks(self, particles):
        for particle in particles:
            self.assignParticleToBlock(particle)
    
    def moveParticle(self, particle, moves):
        particle.dir[1] += 1
        testX = particle.gridPos[0] + particle.dir[0]
        testY = particle.gridPos[1] + particle.dir[1]
        testMove = (testX, testY)
        testMoveRev = (-testX, -testY)
        if testMove in moves:
            particle.move()
        elif testMoveRev in moves:
            particle.move()

        particle.dir[1] = 0

    def refreshParticleAssigment(self, particles):
        self.tempClearHighlight()
        self.tempClearBlockID()
        self.assignParticlesToBlocks(particles)

    def moveParticles(self, particles):
        self.refreshParticleAssigment(particles)
        for particle in particles:
            moves = self.getPossibleMovesByPosition(particle.gridPos)
            self.moveParticle(particle, moves)

class Block():
    def __init__(self, id=0, x=0, y=0, size=1, direction = 8):
        self.id = id
        self.gridPos = (x, y)
        self.rect = pygame.Rect(x*size, y*size, size, size)
        self.color = (255,255,255)
        self.size = size
        self.particleID = None
        self.direction = direction
