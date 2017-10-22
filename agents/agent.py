import pygame as pg
from os import path
from random import randrange
game_folder = path.dirname(__file__)

MASS = 1
MAX_SPEED = 200
STEER_FORCE = 800
APPROACH_RADIUS = 200
WANDER_RING_RADIUS = 150
WANDER_RING_DISTANCE = 151
DETECT_RADIUS = 100

vec2 = pg.math.Vector2
class Agent(pg.sprite.Sprite):
    # for:  how: limitations: 
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(path.join(game_folder, '../arrowRight.png'))
        self.image_orig = self.image.copy()
        self.rect = self.image.get_rect()
        self.pos = vec2(x, y)
        self.vel = vec2(100, 0)
        self.acc = vec2(0, 0)
        self.mass = 1
        self.wander_angle = 0
        self.screen_width = w
        self.screen_height = h

    def apply_force(self, force):
        acc = force / self.mass
        self.acc += acc

    def seek(self, target):
        self.desired = (target - self.pos).normalize() * MAX_SPEED
        steer = self.desired - self.vel
        if steer.length() > STEER_FORCE:
            steer.scale_to_length(STEER_FORCE)
        self.apply_force(steer)
    
    def find_neighbors(self):
        neighbors = []
        for agent in all_sprites:
            if agent != self:
                if self.pos.distance_to(agent.pos) < DETECT_RADIUS:
                    neighbors.append(agent)
        return neighbors
        
    def wander(self):
        target = self.pos + self.vel.normalize() * WANDER_RING_DISTANCE
        self.wander_angle += randrange(-45, 46)
        circle_pos = self.vel.normalize().rotate(self.wander_angle) * WANDER_RING_RADIUS
        target += circle_pos
        self.seek(target)

    def seek_with_approach(self, target):
        distance = (target - self.pos).length()
        self.desired = (target - self.pos).normalize()
        if distance < APPROACH_RADIUS:
            self.desired *= (distance / APPROACH_RADIUS) * MAX_SPEED
        else:
            self.desired *= MAX_SPEED
        steer = self.desired - self.vel
        if steer.length() > STEER_FORCE:
            steer.scale_to_length(STEER_FORCE)
        self.apply_force(steer)
        
    def draw_vectors(self, screen):
        # set scale to .25
        scale = .25
        pg.draw.line(screen, (0, 255, 0), self.pos, (self.pos + self.vel * scale), 5)
        pg.draw.line(screen, (255, 0, 0), self.pos, (self.pos + self.desired * scale), 5)
        pg.draw.line(screen, (255, 255, 0), self.pos, (self.pos + self.acc * scale), 5)
        #pg.draw.circle(screen, (255, 255, 255), pg.mouse.get_pos(), APPROACH_RADIUS, 1)
        pg.draw.circle(screen, (255, 255, 255), self.rect.center, DETECT_RADIUS, 1)

    def update(self, delta):
        neighbors = self.find_neighbors()
        self.acc = vec2(0, 0)
        #self.apply_force(vec2(0, 10))
        #self.seek_with_approach(pg.mouse.get_pos())
        self.wander()
        self.vel += self.acc * delta
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.image = pg.transform.rotate(self.image_orig, self.vel.angle_to(vec2(1, 0)))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.pos += self.vel * delta
        self.pos.x = self.pos.x % self.screen_width
        self.pos.y = self.pos.y % self.screen_height
        self.rect.center = self.pos
