import pygame as pg
from os import path
game_folder = path.dirname(__file__)

MASS = 1
MAX_SPEED = 300
STEER_FORCE = 100
APPROACH_RADIUS = 100

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
        
    def seek(self, target):
        self.desired = (target - self.pos).normalize() * MAX_SPEED
        steer = self.desired - self.vel
        if steer.length() > STEER_FORCE:
            steer.scale_to_length(STEER_FORCE)
        self.apply_force(steer)
        
    def seek_with_approach(self, target):
        distance = (target - self.pos).length()
        self.desired = (target - self.pos).normalize()
        if distance < APPROACH_RADIUS:
            self.desired *= distance / APPROACH_RADIUS * MAX_SPEED
        else:
            self.desired *= MAX_SPEED
        steer = self.desired - self.vel
        if steer.length() > STEER_FORCE:
            steer.scale_to_length(STEER_FORCE)
        self.apply_force(steer)
        
    def draw_vectors(self, screen):
        scale = .25
        pg.draw.line(screen, (0, 255, 0), self.pos, (self.pos + self.vel * scale), 5)
        pg.draw.line(screen, (255, 0, 0), self.pos, (self.pos + self.desired * scale), 5)
        pg.draw.line(screen, (255, 255, 0), self.pos, (self.pos + self.acc * scale), 5)
        pg.draw.circle(screen, (255, 255, 255), pg.mouse.get_pos(), APPROACH_RADIUS, 1)
        
    def update(self, delta):
        self.acc = vec2(0, 0)
        #self.apply_force(vec2(0, 10))
        self.seek_with_approach(pg.mouse.get_pos())
        self.vel += self.acc * delta
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.image = pg.transform.rotate(self.image_orig, self.vel.angle_to(vec2(1, 0)))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.pos += self.vel * delta
        self.rect.center = self.pos
