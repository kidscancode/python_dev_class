import pygame
from settings import *
from sprites import *
from tools import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Adventure!")
        self.clock = pygame.time.Clock()
        self.load_data()

    def load_data(self):
        self.game_folder = game_folder
        self.art_folder = art_folder
        self.map_folder = map_folder
        self.character_sheet = Spritesheet(path.join(art_folder, 'spritesheet_characters'))

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.map_data = []
        with open(path.join(self.map_folder, 'map4.txt'), 'rt') as datafile:
            for line in datafile:
                self.map_data.append(line.strip())
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    wall = Wall(col * TILESIZE, row * TILESIZE)
                    self.all_sprites.add(wall)
                    self.walls.add(wall)
                if tile == 'P':
                    self.player = Player(self, col * TILESIZE, row * TILESIZE)
                    self.all_sprites.add(self.player)
                if tile == 'm':
                    m = Mob(self, col * TILESIZE, row * TILESIZE, self.player)
                    self.all_sprites.add(m)
                    self.mobs.add(m)
        self.camera = Camera(len(self.map_data[0]) * TILESIZE, len(self.map_data) * TILESIZE)

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        # input/events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False

    def update(self):
        # update
        self.all_sprites.update(self.dt)
        self.camera.update(self.player)
        # check if player hits mobs
        mob_hits = pygame.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for mob in mob_hits:
            self.player.health -= MOB_DAMAGE
            mob.pos -= 2 * mob.vel * self.dt
        if mob_hits:
            self.player.pos += vec2(MOB_KNOCKBACK, 0).rotate(-mob_hits[0].rot)
        if self.player.health <= 0:
            self.playing = False

    def draw(self):
        # draw
        self.screen.fill(BLACK)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pygame.display.flip()  # last

g = Game()
g.running = True
while g.running:
    g.new()
    g.run()
    # g.show_game_over()

pygame.quit()
