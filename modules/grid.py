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

    def createBlocks(self):
        tempY = []
        for y in range(self.heightBlocks):
            tempX = []
            for x in range(self.widthBlocks):
                id = len(self.blocks)+1
                block = Block(id, x, y, self.blockSize, [randint(-1, 1), randint(-1, 1)])
                self.blocksCount += 1
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
        strenght = block.pressureStrenght

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
        self.refreshParticleAssigment(particles)
        for particle in particles:
            moves = self.getPossibleMovesByPosition(particle.gridPos)
            self.moveParticle(particle, moves)

    def refreshParticleAssigment(self, particles):
        self.tempClearHighlight()
        self.tempClearBlockID()
        self.assignParticlesToBlocks(particles)

    def tempClearHighlight(self):
        for col in self.blocks:
            for block in col:
                block.highlight = False

    def tempClearBlockID(self):
        for col in self.blocks:
            for block in col:
                block.particleID = None

    def assignParticlesToBlocks(self, particles):
        for particle in particles:
            self.assignParticleToBlock(particle)

    def assignParticleToBlock(self, particle):
        block = self.getBlockByGridPos(particle.gridPos)
        block.particleID = particle.id

    def getPossibleMovesByPosition(self, position):
        block = self.getBlockByGridPos(position)
        moves = self.getNeighbourBlocks(block)
        possibleMoves = self.getFreeMovesFromMoves(moves)
        return possibleMoves
        
    def getNeighbourBlocks(self, block, depth = 1):
        x, y = block.gridPos
        neighbours = self.createMoves(x, y, depth)
        neighboursCopy = neighbours.copy()

        for neighbour in neighbours:
            neighbourX, neighbourY = neighbour
            newBlock = self.getBlockByGridPos(neighbour)

            if not newBlock:
                neighboursCopy.remove(neighbour)

        return neighboursCopy

    def createMoves(self, x, y, depth=1):
        moves = []
        for i in range(1, depth+1):
            neighbours = [[x-i, y], [x+i, y], [x, y-i], [x, y+i], [x-i, y-i], [x+i, y-i], [x-i, y+i], [x+i, y+i]]
            for neighbour in neighbours:
                moves.append(neighbour)
        return moves

    def getFreeMovesFromMoves(self, moves):
        movesCopy = moves.copy()
        for move in moves:
            x, y = move
            block = self.blocks[y][x]
            if block.particleID:
                movesCopy.remove(move)

        return movesCopy

    def getBlockByGridPos(self, pos):
        x, y = pos
        if x < 0 or y < 0 or x >= self.widthBlocks or y >= self.heightBlocks: 
            return None
        return self.blocks[y][x]
    
    def moveParticle(self, particle, moves):
        block = self.getBlockByGridPos(particle.gridPos)
        position = particle.gridPos

        position[0] += block.direction[0]
        position[1] += block.direction[1]
        if position in moves:
            particle.gridPos = position

    def changeBlockDirections(self, mouse):
        gridPos = self.getGridPosFromPos(mouse)
        block = self.getBlockByGridPos(gridPos)
        if block:
            self.changeBlocksDirectionsInRadius(block, gridPos)

    def getGridPosFromPos(self, pos):
        x, y = pos
        return x//self.blockSize, y//self.blockSize

    def changeBlocksDirectionsInRadius(self, block, center, radius = 3):
        blocks = self.getNeighbourBlocks(block, radius)
        for gridPos in blocks:
            self.changeBlockDirection(gridPos, center)

    def changeBlockDirection(self, gridPos, center, strenght=2):
        block = self.getBlockByGridPos(gridPos)
        center = self.getBlockByGridPos(center)

        block.direction[0] = round((center.gridPos[0] - block.gridPos[1])//strenght)
        block.direction[1] = round((center.gridPos[1] - block.gridPos[1])//strenght)

class Block():
    def __init__(self, id=0, x=0, y=0, size=1, direction = [0, 1]):
        self.id = id
        self.gridPos = (x, y)
        self.rect = pygame.Rect(x*size, y*size, size, size)
        self.color = (255,255,255)
        self.size = size
        self.particleID = None
        self.direction = direction
        self.pressureStrenght = 40
