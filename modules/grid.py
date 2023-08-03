import pygame

from modules import BLOCKSIZE, WIDTHBLOCKS, HEIGHTBLOCKS, DEPTH, VISCOSITY, PARTICLESPERCLICK

class Render():
    def renderGrid(self, blockRect: list[pygame.Rect], blocks: list[int]) -> None:
        for y, col in enumerate(blockRect):
            for x, rect in enumerate(col):
                nparticles = blocks[y][x]
                self.renderBlock(nparticles, rect)

    def renderBlock(self, nparticles: int, rect: list[pygame.Rect]) -> None:
        if nparticles >= 0:
            color = self.getColor(nparticles)
            pygame.draw.rect(self.surface, color, rect)
        else:
            pygame.draw.rect(self.surface, [255, 0, 0], rect)

    def getColor(self, nparticles: int) -> list[int]:
        delta = nparticles
        if delta > 255: 
            return [255, 255, 255]
        else:
            return [delta, delta, delta]

class Position():
    def checkBounds(self, x: int, y: int) -> bool:
        if (0 <= x < WIDTHBLOCKS) and (0 <= y < HEIGHTBLOCKS):
            return True
        return False

    def getGridPosFromPos(self, pos: tuple) -> int:
        x, y = pos
        return x//BLOCKSIZE, y//BLOCKSIZE
    
    def getBlockValue(self, x: int, y: int) -> int:
        if self.checkBounds(x, y):
            return self.blocks[y][x]

    def updateBlock(self, x: int, y: int, value: int) -> None:
        if self.checkBounds(x, y) and self.blocks[y][x] != -1:
            self.blocks[y][x] = value

    def updateParticleCounter(self, value: int) -> None:
        self.particleCounter += value

class Moves(Position):
    def getMoves(self, startX: int, startY: int, depth: int=1) -> list[tuple()]:
        moves = []

        for x in range(-depth,depth+1):
            Y = int((depth*depth-x*x)**0.5)
            for y in range(-Y,Y+1):
                x1 = x+startX
                y1 = y+startY

                if self.checkBounds(x1, y1):
                    moves.append((x1, y1))
        return moves
    
    def getBlockValuesFromPosList(self, pos: tuple) -> list[int]:
        values = []
        for x, y in pos:
            val = self.getBlockValue(x, y)
            if val >= 0:
                values.append(val)
        return values
    
    def getAverageForList(self, list: list) -> int:
        return sum(list) / len(list)    

class Diffusion(Moves):
    def update(self, blocks: list[int]) -> None:
        for y, col in enumerate(blocks):
            for x, block in enumerate(col):
                if block >= VISCOSITY:
                    self.updateBlocks(x, y)

    def updateBlocks(self, x: int, y: int) -> None:
        neighboursPos = self.getMoves(x, y, DEPTH)
        values = self.getBlockValuesFromPosList(neighboursPos)
        avg = self.getAverageForList(values)
        for x, y in neighboursPos:
            if self.getBlockValue(x, y) != -1:
                self.updateBlock(x, y, avg)

class Controls():
    def createBlocks(self) -> None:
        for y in range(HEIGHTBLOCKS):
            tempX = []
            tempXRect = []
            for x in range(WIDTHBLOCKS):
                tempX.append(0)
                tempXRect.append(pygame.Rect(x*self.size, y*self.size, self.size, self.size))
                
            self.blocks.append(tempX)
            self.blockRect.append(tempXRect)

    def addParticle(self, mouse: tuple()) -> None:
        x, y = self.getGridPosFromPos(mouse)
        self.updateBlock(x, y, PARTICLESPERCLICK)
        self.updateParticleCounter(PARTICLESPERCLICK)

    def addWall(self, mouse: tuple()) -> None:
        x, y = self.getGridPosFromPos(mouse)
        self.updateBlock(x, y, -1)

    def reset(self) -> None:
        self.blocks = []
        self.blockRect = []
        self.particleCounter = 0

        self.createBlocks()

class Grid(Render, Diffusion, Controls):
    def __init__(self, surface: pygame.surface.Surface) -> None:
        self.surface = surface
        self.size = BLOCKSIZE

        self.blocks = []
        self.blockRect = []
        
        self.particleCounter = 0
        self.createBlocks()

    def render(self) -> None:
        self.renderGrid(self.blockRect, self.blocks)

    def logic(self) -> None:
        self.update(self.blocks)
