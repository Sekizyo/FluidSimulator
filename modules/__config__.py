import pygame

WIDTH = 800 #  - Screen width
HEIGHT = 800 #  - Screen height

BLOCKSIZE = 10 #  - Scale block size, it greatly influences prerformance. Optimal values: 8 - 25

VISCOSITY = 1 # - its resistance to deformation at a given rate. Lower value more likely to spread. Optimal values: 1-100
PARTICLESPERCLICK = 10000 #  - Optimal values: depends on BLOCKSIZE

WIDTHBLOCKS = WIDTH//BLOCKSIZE
HEIGHTBLOCKS = HEIGHT//BLOCKSIZE

FONT = pygame.font.SysFont("Arial", 18)