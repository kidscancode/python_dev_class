import pygame
import random

WIDTH = 800
HEIGHT = 600
FPS = 60
TILESIZE = 32
PLAYER_SPEED = 1500  # pixels/sec
FRICTION = -5

BLACK = (80, 80, 80)
WHITE = (255, 255, 255)
BLUE = (55, 121, 179)
RED = (255, 84, 76)
YELLOW = (221, 232, 63)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adventure!")
clock = pygame.time.Clock()

vec2 = pygame.math.Vector2
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec2(x, y)
        self.vel = vec2(0, 0)
        self.acc = vec2(0, 0)
        self.rect.center = self.pos

    def update(self, dt):
        self.acc = vec2(0, 0)
        keys = pygame.key.get_pressed()
        self.acc.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.acc.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        if self.acc.length() > 0:
            self.acc = self.acc.normalize() * PLAYER_SPEED
        self.acc += self.vel * FRICTION
        self.vel += self.acc * dt
        self.pos += self.vel * dt
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT
        self.rect.center = self.pos

all_sprites = pygame.sprite.Group()
player = Player(WIDTH / 2, HEIGHT / 2)
all_sprites.add(player)
running = True
while running:
    dt = clock.tick(FPS) / 1000
    # input/events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # update
    all_sprites.update(dt)
    # draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()  # last

pygame.quit()
