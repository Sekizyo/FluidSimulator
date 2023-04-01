
import pygame
from modules.screen import Screen

screen = Screen()
exit = False

def controls():
    global exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
            exit = True

def draw():

    pygame.display.update()

def run():
    global exit
    while not exit:
        controls()
        draw()