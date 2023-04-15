import pygame
from modules import WIDTH, HEIGHT
class Grid():
    def __init__(self, surface):
        self.surface = surface

        self.width = WIDTH
        self.height = HEIGHT
        self.blockSize = 100
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

    def getBlockByCords(self, x, y):
        try:
            return self.blocks[y][x]
        except Exception:
            return None

    def tempClearHighlight(self):
        for col in self.blocks:
            for block in col:
                block.highlight = False

    def getNeighbourBlocks(self, block):
        x, y = block.gridPos
        neighbours = [(x-1,y), (x+1, y), (x, y-1), (x, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y+1)]
        for neighbour in neighbours:
            neighbourX, neighbourY = neighbour
            if neighbourX < 0 or neighbourY < 0:  
                neighbours.remove(neighbour)
                continue

            try:
                newBlock = self.blocks[neighbourY][neighbourX]
                newBlock.highlight = True

            except Exception as e:
                neighbours.remove(neighbour)

        return neighbours

    def getPossibleMovesByPosition(self, position):
        block = self.getBlockByPosition(position)
        moves = self.getNeighbourBlocks(block)
        print(moves)
        return moves

    def getBlockByPosition(self, position):
        for col in self.blocks:
            for block in col:
                if block.rect[0] <= position.x <= block.rect[0]+self.blockSize:
                    if block.rect[1] <= position.y <= block.rect[1]+self.blockSize:
                        return block

    def assignParticleToBlock(self, particle):
        self.tempClearHighlight()
        block = self.getBlockByPosition(particle.pos)
        self.getPossibleMovesByPosition(particle.pos)
        block.particleID = particle.id
            
    def assignParticlesToBlocks(self, particles):
        for particle in particles:
            self.assignParticleToBlock(particle)


class Block():
    def __init__(self, id=0, x=0, y=0, size=1):
        self.id = id
        self.gridPos = (x, y)
        self.rect = pygame.Rect(x*size, y*size, size, size)
        self.color = (x*5,y*5,255)
        self.highlight = False
        self.size = size
        self.particleID = None
        self.font = pygame.font.SysFont("Arial", 18)

    def render(self, surface):
        if self.highlight:
            pygame.draw.rect(surface, (200,100,250), self.rect, 1)
        else:
            pygame.draw.rect(surface, self.color, self.rect, 1)
        idText = self.font.render(str(self.gridPos), 1, self.color)
        pygame.Surface.blit(surface, idText, (self.rect[0]+(self.size//2), self.rect[1]+(self.size//2-10)))
        
        particleIDText = self.font.render(str(self.particleID), 1, (255,255,255))
        pygame.Surface.blit(surface, particleIDText, (self.rect[0]+(self.size//2), self.rect[1]+(self.size//2+10)))
        
    