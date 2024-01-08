import pygame
import numpy as np

from scipy.signal import convolve2d

from modules.__config__ import BLOCKSIZE, WIDTHBLOCKS, HEIGHTBLOCKS, PARTICLESPERCLICK

class Convolution():
    def __init__(self) -> None:
        super(Convolution, self).__init__()
        self.matrix = np.zeros((WIDTHBLOCKS, HEIGHTBLOCKS))
        self.kernel = np.array([
            [1/9, 1/9, 1/9],
            [1/9, 1/9, 1/9],
            [1/9, 1/9, 1/9]
        ])

    def convolve(self, matrix: np.ndarray) -> np.ndarray:
        initial_sum = matrix.sum()
        if initial_sum == 0:
            return matrix

        convolved_matrix = convolve2d(matrix, self.kernel, mode='same', boundary='symm')
        
        scaling_factor = initial_sum / convolved_matrix.sum()
        convolved_matrix *= scaling_factor
        return convolved_matrix

class Controls():
    def __init__(self) -> None:
        super(Controls, self).__init__()
        self.particleCounter = 0

    def addParticle(self, mouse: tuple) -> None:
        x, y = self.getGridPosFromPos(mouse)
        if self.checkBounds(x, y):
            self.matrix[x, y] += PARTICLESPERCLICK
            self.particleCounter += PARTICLESPERCLICK

    def getGridPosFromPos(self, pos: tuple) -> int:
        x, y = pos
        return (x//BLOCKSIZE, y//BLOCKSIZE)
    
    def checkBounds(self, x: int, y: int) -> bool:
        if (0 <= x < WIDTHBLOCKS) and (0 <= y < HEIGHTBLOCKS):
            return True
        else:
            return False

    def reset(self) -> None:
        self.matrix = np.zeros((WIDTHBLOCKS, HEIGHTBLOCKS))
        self.particleCounter = 0

class Render():
    def renderGrid(self, blocks: np.ndarray, surface: pygame.Surface) -> None:
        block_colors = self.generateBlockColors(blocks)
        surface.blit(block_colors, (0, 0))

    def generateBlockColors(self, blocks: np.ndarray) -> pygame.Surface:
        colors = np.clip(blocks * 255, 0, 255).astype(np.uint8)
        colors_surface = pygame.surfarray.make_surface(colors)
        return pygame.transform.scale(colors_surface, (WIDTHBLOCKS * BLOCKSIZE, HEIGHTBLOCKS * BLOCKSIZE))

class Matrix(Convolution, Controls, Render):
    def __init__(self, surface: pygame.surface.Surface) -> None:
        super(Matrix, self).__init__()
        self.surface = surface

    def render(self) -> None:
        self.renderGrid(self.matrix, self.surface)

    def logic(self) -> None:
        self.matrix = self.convolve(self.matrix)