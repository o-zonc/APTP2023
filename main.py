import pygame

from breakout import *

pygame.init()
iconimg = pygame.image.load('./src/image/icon.png')
pygame.display.set_icon(iconimg)

window.splash()

running = True

while running:
    running = window.home()
