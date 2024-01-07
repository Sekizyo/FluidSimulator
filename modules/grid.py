import pygame
import numpy as np
from scipy import signal
from skimage.util.shape import view_as_windows

from modules.__config__ import BLOCKSIZE, WIDTHBLOCKS, HEIGHTBLOCKS, PARTICLESPERCLICK

class Render():
    def renderGrid(self, blocks: np.ndarray, surface: pygame.Surface) -> None:
        block_colors = self.generateBlockColors(blocks)
        surface.blit(block_colors, (0, 0))

    def generateBlockColors(self, blocks: np.ndarray) -> pygame.Surface:
        colors = np.clip(blocks * 255, 0, 255).astype(np.uint8)
        colors_surface = pygame.surfarray.make_surface(colors)
        return pygame.transform.scale(colors_surface, (WIDTHBLOCKS * BLOCKSIZE, HEIGHTBLOCKS * BLOCKSIZE))

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
    def convolve(self, matrix, block_size):
        results = []
        sliced_matrix = self.split_matrix(matrix, block_size)
        
        for row in range(len(sliced_matrix)):
            for col in range(len(sliced_matrix[row])):
                results.append(self.updateSlice(sliced_matrix[row][col]))

        combined_array = self.concatenate(results[0], results[1], axis=1)
        combined_array_2 = self.concatenate(results[2], results[3], axis=1)
        final_combined_array = self.concatenate(combined_array, combined_array_2, axis=0)

        return final_combined_array
    
    def split_matrix(self, matrix, size):
        return view_as_windows(matrix, (size, size), step=size)
    
    def concatenate(self, matrix1, matrix2, axis=0):
        combinedArray = np.concatenate((matrix1, matrix2), axis=axis)
        if axis == 0:
            overlap = (matrix1[-1, :] + matrix2[0, :]) / 2  # Average overlapping rows
            combinedArray[matrix1.shape[0] - 1, :] = overlap
            combinedArray[matrix1.shape[0], :] = overlap
        elif axis == 1:
            overlap = (matrix1[:, -1] + matrix2[:, 0]) / 2  # Average overlapping columns
            combinedArray[:, matrix1.shape[1] - 1] = overlap
            combinedArray[:, matrix1.shape[1]] = overlap

        return combinedArray
    
    def updateSlice(self, matrix):
        initial_sum = matrix.sum()
        if initial_sum == 0:
            matrix[0][0] = 0.001 

        convolved_matrix = convolve2d(matrix, self.kernel, mode='same', boundary='symm')
        
        scaling_factor = initial_sum / convolved_matrix.sum()
        convolved_matrix *= scaling_factor
        return convolved_matrix


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
        self.matrix[0][0] = 0.01
        self.particleCounter = 0

class Grid(Convolution, Controls, Render):
    def __init__(self, surface: pygame.surface.Surface) -> None:
        self.surface = surface

        self.matrix = np.zeros((WIDTHBLOCKS, HEIGHTBLOCKS))
        self.particleCounter = 0
        self.blockRect = pygame.Rect(0, 0, BLOCKSIZE, BLOCKSIZE)

        self.kernel = np.array([
                    [1/9, 1/9, 1/9],
                    [1/9, 1/9, 1/9],
                    [1/9, 1/9, 1/9]
                ])

    def render(self) -> None:
        self.renderGrid(self.matrix)

    def logic(self) -> None:
        self.matrix = self.convolve(self.matrix, WIDTHBLOCKS//2)