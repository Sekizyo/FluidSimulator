import pygame

import numpy as np
from modules.__config__ import BLOCKSIZE, WIDTHBLOCKS, HEIGHTBLOCKS, MASKSIZE, VISCOSITY, PARTICLESPERCLICK

class Render():
    def renderGrid(self, blocks: list[int]) -> None:
        for y, col in enumerate(blocks):
            for x, nparticles in enumerate(col):
                self.renderBlock(x, y, nparticles)

    def renderBlock(self, x: int, y: int, nparticles: int) -> None:

        self.blockRect.left = BLOCKSIZE*x
        self.blockRect.top = BLOCKSIZE*y

        if nparticles >= 0:
            color = int(nparticles*255)
            pygame.draw.rect(self.surface, (color, color, color), self.blockRect)
        else:
            pygame.draw.rect(self.surface, [255, 0, 0], self.blockRect)
class Position():
    def checkBounds(self, x: int, y: int) -> bool:
        if (0 <= x < WIDTHBLOCKS) and (0 <= y < HEIGHTBLOCKS):
            return True
        else:
            return False

    def getGridPosFromPos(self, pos: tuple) -> int:
        x, y = pos
        return x//BLOCKSIZE, y//BLOCKSIZE
    
    def updateBlock(self, x: int, y: int, value: int) -> None:
        if self.checkBounds(x, y) and self.blocks[y][x] != -1:
            self.blocks[y][x] = value

    def updateParticleCounter(self, value: int) -> None:
        self.particleCounter += value

class Mask(Position):
    def getMask(self, startX: int, startY: int) -> list[tuple()]:
        x_coords = np.arange((-MASKSIZE // 2)+startX+1, (MASKSIZE // 2)+startX+1)
        y_coords = np.arange((-MASKSIZE // 2)+startY+1, (MASKSIZE // 2)+startY+1)

        X, Y = np.meshgrid(x_coords, y_coords)

        return np.vstack((X.ravel(), Y.ravel())).T

    def getBlockValuesFromPosList(self, pos: list[tuple]) -> list[int]:
        values = []
        for x, y in pos:
            val = self.blocks[y][x]
            if val >= 0:
                values.append(val)
        return values
    
    def getAverageForList(self, list: list) -> float:
        if list:
            return sum(list) / len(list)    

class Diffusion(Mask):
    def update(self, blocks: list[int]) -> None:
        for y in range(MASKSIZE, len(blocks)-MASKSIZE):
            for x in range(MASKSIZE, len(blocks)-MASKSIZE):
                if blocks[y][x] >= VISCOSITY:
                    self.updateBlocks(x, y)

    def updateBlocks(self, x: int, y: int) -> None:
        neighboursPos = self.getMask(x, y)
        values = self.getBlockValuesFromPosList(neighboursPos)
        avg = self.getAverageForList(values)
        for x, y in neighboursPos:
            if self.blocks[y][x] != -1:
                self.updateBlock(x, y, avg)

class Controls():
    def addParticle(self, mouse: tuple()) -> None:
        x, y = self.getGridPosFromPos(mouse)
        self.updateBlock(x, y, PARTICLESPERCLICK)
        self.updateParticleCounter(PARTICLESPERCLICK)

    def addWall(self, mouse: tuple()) -> None:
        x, y = self.getGridPosFromPos(mouse)
        self.updateBlock(x, y, -1)

    def reset(self) -> None:
        self.blocks = np.zeros((HEIGHTBLOCKS, WIDTHBLOCKS))
        self.particleCounter = 0

class Grid(Render, Diffusion, Controls):
    def __init__(self, surface: pygame.surface.Surface) -> None:
        self.surface = surface

        self.blocks = np.zeros((HEIGHTBLOCKS, WIDTHBLOCKS))
        self.particleCounter = 0
        self.blockRect = pygame.Rect(0, 0, BLOCKSIZE, BLOCKSIZE)

    def render(self) -> None:
        self.renderGrid(self.blocks)

    def logic(self) -> None:
        self.update(self.blocks)