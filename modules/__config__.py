import pygame

WIDTH = 800 #  - Screen width
HEIGHT = 800 #  - Screen height

BLOCKSIZE = 50 #  - Scale block size, it greatly influences prerformance. Optimal values: 8 - 25

MASKSIZE = 3 # Creates mask 3x3

VISCOSITY = 0.10 # - its resistance to deformation at a given rate. Lower value more likely to spread. Optimal values: 1-100
PARTICLESPERCLICK = 1 #  - Optimal values: depends on BLOCKSIZE

WIDTHBLOCKS = WIDTH//BLOCKSIZE
HEIGHTBLOCKS = HEIGHT//BLOCKSIZE

FONT = pygame.font.SysFont("Arial", 18)