import pygame
import numpy as np
from random import randint

from scipy.signal import convolve2d

from modules.__config__ import WIDTH, HEIGHT, WIDTHBLOCKS, HEIGHTBLOCKS, BLOCKSIZE, DECAYRATE, PARTICLESPERCLICK, VELOCITYCOEFF, PRESSURECOEFF

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

class Convolution(Kernels):
    def __init__(self) -> None:
        super(Convolution, self).__init__()
        self.matrix = np.zeros((WIDTHBLOCKS, HEIGHTBLOCKS))
        self.decayRate = DECAYRATE
        self.velocityCoeff = VELOCITYCOEFF
        self.pressureCoeff = PRESSURECOEFF

    def convolve(self, matrix: np.ndarray) -> np.ndarray:
        return convolve2d(matrix, self.kernel, mode='same', boundary='wrap')
    
    def flow(self, matrix: np.ndarray) -> np.ndarray:
        horizontal_conv = convolve2d(matrix, self.horizontal_kernel, mode='same', boundary='wrap')
        vertical_conv = convolve2d(matrix, self.vertical_kernel, mode='same', boundary='wrap')
        matrix = np.sqrt(horizontal_conv**2 + vertical_conv**2)
        
        return matrix
    
    def flow2(self, matrix: np.ndarray) -> np.ndarray:
        velocity_matrix = np.sqrt(matrix) * self.velocityCoeff 
        pressure_matrix = matrix * self.pressureCoeff
        matrix = np.sqrt(velocity_matrix**2 + pressure_matrix**2)

        return matrix
    
    def decay(self, matrix: np.ndarray) -> np.ndarray:
        matrix *= self.decayRate
        return matrix 
    
    def scale(self, matrix: np.ndarray, initSum: float) -> np.ndarray:
        scaling_factor = initSum / matrix.sum()
        matrix *= scaling_factor
        return matrix

class Controls():
    def __init__(self) -> None:
        super(Controls, self).__init__()
        self.particleCounter = 0
        self.particlesPerClick = PARTICLESPERCLICK
        self.width = WIDTHBLOCKS
        self.height = HEIGHTBLOCKS
        self.blockSize = BLOCKSIZE
        self.isRain = False
        self.changeAmount = 0.1
        self.changeAmounDecayRate = 0.001

    def addParticle(self, mouse: tuple) -> None:
        x, y = self.getGridPosFromPos(mouse)
        if self.checkBounds(x, y):
            self.matrix[x, y] += self.particlesPerClick
            self.particleCounter += self.particlesPerClick

    def rain(self) -> None:
        if self.isRain:
            self.addParticle((randint(0, WIDTH), randint(0, HEIGHT)))

    def increasePreassureCoeff(self) -> None:
        newPressure = self.pressureCoeff + self.changeAmount
        if newPressure <= 1:
            self.pressureCoeff = newPressure

    def decreasePreassureCoeff(self) -> None:
        newPressure = self.pressureCoeff - self.changeAmount
        if newPressure >= 0:
            self.pressureCoeff = newPressure

    def increaseVelocityCoeff(self) -> None:
        newVelocity = self.velocityCoeff + self.changeAmount
        if newVelocity <= 1:
            self.velocityCoeff = newVelocity

    def decreaseVelocityCoeff(self) -> None:
        newVelocity = self.velocityCoeff - self.changeAmount
        if newVelocity >= 0:
            self.velocityCoeff = newVelocity

    def increaseDecayRate(self) -> None:
        newRate = self.decayRate + self.changeAmounDecayRate
        if newRate <= 1:
            self.decayRate = newRate

    def decreaseDecayRate(self) -> None:
        newRate = self.decayRate - self.changeAmounDecayRate
        if newRate >= 0:
            self.decayRate = newRate
        
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
        self.isRain = False
        self.velocityCoeff = VELOCITYCOEFF
        self.pressureCoeff = PRESSURECOEFF
        self.decayRate = DECAYRATE

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
        matrix = self.matrix
        self.rain()

        initSum = matrix.sum()
        if initSum == 0:
            return

        matrix = self.flow(matrix)
        matrix = self.flow2(matrix)
        matrix = self.convolve(matrix)

        self.matrix = self.scale(matrix, initSum)
        matrix = self.decay(matrix)
