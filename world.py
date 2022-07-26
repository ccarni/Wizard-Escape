import pygame.rect
import random
import powerup
import wall
import enemy
import art
import attacks


class World():
    def __init__(self, runner):
        self.runner = runner
        self.screen = runner.screen
        self.player = runner.player

    def set_room(self, room, door):
        self.current_room = room

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
        print(room.current_path)


    def make_level(self, filename):
        return Room(self.screen, self.player, filename, neighbors=['up', 'down', 'left', 'right'])

    def collide_doors(self, player):
        for door in self.current_room.doors:
            if pygame.rect.Rect.colliderect(player.rect, door.rect):
                self.set_room(door.destination, door)

    def setup_neighbors(self, room_classes, rooms_layout):

        # makes finding the index of a room in the list easier
        def find(list, item):
            for i in range(len(list[0])):
                for j in range(len(list[i])):
                    if list[i][j] == item:
                        return [i, j]

        # setup neighbors
        for room in room_classes:
            index = find(rooms_layout, room)
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


class Room(pygame.sprite.Sprite):
    def __init__(self, screen, player, level_path, neighbors=['up', 'down', 'left', 'right']):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.player = player
        self.current_path = level_path

        self.clear = False

        self.doors = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.wall_image = self.draw_wall(screen)

        self.set_neighbors(neighbors)
        self.setup_level(self.screen, self.player)

    def setup_level(self, screen, player):
        #CHANGE THIS TO YOUR DIRECTORY \/
        folder_name = 'Wizard Escape v1.2.5'
        with open(f'../{folder_name}/levels/{self.current_path}.txt', 'r') as level:
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
                    e = enemy.Enemy0(40, screen, player, 10, ((column * tilesize, row * tilesize)))
                    self.enemies.add(e)
                #powerups
                elif block_grid[row][column] == 'h':
                    h = powerup.Heart(screen,  art.draw_heart(screen, 60), ((column * tilesize, row * tilesize)))
                    self.powerups.add(h)
                #trophies
                elif block_grid[row][column] == 't':
                    t = powerup.Trophy(screen,  art.draw_trophy(screen, 60), ((column * tilesize, row * tilesize)))
                    self.powerups.add(t)

    def set_neighbors(self, neighbors):
        self.doors.empty()
        for i in range(4):
            if neighbors[i] != None:
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

        self.room_classes = pygame.sprite.Group()

        # make rooms
        self.start_room = self.make_level('levelspawn')
        self.blank_room = self.make_level('levelspawn')
        self.blank_room2 = self.make_level('levelspawn')
        self.blank_room3 = self.make_level('levelspawn')
        self.roomw1 = self.make_level('levelweapon1')
        self.roomw2 = self.make_level('levelweapon2')
        self.room1 = self.make_level('level1')
        self.room2 = self.make_level('level2')
        self.room3 = self.make_level('level3')
        self.room4 = self.make_level('level4')
        self.room5 = self.make_level('level5')
        self.room6 = self.make_level('level6')
        self.room7 = self.make_level('level7')
        self.room8 = self.make_level('level8')
        self.room9 = self.make_level('level9')
        self.room9_2 = self.make_level('level9')
        self.room10 = self.make_level('level10')
        self.room11 = self.make_level('level11')
        self.room12 = self.make_level('level12')
        self.room13 = self.make_level('level13')
        self.room14 = self.make_level('level14')
        self.room14_2 = self.make_level('level14')
        self.room15 = self.make_level('level15')
        self.room16 = self.make_level('level16')
        self.room17 = self.make_level('level17')
        self.room18 = self.make_level('level18')
        self.room19 = self.make_level('level19')
        self.roomwin = self.make_level('level20')

        # add them to the room_classes group
        self.room_classes.add(self.start_room)
        self.room_classes.add(self.blank_room)
        self.room_classes.add(self.blank_room2)
        self.room_classes.add(self.blank_room3)
        self.room_classes.add(self.room1)
        self.room_classes.add(self.room2)
        self.room_classes.add(self.room3)
        self.room_classes.add(self.room4)
        self.room_classes.add(self.room5)
        self.room_classes.add(self.room6)
        self.room_classes.add(self.room7)
        self.room_classes.add(self.room8)
        self.room_classes.add(self.room9)
        self.room_classes.add(self.room9_2)
        self.room_classes.add(self.room10)
        self.room_classes.add(self.room11)
        self.room_classes.add(self.room12)
        self.room_classes.add(self.room13)
        self.room_classes.add(self.room14)
        self.room_classes.add(self.room14_2)
        self.room_classes.add(self.room15)
        self.room_classes.add(self.room16)
        self.room_classes.add(self.room17)
        self.room_classes.add(self.room18)
        self.room_classes.add(self.room19)
        self.room_classes.add(self.roomwin)
        self.room_classes.add(self.roomw1)
        self.room_classes.add(self.roomw2)

        # tells the game how to layout rooms
        self.rooms_layout = [[None, None, None, None, None, None, None, None, None, None, None],
                             [None, None, self.roomw1, None, None, None, None, None, None, None, None],
                             [None, None, self.room9, None, None, None, None, None, None, None, None],
                             [None, None, self.room6, None, None, self.room17, self.room14, self.blank_room2, self.blank_room3, None, None],
                             [None, None, self.room3, None, None, self.room16, None, None, self.room18, None, None],
                             [None, self.room1, self.room2, self.room4, None, self.room15, None, None, self.room19, self.blank_room, None],
                             [None, self.start_room, None, self.room5, None, self.room14_2, self.room13, None, None, self.roomwin, None],
                             [None, None, None, self.room7, None, self.room12, None, None, None, None, None],
                             [None, self.roomw2, self.room11, self.room8, self.room9_2, self.room10, None, None, None, None, None],
                             [None, None, None, None, None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None, None, None, None, None]]

        self.setup_neighbors(self.room_classes, self.rooms_layout)

        # sets the starting room
        self.current_room = self.start_room

