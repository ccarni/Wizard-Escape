import pygame.rect
import random
import powerup
import wall
import enemy
import art
import attacks
import numpy as np

class World():
    def __init__(self, runner):
        self.runner = runner
        self.screen = runner.screen
        self.player = runner.player
        self.room_classes = pygame.sprite.Group()
        self.visited_rooms = []
        self.rooms = []

    def set_room(self, room, door):
        self.current_room = room
        self.visited_rooms.append(self.current_room)
        self.runner.update_minimap_position()
        self.player.stamina = self.player.max_stamina

        horizontal_center = self.screen.get_width() / 2
        if door.location == 0:
            self.player.rect.topleft = (horizontal_center - self.player.rect.width / 2, self.screen.get_width() - door.rect.height * 3)
        elif door.location == 1:
            self.player.rect.topleft = (horizontal_center - self.player.rect.width / 2, door.rect.height)
        elif door.location == 2:
            self.player.rect.topleft = (self.screen.get_width() - door.rect.height, horizontal_center - self.player.rect.width / 2)
        elif door.location == 3:
            self.player.rect.topleft = (door.rect.height / 2, horizontal_center - self.player.rect.width / 2)
            
        #projectiles shouldn't carry over between rooms
        self.player.projectiles.empty()

    def make_level(self, filename, tag=None):
        rm = Room(self.screen, self.player, filename, tag)
        self.room_classes.add(rm)
        return rm

    def collide_doors(self, player):
        for door in self.current_room.doors:
            if pygame.rect.Rect.colliderect(player.rect, door.rect):
                self.set_room(door.destination, door)

    # makes finding the index of a room in the list easier
    def find(self, list, item):
        # if not item in list: raise ChildProcessError('Find Function: item not in list')
        for x, y in enumerate(list):
            if item in y:
                return [x, y.index(item)]

    def setup_neighbors(self, room_classes, rooms_layout):

        # setup neighbors
        for room in room_classes:
            index = self.find(rooms_layout, room)
            room.set_neighbors(self.get_neighbors(rooms_layout, index[0], index[1]))

    def get_neighbors(self, rooms, room_index1, room_index2):
        up = rooms[room_index1 - 1][room_index2]
        down = rooms[room_index1 + 1][room_index2]
        left = rooms[room_index1][room_index2 - 1]
        right = rooms[room_index1][room_index2 + 1]
        return [up, down, left, right]

    def update(self, player):
        self.current_room.update()
        if self.current_room.clear:
            self.collide_doors(player)

    def draw(self, cleared):
        self.current_room.draw(self.screen)
        for door in self.current_room.doors:
            pygame.draw.rect(self.screen, door.color if cleared else door.disabled_color, door.rect)

    def make_rooms(self):
        # spawn
        self.rooms.append(R('spn', 'levelspawn'))

        # blank rooms
        for i in range(3):
            self.rooms.append(R(f'br{i + 1}', 'levelspawn'))

        # weapon rooms
        for i in range(3):
            self.rooms.append(R(f'rw{i + 1}', f'levelweapon{i + 1}'))

        # basic rooms
        for i in range(19):
            self.rooms.append(R(f'r{i + 1}', f'level{i + 1}'))

        # win room
        self.rooms.append(R('win', 'level20'))

        # misc
        self.rooms.append(R('9-', 'level9'))
        self.rooms.append(R('14-', 'level14'))

    def get_room(self, name):
        for r in self.rooms:
            if r.name == name:
                return r.data

class R:
    def __init__(self, name, data):
        self.name = name
        self.data = data

