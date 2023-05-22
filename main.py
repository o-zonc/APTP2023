import pygame
from breakout import *
from dqn import *
from setting import *

pygame.init()
iconimg = pygame.image.load('./src/image/icon.png')
pygame.display.set_icon(iconimg)

window.splash()

window.home()

window.main()