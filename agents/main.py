import pygame
import random
from agent import *

WIDTH = 800
HEIGHT = 600
FPS = 60
BLACK = (80, 80, 80)
WHITE = (255, 255, 255)
BLUE = (55, 121, 179)
RED = (255, 84, 76)
YELLOW = (221, 232, 63)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
a = Agent(40, 40)
all_sprites.add(a)
running = True
while running:
    delta = clock.tick(FPS) / 1000
    # input/events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # update
    all_sprites.update(delta)
    # draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()  # last

pygame.quit()
