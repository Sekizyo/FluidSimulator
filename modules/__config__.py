import pygame

WIDTH = 1000 #  - Screen width
HEIGHT = 1000 #  - Screen height

BLOCKSIZE = 5 #  - Scale block size, it greatly influences prerformance. Optimal values: 8 - 25

PARTICLESPERCLICK = 100 #  - Optimal values: depends on BLOCKSIZE

WIDTHBLOCKS = WIDTH//BLOCKSIZE
HEIGHTBLOCKS = HEIGHT//BLOCKSIZE

FONT = pygame.font.SysFont("Arial", 18)