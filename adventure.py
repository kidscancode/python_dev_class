# mobs
#   damage/etc
#   shooting
#   pathfinding
# tile map graphics
# win condition

import pygame
import random
from os import path
import xml.etree.ElementTree as ET
game_folder = path.dirname(__file__)
map_folder = path.join(game_folder, 'maps')
art_folder = path.join(game_folder, 'art')

WIDTH = 800
HEIGHT = 640
FPS = 60
TILESIZE = 64
PLAYER_ACCEL = 5000  # pixels/sec
FRICTION = -15

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

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite, group, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
            if hits:
                if sprite.hit_rect.centerx > hits[0].rect.centerx:
                    sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
                if sprite.hit_rect.centerx < hits[0].rect.centerx:
                    sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
                sprite.hit_rect.centerx = sprite.pos.x
                sprite.vel.x = 0
        if dir == 'y':
            hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
            if hits:
                if sprite.hit_rect.centery > hits[0].rect.centery:
                    sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
                if sprite.hit_rect.centery < hits[0].rect.centery:
                    sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
                sprite.hit_rect.centery = sprite.pos.y
                sprite.vel.y = 0

class Spritesheet:
    def __init__(self, filename):
        # filename - without extension, find matching xml
        self.spritesheet = pygame.image.load(filename + '.png').convert_alpha()
        if path.isfile(filename + '.xml'):
            tree = ET.parse(filename + '.xml')
            self.map = {}
            # read xml and pull out desired values (x, y, w, h)
            for node in tree.iter():
                if node.attrib.get('name'):
                    name = node.attrib.get('name')
                    self.map[name] = {}
                    self.map[name]['x'] = int(node.attrib.get('x'))
                    self.map[name]['y'] = int(node.attrib.get('y'))
                    self.map[name]['w'] = int(node.attrib.get('width'))
                    self.map[name]['h'] = int(node.attrib.get('height'))

    def get_image_by_name(self, name):
        rect = pygame.Rect(self.map[name]['x'], self.map[name]['y'],
                           self.map[name]['w'], self.map[name]['h'])
        return self.spritesheet.subsurface(rect)

    def get_image_by_rect(self, x, y, w, h):
        rect = pygame.Rect(x, y, w, h)
        return self.spritesheet.subsurface(rect)

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)
        x = min(0, x)
        y = min(0, y)
        x = max(WIDTH - self.width, x)
        y = max(HEIGHT - self.height, y)
        self.camera = pygame.Rect(x, y, self.width, self.height)

    def apply(self, object):
        return object.rect.move(self.camera.topleft)

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((TILESIZE//1.2, TILESIZE//1.2 ))
        self.image = character_sheet.get_image_by_name('robot1_gun.png')
        self.image_clean = self.image.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, 35, 35)
        self.pos = vec2(x, y)
        self.vel = vec2(0, 0)
        self.acc = vec2(0, 0)
        self.rot = 0
        self.rect.center = self.pos
        self.hit_rect.center = self.rect.center
        self.target = target

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((TILESIZE//1.2, TILESIZE//1.2 ))
        self.image = character_sheet.get_image_by_name('manBlue_gun.png')
        self.image_clean = self.image.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, 35, 35)
        self.pos = vec2(x, y)
        self.vel = vec2(0, 0)
        self.acc = vec2(0, 0)
        self.rot = 0
        self.rect.center = self.pos
        self.hit_rect.center = self.rect.center

    def update(self, dt):
        self.acc = vec2(0, 0)
        self.rot_speed = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rot_speed = 200
        if keys[pygame.K_RIGHT]:
            self.rot_speed = -200
        if keys[pygame.K_UP]:
            self.acc = vec2(PLAYER_ACCEL, 0).rotate(-self.rot)
        # self.acc.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        # self.acc.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        # if self.acc.length() > 0:
        #     self.acc = self.acc.normalize() * PLAYER_ACCEL
        self.rot = (self.rot + self.rot_speed * dt) % 360
        self.image = pygame.transform.rotate(self.image_clean, self.rot)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.acc += self.vel * FRICTION
        self.vel += self.acc * dt
        self.pos += self.vel * dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, walls, 'y')
        self.rect.center = self.hit_rect.center

all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()

# wall1 = Wall(32 * 10, 32 * 10)
# all_sprites.add(wall1)
# walls.add(wall1)
character_sheet = Spritesheet(path.join(art_folder, 'spritesheet_characters'))
map_data = []
with open(path.join(map_folder, 'map4.txt'), 'rt') as datafile:
    for line in datafile:
        map_data.append(line.strip())
for row, tiles in enumerate(map_data):
    for col, tile in enumerate(tiles):
        if tile == '1':
            wall = Wall(col * TILESIZE, row * TILESIZE)
            all_sprites.add(wall)
            walls.add(wall)
        if tile == 'P':
            player = Player(col * TILESIZE, row * TILESIZE)
            all_sprites.add(player)
        if tile == 'm':
            m = Mob(col * TILESIZE, row * TILESIZE, player)
            all_sprites.add(m)

camera = Camera(len(map_data[0]) * TILESIZE, len(map_data) * TILESIZE)
running = True
while running:
    dt = clock.tick(FPS) / 1000
    # input/events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # update
    all_sprites.update(dt)
    camera.update(player)
    # draw
    screen.fill(BLACK)
    #all_sprites.draw(screen)
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite))
    # pygame.draw.rect(screen, WHITE, player.rect, 2)
    # pygame.draw.rect(screen, WHITE, player.hit_rect, 2)
    pygame.display.flip()  # last

pygame.quit()
