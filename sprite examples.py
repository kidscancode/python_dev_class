import pygame
import random

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
screen_rect = screen.get_rect()
clock = pygame.time.Clock()

# convenient name for Vector2
vec = pygame.math.Vector2
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.pos = vec(0, 50)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self, dt):
        self.acc = vec(0, 0)
        keys = pygame.key.get_pressed()
        self.acc.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.acc.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        if self.acc.length() > 0:
            self.acc = self.acc.normalize() * 150
        self.vel += self.acc * dt
        self.pos += self.vel * dt
        self.rect.center = self.pos

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = screen_rect.center
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(random.randrange(50, 150), 0).rotate(random.randrange(360))

    def update(self, dt):
        self.pos += self.vel * dt
        self.rect.center = self.pos
        if self.pos.x > WIDTH - self.rect.width / 2:
            self.vel.x *= -1
        if self.pos.x < self.rect.width / 2:
            self.vel.x *= -1
        if self.pos.y < self.rect.height / 2:
            self.vel.y *= -1
        if self.pos.y > HEIGHT - self.rect.height / 2:
            self.vel.y *= -1

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
for i in range(5):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
player = Player()
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
    # check for collisions
    hits = pygame.sprite.spritecollide(player, mobs, True)
    # draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()  # last

pygame.quit()
