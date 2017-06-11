import pygame
from os import path
vec2 = pygame.math.Vector2

game_folder = path.dirname(__file__)
map_folder = path.join(game_folder, 'maps')
art_folder = path.join(game_folder, 'art')

WIDTH = 800
HEIGHT = 640
FPS = 60
TILESIZE = 64
PLAYER_ACCEL = 5000  # pixels/sec
FRICTION = -15
PLAYER_HEALTH = 100
FIRE_RATE = 250
BARREL_OFFSET = vec2(30, 10)

MOB_SPEED = 200
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20

BULLET_SPEED = 500
BULLET_LIFETIME = 1000
KICKBACK = 100

BLACK = (80, 80, 80)
WHITE = (255, 255, 255)
BLUE = (55, 121, 179)
RED = (255, 84, 76)
YELLOW = (221, 232, 63)
