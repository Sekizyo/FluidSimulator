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
            if color > 255:
                color = 255
            pygame.draw.rect(self.surface, (color, color, color), self.blockRect)

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
        if self.checkBounds(x, y) and self.matrix[y][x] != -1:
            self.matrix[y][x] = value

class Convolution:
    def update(self, matrix):
        input_height, input_width = matrix.shape
        kernel_height, kernel_width = self.kernel.shape

        output_height = input_height - kernel_height + 1
        output_width = input_width - kernel_width + 1

        output_matrix = np.zeros((output_height, output_width))

        for i in range(output_height):
            for j in range(output_width):
                output_matrix[i, j] = np.sum(matrix[i:i+kernel_height, j:j+kernel_width] * self.kernel)

        return output_matrix

class Controls(Position):
    def addParticle(self, mouse: tuple()) -> None:
        x, y = self.getGridPosFromPos(mouse)
        self.updateBlock(x, y, PARTICLESPERCLICK)
        self.particleCounter += PARTICLESPERCLICK

    def addWall(self, mouse: tuple()) -> None:
        x, y = self.getGridPosFromPos(mouse)
        self.updateBlock(x, y, -1)

    def reset(self) -> None:
        self.matrix = np.zeros((WIDTHBLOCKS, HEIGHTBLOCKS))
        self.particleCounter = 0

class Grid(Convolution, Controls, Render):
    def __init__(self, surface: pygame.surface.Surface) -> None:
        self.surface = surface

        self.matrix = np.zeros((WIDTHBLOCKS, HEIGHTBLOCKS))
        self.matrix[0][0] = 0.01
        self.particleCounter = 0
        self.blockRect = pygame.Rect(0, 0, BLOCKSIZE, BLOCKSIZE)

        self.kernel = np.array([
                    [1/16, 1/8, 1/16],
                    [1/8, 1/4, 1/8],
                    [1/16, 1/8, 1/16]
                ])

    def render(self) -> None:
        self.renderGrid(self.matrix)

    def logic(self) -> None:
        initial_sum = self.matrix.sum()
        padded_matrix = np.pad(self.matrix, ((1, 1), (1, 1)), mode='constant')
        self.matrix = self.update(padded_matrix)

        scaling_factor = initial_sum / self.matrix.sum()
        self.matrix *= scaling_factor