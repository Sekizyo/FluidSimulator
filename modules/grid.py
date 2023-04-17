import pygame
from modules import BLOCKSIZE, WIDTHBLOCKS, HEIGHTBLOCKS
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

    def render(self):
        for col in self.blocks:
            for block in col:
                block.render(self.surface, self.renderDebug)

    def createBlocks(self):
        tempY = []
        for y in range(self.heightBlocks):
            tempX = []
            for x in range(self.widthBlocks):
                id = len(self.blocks)+1
                block = Block(id, x, y, self.blockSize)
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

            if newBlock:
                newBlock = self.blocks[neighbourY][neighbourX]
            else:
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
        print(particle.id, particle.gridPos, particle.dir, moves)
        particle.dir[1] += 1
        testX = particle.gridPos[0] + particle.dir[0]
        testY = particle.gridPos[1] + particle.dir[1]
        testMove = (testX, testY)
        testMoveRev = (-testX, -testY)
        if testMove in moves:
            print(testMove)
            particle.move()
            print("Foubd1")
        elif testMoveRev in moves:
            particle.move()
            print(testMoveRev)
            print("Foubd2")
        else:
            print("Not Found")

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
    def __init__(self, id=0, x=0, y=0, size=1):
        self.id = id
        self.gridPos = (x, y)
        self.rect = pygame.Rect(x*size, y*size, size, size)
        self.color = (255,255,255)
        self.highlight = False
        self.highlightColor = (255, 255, 255)
        self.size = size
        self.particleID = None
        self.font = pygame.font.SysFont("Arial", 18)

    def render(self, surface, debug=False):
        if self.particleID:
            pygame.draw.rect(surface, (100,100,100), self.rect, 0)
        elif debug:
            pygame.draw.rect(surface, self.color, self.rect, 1)
        
            idText = self.font.render(str(self.gridPos), 1, self.color)
            pygame.Surface.blit(surface, idText, (self.rect[0]+(self.size//2), self.rect[1]+(self.size//2-10)))
            
            particleIDText = self.font.render(str(self.particleID), 1, (255,255,255))
            pygame.Surface.blit(surface, particleIDText, (self.rect[0]+(self.size//2), self.rect[1]+(self.size//2+10)))
        
    