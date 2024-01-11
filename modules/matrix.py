import pygame
import numpy as np

from scipy.signal import convolve2d

from modules.__config__ import WIDTH, HEIGHT, WIDTHBLOCKS, HEIGHTBLOCKS, BLOCKSIZE, DECAYRATE, PARTICLESPERCLICK

class Kernels():
    def __init__(self) -> None:
        super(Kernels, self).__init__()
        self.kernel = np.array([
            [1/9, 1/9, 1/9],
            [1/9, 1/9, 1/9],
            [1/9, 1/9, 1/9]
        ])

        # Sobel filter for different directions
        self.horizontal_kernel = np.array([
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ])

        self.vertical_kernel = np.array([
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1]
        ])

        self.diagonal_kernel = np.array([
            [0, 1, 2],
            [-1, 0, 1],
            [-2, -1, 0]
        ])

        self.antidiagonal_kernel = np.array([
            [2, 1, 0],
            [1, 0, -1],
            [0, -1, -2]
        ])

class Convolution(Kernels):
    def __init__(self) -> None:
        super(Convolution, self).__init__()
        self.matrix = np.zeros((WIDTHBLOCKS, HEIGHTBLOCKS))
        self.decayRate = DECAYRATE

    def convolve(self, matrix: np.ndarray) -> np.ndarray:
        initialSum = matrix.sum()
        if initialSum == 0:
            return matrix

        convolved_matrix = convolve2d(matrix, self.kernel, mode='same', boundary='symm')
        return self.scale(convolved_matrix, initialSum)
    
    def flow(self, matrix: np.ndarray) -> np.ndarray:
        initialSum = matrix.sum()
        if initialSum == 0:
            return matrix

        horizontal_conv = convolve2d(matrix, self.horizontal_kernel, mode='same', boundary='symm')
        vertical_conv = convolve2d(matrix, self.vertical_kernel, mode='same', boundary='symm')
        diagonal_conv = convolve2d(matrix, self.diagonal_kernel, mode='same', boundary='symm')
        antidiagonal_conv = convolve2d(matrix, self.antidiagonal_kernel, mode='same', boundary='symm')

        convolved_matrix = np.sqrt(horizontal_conv**2 + vertical_conv**2 + diagonal_conv**2 + antidiagonal_conv**2)
        return self.scale(convolved_matrix, initialSum)
    
    def scale(self, matrix: np.ndarray, initialSum: float) -> np.ndarray:
        scaling_factor = initialSum / matrix.sum()
        matrix *= scaling_factor
        matrix *= self.decayRate
        
        return matrix
    
class Controls():
    def __init__(self) -> None:
        super(Controls, self).__init__()
        self.particleCounter = 0
        self.particlesPerClick = PARTICLESPERCLICK
        self.width = WIDTHBLOCKS
        self.height = HEIGHTBLOCKS
        self.blockSize = BLOCKSIZE

    def addParticle(self, mouse: tuple) -> None:
        x, y = self.getGridPosFromPos(mouse)
        if self.checkBounds(x, y):
            self.matrix[x, y] += self.particlesPerClick
            self.particleCounter += self.particlesPerClick

    def getGridPosFromPos(self, pos: tuple) -> int:
        x, y = pos
        return (x//self.blockSize, y//self.blockSize)
    
    def checkBounds(self, x: int, y: int) -> bool:
        if (0 <= x < self.width) and (0 <= y < self.height):
            return True
        else:
            return False

    def reset(self) -> None:
        self.matrix = np.zeros((self.width, self.height))
        self.particleCounter = 0

class Render():
    def renderGrid(self, blocks: np.ndarray, surface: pygame.Surface) -> None:
        blocks = self.generateBlocks(blocks)
        surface.blit(blocks, (0, 0))

    def generateBlocks(self, blocks: np.ndarray) -> pygame.Surface:
        colors = np.clip(blocks * 255, 0, 255).astype(np.uint8)
        colors_surface = pygame.surfarray.make_surface(colors)
        return pygame.transform.scale(colors_surface, (WIDTH, HEIGHT))

class Matrix(Convolution, Controls, Render):
    def __init__(self, surface: pygame.surface.Surface) -> None:
        super(Matrix, self).__init__()
        self.surface = surface

    def render(self) -> None:
        self.renderGrid(self.matrix, self.surface)

    def update(self) -> None:
        self.matrix = self.convolve(self.matrix)
        self.matrix = self.flow(self.matrix)