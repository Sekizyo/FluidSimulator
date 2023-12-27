import pygame

WIDTH = 800 #  - Screen width
HEIGHT = 800 #  - Screen height

BLOCKSIZE = 10 #  - Scale block size, it greatly influences prerformance. Optimal values: 8 - 25

PARTICLESPERCLICK = 10 #  - Optimal values: depends on BLOCKSIZE

WIDTHBLOCKS = WIDTH//BLOCKSIZE
HEIGHTBLOCKS = HEIGHT//BLOCKSIZE

FONT = pygame.font.SysFont("Arial", 18)