class Room(pygame.sprite.Sprite):
    def __init__(self, screen, player, level_path, tag=None):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.player = player
        self.current_path = level_path
        self.tag = tag

        self.clear = False

        self.doors = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.wall_image = self.draw_wall(screen)

        self.neighbors = []

        self.setup_level(self.screen, self.player)

    def setup_level(self, screen, player):
        #CHANGE THIS TO YOUR DIRECTORY \/
        # folder_name = 'WizardEscape'
        with open(f'.\levels\{self.current_path}.txt', 'r') as level:
            block_grid = level.read()

        #splits block grid into multiple strings per line
        block_grid = block_grid.split('\n')
        tilesize = screen.get_width() / 15

        #iterates through the block grid, checks for walls and enemies, and adds them accordingly
        for row in range(len(block_grid)):
            for column in range(len(block_grid[row])):
                #walls
                if block_grid[row][column] == 'w':
                    w = wall.Wall(self.wall_image, column * tilesize, row * tilesize)
                    self.walls.add(w)
                #enemies
                elif block_grid[row][column] == 'e':
                    e = enemy.BasicEnemy(40, 8, screen, player, 10, ((column * tilesize, row * tilesize)))
                    self.enemies.add(e)
                elif block_grid[row][column] == 's':
                    e = enemy.StrongEnemy(40, 10, screen, player, 16, ((column * tilesize, row * tilesize)))
                    self.enemies.add(e)
                elif block_grid[row][column] == 'q':
                    e = enemy.SlowEnemy(30, 3, screen, player, 6, ((column * tilesize, row * tilesize)))
                    self.enemies.add(e)
                #powerups
                elif block_grid[row][column] == 'h':
                    h = powerup.Heart(screen,  art.draw_heart(screen, 60), ((column * tilesize, row * tilesize)))
                    self.powerups.add(h)
                elif block_grid[row][column] == 'g':
                    g = powerup.GoldHeart(screen, art.draw_gold_heart(screen, 60), ((column * tilesize, row * tilesize)))
                    self.powerups.add(g)
                #trophies
                elif block_grid[row][column] == 't':
                    t = powerup.Trophy(screen,  art.draw_trophy(screen, 60), ((column * tilesize, row * tilesize)))
                    self.powerups.add(t)
                #attacks
                elif block_grid[row][column] == 'i':
                    a = powerup.Attack(screen,  art.draw_ice(screen, 60), ((column * tilesize, row * tilesize)), attacks.ice, attacks.ice_cooldown)
                    self.powerups.add(a)
                elif block_grid[row][column] == 'n':
                    a = powerup.Attack(screen,  art.draw_wind(screen, 60), ((column * tilesize, row * tilesize)), attacks.wind, attacks.wind_cooldown)
                    self.powerups.add(a)
                elif block_grid[row][column] == 'l':
                    a = powerup.Attack(screen,  art.draw_leaf(screen, 60), ((column * tilesize, row * tilesize)), attacks.leaf, attacks.leaf_cooldown)
                    self.powerups.add(a)
                elif block_grid[row][column] == 'f':
                    a = powerup.Attack(screen,  art.draw_fireball(screen, 60), ((column * tilesize, row * tilesize)), attacks.fireball, attacks.fireball_cooldown)
                    self.powerups.add(a)
                elif block_grid[row][column] == 'r':
                    a = powerup.Attack(screen,  art.draw_earth(screen, 60), ((column * tilesize, row * tilesize)), attacks.earth, attacks.earth_cooldown)
                    self.powerups.add(a)

    def set_neighbors(self, neighbors):
        self.doors.empty()
        for i in range(4):
            if neighbors[i] != None:
                self.neighbors.append(neighbors[i])
                self.doors.add(Door(i, neighbors[i], self.screen))

    def draw_wall(self, screen):
        wall_surf = pygame.Surface((screen.get_width() / 15, screen.get_width() / 15))
        w_height = wall_surf.get_height()
        w_width = wall_surf.get_width()
        wall_surf.fill((82, 82, 82))
        for i in range(32):
            pygame.draw.circle(wall_surf, (120, 120, 120), (random.randint(int(w_width / 50), int(w_width * 49 / 50)),
                                                            random.randint(int(w_height / 50), int(w_height * 49 / 50))), w_width / 23)
        return wall_surf

    def update(self):
        self.clear = True if len(list(self.enemies)) == 0 else False      

    def draw(self, screen):
        self.powerups.draw(screen)
        for wall in self.walls:
            screen.blit(wall.image, wall.rect.topleft)


class Door(pygame.sprite.Sprite):
    def __init__(self, location, destination, screen, color=(115, 46, 7), disabled_color=(66, 29, 7), width=60, height=20):
        pygame.sprite.Sprite.__init__(self)
        # index 1, 2, 3, 4 correspond to up, down, left, right
        self.location = location
        self.destination = destination
        self.color = color
        self.disabled_color = disabled_color
        self.width = width
        self.height = height

        self.setup_location(screen)
    
    def setup_location(self, screen):
        if self.location == 0:
            self.rect = pygame.rect.Rect(screen.get_width() / 2 - self.width / 2, 0, self.width, self.height)
        elif self.location == 1:
            self.rect = pygame.rect.Rect(screen.get_width() / 2 - self.width / 2, screen.get_height() - self.height, self.width, self.height)
        elif self.location == 2:
            self.rect = pygame.rect.Rect(0, screen.get_height() / 2 - self.height * 1.5, self.height, self.width)
        else:
            self.rect = pygame.rect.Rect(screen.get_width() - self.height, screen.get_height() / 2 - self.height * 1.5, self.height, self.width)


class World1(World):
    def __init__(self, runner):
        World.__init__(self, runner)

        self.make_rooms()

        # convert room data into a room
        for r in self.rooms:
            r.data = self.make_level(r.data)

        # simplified so it takes up less space and looks better
        g = self.get_room

        self.map = [
         [None,     None,     None,     None,     None,     None,     None,     None,     None,     None,     None],
         [None,     None,     g('rw1'), None,     None,     None,     None,     None,     None,     None,     None],
         [None,     None,     g('r9'),  None,     None,     None,     None,     None,     None,     None,     None],
         [None,     None,     g('r6'),  None,     None,     g('r17'), g('r14'), g('br2'), g('br3'), None,     None],
         [None,     None,     g('r3'),  None,     None,     g('r16'), None,     None,     g('r18'), None,     None],
         [None,     g('r1'),  g('r2'),  g('r4'),  None,     g('r15'), None,     None,     g('r19'), g('br1'), None],
         [None,     g('spn'), None,     g('r5'),  None,     g('14-'), g('r13'), g('rw3'), None,     g('win'), None],
         [None,     None,     None,     g('r7'),  None,     g('r12'), None,     None,     None,    None,      None],
         [None,     g('rw2'), g('r11'), g('r8'),  g('9-'),  g('r10'), None,     None,     None,    None,      None],
         [None,     None,     None,     None,     None,     None,     None,     None,     None,    None,      None]]

        # nicely formatted line
        # [None,     None,     None,     None,     None,     None,     None,     None,     None,     None,     None],

        self.setup_neighbors(self.room_classes, self.map)

        # sets the starting room
        self.current_room = g('spn')
        self.visited_rooms.append(self.current_room)
