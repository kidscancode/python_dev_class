import pygame
from random import randrange
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
a = Agent(40, 40, WIDTH, HEIGHT)
all_sprites.add(a)
show_vectors = False
running = True
while running:
    delta = clock.tick(FPS) / 1000
    # input/events
    keystate = pygame.key.get_pressed()
    # if keystate[pygame.K_SPACE]:
    #     a = Agent(randrange(WIDTH), randrange(HEIGHT))
    #     all_sprites.add(a)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
            show_vectors = not show_vectors
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            a = Agent(randrange(WIDTH), randrange(HEIGHT), WIDTH, HEIGHT)
            all_sprites.add(a)
    # update
    all_sprites.update(delta)
    # draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    if show_vectors:
        for sprite in all_sprites:
            sprite.draw_vectors(screen)
    pygame.display.flip()  # last

pygame.quit()
