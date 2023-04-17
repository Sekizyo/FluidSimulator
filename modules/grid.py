import pygame
from modules import WIDTH, HEIGHT
class Grid():
    def __init__(self, surface):
        self.surface = surface

        self.width = WIDTH
        self.height = HEIGHT
        self.blockSize = 125
        self.widthBlocks = self.width//self.blockSize
        self.heightBlocks = self.height//self.blockSize
        
        self.renderBlocks = True
        self.blocksCount = 0
        self.blocks = []
        self.createBlocks()

    def switchRenderBlocks(self):
        if self.renderBlocks == True:
            self.renderBlocks = False
        elif self.renderBlocks == False:
            self.renderBlocks = True

    def render(self):
        if self.renderBlocks:
            for col in self.blocks:
                for block in col:
                    block.render(self.surface)

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

    def getBlockByGridPos(self, x, y):
        if x < 0 or y < 0 or x >= self.widthBlocks or y >= self.heightBlocks: 
            return None
        return self.blocks[y][x]
            
    def getNeighbourBlocks(self, block):
        x, y = block.gridPos
        neighbours = [(x-1,y), (x+1, y), (x, y-1), (x, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y+1)]
        neighboursCopy = neighbours.copy()

        for neighbour in neighbours:
            neighbourX, neighbourY = neighbour
            newBlock = self.getBlockByGridPos(neighbourX, neighbourY)

            if newBlock:
                newBlock = self.blocks[neighbourY][neighbourX]
                newBlock.highlight = True
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
        block = self.getBlockByPosition(position)
        moves = self.getNeighbourBlocks(block)
        possibleMoves = self.getFreeMovesFromMoves(moves)
        print(block.gridPos, len(possibleMoves), possibleMoves)
        return possibleMoves

    def getBlockByPosition(self, position):
        for col in self.blocks:
            for block in col:
                if block.rect[0] <= position.x <= block.rect[0]+self.blockSize:
                    if block.rect[1] <= position.y <= block.rect[1]+self.blockSize:
                        return block

    def assignParticleToBlock(self, particle):
        block = self.getBlockByPosition(particle.pos)
        block.particleID = particle.id
        block.highlightColor = particle.color
            
    def assignParticlesToBlocks(self, particles):
        for particle in particles:
            self.assignParticleToBlock(particle)
    
    def moveParticle(self, particle, moves):
        for move in moves:
            particle.gridPos = move
            particle.
            return
            
    def refreshParticleAssigment(self, particles):
        self.tempClearHighlight()
        self.tempClearBlockID()
        self.assignParticlesToBlocks(particles)

    def moveParticles(self, particles):
        self.refreshParticleAssigment(particles)
        for particle in particles:
            moves = self.getPossibleMovesByPosition(particle.pos)
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

    def render(self, surface):
        if self.highlight:
            pygame.draw.rect(surface, self.highlightColor, self.rect, 1)
        else:
            pygame.draw.rect(surface, self.color, self.rect, 1)
        
        idText = self.font.render(str(self.gridPos), 1, self.color)
        pygame.Surface.blit(surface, idText, (self.rect[0]+(self.size//2), self.rect[1]+(self.size//2-10)))
        
        particleIDText = self.font.render(str(self.particleID), 1, (255,255,255))
        pygame.Surface.blit(surface, particleIDText, (self.rect[0]+(self.size//2), self.rect[1]+(self.size//2+10)))
        
    