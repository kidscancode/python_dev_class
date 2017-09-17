import pygame as pg
from os import path
game_folder = path.dirname(__file__)

MASS = 1
MAX_SPEED = 300

vec2 = pg.math.Vector2
class Agent(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(path.join(game_folder, '../arrowRight.png'))
        self.image_orig = self.image.copy()
        self.rect = self.image.get_rect()
        self.pos = vec2(x, y)
        self.vel = vec2(100, 0)
        self.acc = vec2(0, 0)
        self.mass = 1
        
    def apply_force(self, force):
        acc = force / self.mass
        self.acc += acc
        
    def update(self, delta):
        self.apply_force(vec2(0, 10))
        self.vel += self.acc * delta
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.image = pg.transform.rotate(self.image_orig, self.vel.angle_to(vec2(1, 0)))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.pos += self.vel * delta
        self.rect.center = self.pos
        
