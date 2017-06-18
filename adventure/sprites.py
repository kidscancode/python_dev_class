import pygame
from settings import *
from tools import *
vec2 = pygame.math.Vector2

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, pos, dir):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((5, 5))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec2(pos)
        self.rect.center = pos
        self.vel = vec2(BULLET_SPEED, 0).rotate(dir)
        self.spawn_time = pygame.time.get_ticks()
        self.damage = BULLET_DAMAGE

    def update(self, dt):
        self.pos += self.vel * dt
        self.rect.center = self.pos
        if pygame.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()
        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, game, x, y, target):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        #self.image = pygame.Surface((TILESIZE//1.2, TILESIZE//1.2 ))
        self.image = game.character_sheet.get_image_by_name('robot1_gun.png')
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
        self.health = MOB_HEALTH

    def draw_health(self):
        pct = self.health / MOB_HEALTH
        if pct > 0.6:
            col = GREEN
        elif pct > 0.3:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * pct)
        bar = pygame.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pygame.draw.rect(self.image, col, bar)

    def update(self, dt):
        if self.health <= 0:
            self.kill()
        dir_vector = (self.target.pos - self.pos).normalize()
        self.rot = dir_vector.angle_to(vec2(1, 0))
        self.image = pygame.transform.rotate(self.image_clean, self.rot)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.vel = dir_vector * MOB_SPEED
        self.pos += self.vel * dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        #self.image = pygame.Surface((TILESIZE//1.2, TILESIZE//1.2 ))
        self.image = game.character_sheet.get_image_by_name('manBlue_gun.png')
        self.image_clean = self.image.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, 35, 35)
        self.pos = vec2(x, y)
        self.vel = vec2(0, 0)
        self.acc = vec2(0, 0)
        self.rot = 0
        self.rect.center = self.pos
        self.hit_rect.center = self.rect.center
        self.health = PLAYER_HEALTH
        self.last_shot = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > FIRE_RATE:
            self.last_shot = now
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            self.vel = vec2(-KICKBACK, 0).rotate(-self.rot)
            b = Bullet(self.game, pos, -self.rot)
            self.game.all_sprites.add(b)
            self.game.bullets.add(b)

    def update(self, dt):
        self.acc = vec2(0, 0)
        self.rot_speed = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_LEFT]:
            self.rot_speed = 200
        if keys[pygame.K_RIGHT]:
            self.rot_speed = -200
        if keys[pygame.K_UP]:
            self.acc = vec2(PLAYER_ACCEL, 0).rotate(-self.rot)
        if keys[pygame.K_DOWN]:
            self.acc = vec2(-PLAYER_ACCEL / 2, 0).rotate(-self.rot)
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
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
