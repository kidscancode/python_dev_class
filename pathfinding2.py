import pygame as pg
from os import path
import heapq

TILESIZE = 32
GRIDWIDTH = 28
GRIDHEIGHT = 15
WIDTH = TILESIZE * GRIDWIDTH
HEIGHT = TILESIZE * GRIDHEIGHT

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (14, 183, 63)
BLUE = (55, 121, 179)
RED = (255, 84, 76)
YELLOW = (221, 232, 63)
DARKGRAY = (40, 40, 40)
LIGHTGRAY = (100, 100, 100)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
vec2 = pg.math.Vector2

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.connections = [vec2(1, 0), vec2(-1, 0), vec2(0, 1), vec2(0, -1)]
        self.connections += [vec2(1, 1), vec2(1, -1), vec2(-1, 1), vec2(-1, -1)]

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def passable(self, node):
        return node not in self.walls

    def find_neighbors(self, node):
        neighbors = [node + conn for conn in self.connections]
        if (node.x + node.y) % 2:
            neighbors.reverse()
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return neighbors

    def draw(self):
        for wall in self.walls:
            rect = pg.Rect(wall * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(screen, LIGHTGRAY, rect)

class WeightedGrid(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        if (vec2(from_node) - vec2(to_node)).length_squared() == 1:
            return self.weights.get(to_node, 0) + 10
        else:
            return self.weights.get(to_node, 0) + 14

class PriorityQueue:
    def __init__(self):
        self.nodes = []

    def put(self, node, cost):
        heapq.heappush(self.nodes, (cost, node))

    def get(self):
        return heapq.heappop(self.nodes)[1]

    def empty(self):
        return len(self.nodes) == 0

def vec2int(v):
    return(int(v.x), int(v.y))

def dijkstra_search(graph, start, end):
    frontier = PriorityQueue()
    frontier.put(vec2int(start), 0)
    path = {}
    cost = {}
    path[vec2int(start)] = None
    cost[vec2int(start)] = 0
    while not frontier.empty():
        current = frontier.get()
        if current == end:
            break
        for next_node in graph.find_neighbors(vec2(current)):
            next_node = vec2int(next_node)
            next_cost = cost[current] + graph.cost(current, next_node)
            if next_node not in cost or next_cost < cost[next_node]:
                cost[next_node] = next_cost
                priority = next_cost
                frontier.put(next_node, priority)
                path[next_node] = vec2(current) - vec2(next_node)
    return path


folder = path.dirname(__file__)
arrows = {}
arrow_img = pg.image.load(path.join(folder, 'arrowRight.png')).convert_alpha()
arrow_img = pg.transform.scale(arrow_img, (TILESIZE, TILESIZE))
for dir in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
    arrows[dir] = pg.transform.rotate(arrow_img, vec2(dir).angle_to(vec2(1, 0)))

g = WeightedGrid(GRIDWIDTH, GRIDHEIGHT)
walls = [(10, 7), (11, 7), (12, 7), (13, 7), (14, 7), (15, 7), (16, 7), (7, 7), (6, 7), (5, 7), (5, 5), (5, 6), (1, 6), (2, 6), (3, 6), (5, 10), (5, 11), (5, 12), (5, 9), (5, 8), (12, 8), (12, 9), (12, 10), (12, 11), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10), (17, 7), (18, 7), (21, 7), (21, 6), (21, 5), (21, 4), (21, 3), (22, 5), (23, 5), (24, 5), (25, 5), (18, 10), (20, 10), (19, 10), (21, 10), (22, 10), (23, 10), (14, 4), (14, 5), (14, 6), (14, 0), (14, 1), (9, 2), (9, 1), (7, 3), (8, 3), (10, 3), (9, 3), (11, 3), (2, 5), (2, 4), (2, 3), (2, 2), (2, 0), (2, 1), (0, 11), (1, 11), (2, 11), (21, 2), (20, 11), (20, 12), (23, 13), (23, 14), (24, 10), (25, 10), (6, 12), (7, 12), (10, 12), (11, 12), (12, 12), (5, 3), (6, 3), (5, 4)]
for wall in walls:
    g.walls.append(vec2(wall))
start = vec2(14, 8)
end = vec2(14, 10)
path = dijkstra_search(g, start, end)

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (0, y), (WIDTH, y))

running = True
while running:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_m:
            print([(int(loc.x), int(loc.y)) for loc in g.walls])
        if event.type == pg.MOUSEBUTTONDOWN:
            mpos = vec2(pg.mouse.get_pos()) // TILESIZE
            if event.button == 1:
                if mpos in g.walls:
                    g.walls.remove(mpos)
                else:
                    g.walls.append(mpos)
            if event.button == 3:
                start = mpos
            path = dijkstra_search(g, start, end)
    screen.fill(DARKGRAY)
    # fill explored area
    for node in path:
        x, y = node
        rect = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
        pg.draw.rect(screen, (75, 75, 75), rect)
    draw_grid()
    g.draw()
    # draw path
    current = end + path[vec2int(end)]
    while current != start:
        x, y = current
        x = x * TILESIZE + TILESIZE / 2
        y = y * TILESIZE + TILESIZE / 2
        img = arrows[vec2int(path[(current.x, current.y)])]
        r = img.get_rect(center=(x, y))
        screen.blit(img, r)
        current = current + path[vec2int(current)]
    start_center = (int(start.x*TILESIZE+TILESIZE/2), int(start.y*TILESIZE+TILESIZE/2))
    pg.draw.circle(screen, RED, start_center, TILESIZE//2)
    end_center = (int(end.x*TILESIZE+TILESIZE/2), int(end.y*TILESIZE+TILESIZE/2))
    pg.draw.circle(screen, GREEN, end_center, TILESIZE//2)
    pg.display.flip()

pg.quit()
