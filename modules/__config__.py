import pygame

FONT = pygame.font.SysFont("Arial", 18)

WIDTH = 800 #  - Screen width
HEIGHT = 800 #  - Screen height
BLOCKSIZE = 5 #  - Scale block size, it greatly influences prerformance
WIDTHBLOCKS = WIDTH//BLOCKSIZE
HEIGHTBLOCKS = HEIGHT//BLOCKSIZE

MAXFPS = 60
DECAYRATE = 0.997
PARTICLESPERCLICK = 100 #  - Optimal values: depends on BLOCKSIZE

