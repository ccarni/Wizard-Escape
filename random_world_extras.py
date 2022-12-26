import world
import random_world
import random

# archive

class Strict(random_world.RandomWorld):
    def __init__(self, runner, width, height):
        random_world.RandomWorld.__init__(self, runner, width, height)

        R = world.R

        self.rooms = []
        self.spn = None
        self.pwp = []
        self.win = None
        self.bsc = []
        self.ctr = None

        self.make_rooms()


        # convert room data into a room
        for room in self.rooms:
            room.data = self.make_level(room.data)

        print(self.make_rooms())

        self.map = [
            [ None, 'w', None, None, None, None, None, None, None],
            [ None, 'b', None, None, None, None, None, None, None],
            [ None, 'b', None, None, None, None, None, None, None],
            [ None, 'b', None, None, 'b', 'b', 'b', 'b', None],
            [ 'b', 'b', 'b', None, 'b', None, None, 'b', 'b'],
            [ 's', None, 'b', None, 'b', 'b', 'b', None, 't'],
            [ None, None, 'b', 'b', 'b', None, None, None, None],
            ['w', 'b', 'b', 'b', 'b', None, None, None, None]]

        #fill rooms
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                if not self.map[row][col] == None:
                    if self.map[row][col] == 's':
                        self.map[row][col] = self.spn
                    elif self.map[row][col] == 'b':
                        length = len(self.bsc)
                        if length == 0: raise ChildProcessError('Not enough basic rooms implemented')
                        else: self.map[row][col] = self.bsc.pop(random.randrange(0, length - 1))
                    elif self.map[row][col] == 'w':
                        length = len(self.pwp)
                        if length == 0: raise ChildProcessError('Not enough powerup rooms implemented')
                        else: self.map[row][col] = self.pwp.pop(random.randrange(0, length - 1))
                    elif self.map[row][col] == 't':
                        self.map[row][col] = self.win

        self.finish_map()



class Random(random_world.RandomWorld):
    def __init__(self, runner, width, height):
        random_world.RandomWorld.__init__(self, runner, width, height)

        R = world.R

        self.rooms = []
        self.spn = None
        self.pwp = []
        self.win = None
        self.bsc = []

        def make_rooms():
            # spawn
            r = R('spn', 'levelspawn')
            self.rooms.append(r)
            self.spn = self.get_full_room('spn')

            # blank rooms
            for i in range(3):
                r = R(f'br{i + 1}', 'levelspawn')
                self.rooms.append(r)
                self.bsc.append(r)

            # weapon rooms
            for i in range(3):
                r = R(f'rw{i + 1}', f'levelweapon{i + 1}')
                self.rooms.append(r)
                self.pwp.append(r)

            # basic rooms
            for i in range(19):
                r = R(f'r{i + 1}', f'level{i + 1}')
                self.rooms.append(r)
                self.bsc.append(r)

            # win room
            r = R('win', 'level20')
            self.rooms.append(r)
            self.win = self.get_full_room('win')

        make_rooms()

        # convert room data into a room
        for room in self.rooms:
            room.data = self.make_level(room.data)

        # random positions on the map
        def random_position():
            return [random.randrange(0, self.width), random.randrange(0, self.height)]

        positions = []
        for i in range(4):
            positions.append(random_position())

        # grabs a random position for each point of interest
        win_pos = positions.pop(random.randrange(0, len(positions)))
        spawn_pos = positions.pop(random.randrange(0, len(positions)))
        powerup_1 = positions.pop(random.randrange(0, len(positions)))
        powerup_2 = positions.pop(random.randrange(0, len(positions)))

        self.map = [[None for i in range(self.width)] for j in range(self.height)]

        # make 'lines' between rooms of interest
        extras = []  # this makes sure no "islands" appear as a result of 2 points of interest being next to each other
        s1 = self.make_line_between(self.map, spawn_pos[0], spawn_pos[1], powerup_1[0], powerup_1[1])
        s2 = self.make_line_between(self.map, spawn_pos[0], spawn_pos[1], powerup_2[0], powerup_2[1])
        w1 = self.make_line_between(self.map, powerup_1[0], powerup_1[1], win_pos[0], win_pos[1])
        w2 = self.make_line_between(self.map, powerup_2[0], powerup_2[1], win_pos[0], win_pos[1])

        # add extra lines if rooms of interest are next to each other
        if (not 1 in s1) or (not 1 in s2):
            extras.append(self.make_line_between(self.map, powerup_1[0], powerup_1[1], powerup_2[0], powerup_2[1]))
        if (not 1 in w1):
            extras.append(self.make_line_between(self.map, spawn_pos[0], spawn_pos[1], powerup_1[0], powerup_1[1]))
        if (not 1 in w2):
            extras.append(self.make_line_between(self.map, spawn_pos[0], spawn_pos[1], powerup_2[0], powerup_2[1]))

        # setup important rooms
        self.map[spawn_pos[0]][spawn_pos[1]] = self.spn
        self.map[win_pos[0]][win_pos[1]] = self.win
        self.map[powerup_1[0]][powerup_1[1]] = self.pwp.pop(random.randrange(0, len(self.pwp) - 1))
        self.map[powerup_2[0]][powerup_2[1]] = self.pwp.pop(random.randrange(0, len(self.pwp) - 1))

        # fill lines between rooms of interest with rooms
        for y in range(len(s1)):
            for x in range(len(s1[y])):
                if len(self.bsc) < 2:
                    raise ChildProcessError('map too large for how many rooms implemented')
                if s1[y][x] == 1 or (s1[y][x] == 2 and self.map[y][x] == None):
                    self.map[y][x] = (self.bsc.pop(random.randrange(0, len(self.bsc) - 1, 1)))
                elif s2[y][x] == 1 or (s2[y][x] == 2 and self.map[y][x] == None):
                    self.map[y][x] = (self.bsc.pop(random.randrange(0, len(self.bsc) - 1, 1)))
                elif w1[y][x] == 1 or (w1[y][x] == 2 and self.map[y][x] == None):
                    self.map[y][x] = (self.bsc.pop(random.randrange(0, len(self.bsc) - 1, 1)))
                elif w2[y][x] == 1 or (w2[y][x] == 2 and self.map[y][x] == None):
                    self.map[y][x] = (self.bsc.pop(random.randrange(0, len(self.bsc) - 1, 1)))
                # else:
                    for extra in extras:
                        if extra[y][x] == 1:
                            self.map[y][x] = (self.bsc.pop(random.randrange(0, len(self.bsc) - 1, 1)))

        self.finish_map()


class QuadCenter(random_world.RandomWorld):
    def __init__(self, runner, width, height):
        random_world.RandomWorld.__init__(self, runner, width, height)

        R = world.R

        self.rooms = []
        self.spn = None
        self.pwp = []
        self.win = None
        self.bsc = []
        self.ctr = None

        def make_rooms():
            # spawn
            r = R('spn', 'levelspawn')
            self.rooms.append(r)
            self.spn = self.get_full_room('spn')

            # blank rooms
            for i in range(3):
                r = R(f'br{i + 1}', 'levelspawn')
                self.rooms.append(r)
                self.bsc.append(r)

            # weapon rooms
            for i in range(3):
                r = R(f'rw{i + 1}', f'levelweapon{i + 1}')
                self.rooms.append(r)
                self.pwp.append(r)

            # basic rooms
            for i in range (19):
                r = R(f'r{i + 1}', f'level{i + 1}')
                self.rooms.append(r)
                self.bsc.append(r)

            # win room
            r = R('win', 'level20')
            self.rooms.append(r)
            self.win = self.get_full_room('win')

            # misc
            r = R('ctr', 'center1')
            self.rooms.append(r)
            self.ctr = self.get_full_room('ctr')

        make_rooms()

        # convert room data into a room
        for room in self.rooms:
            room.data = self.make_level(room.data)

        #random positions in corresponding quadrants 1, 2, 3, and 4
        p1 = [random.randrange((self.width / 2), self.width), random.randrange(0, (self.height / 2))]
        p2 = [random.randrange(0, (self.width / 2)), random.randrange(0, (self.height / 2))]
        p3 = [random.randrange(0, (self.width / 2)), random.randrange((self.height / 2), self.height)]
        p4 = [random.randrange((self.width / 2), self.width), random.randrange((self.height / 2), self.height)]
        pc = [random.randrange(((self.width / 2) - 1), (self.width / 2) + 1), random.randrange(((self.height / 2) - 1), (self.height / 2) + 1)]

        positions = [p1, p2, p3, p4]
        #grabs a random quadrant
        spawn_index = random.randint(0, len(positions) - 1)

        #puts positions in the right quadrants
        win_pos = positions[spawn_index - 2]
        spawn_pos = positions[spawn_index]
        powerup_1 = positions[spawn_index - 3]
        powerup_2 = positions[spawn_index - 1]

        self.map = [[None for i in range(self.width)] for j in range(self.height)]

        #make 'lines' between rooms of interest
        extras = [] #this makes sure no "islands" appear as a result of 2 points of interest being next to each other
        s1 = self.make_line_between(self.map, spawn_pos[0], spawn_pos[1], powerup_1[0], powerup_1[1])
        s2 = self.make_line_between(self.map, spawn_pos[0], spawn_pos[1], powerup_2[0], powerup_2[1])
        w1 = self.make_line_between(self.map, powerup_1[0], powerup_1[1], win_pos[0], win_pos[1])
        w2 = self.make_line_between(self.map, powerup_2[0], powerup_2[1], win_pos[0], win_pos[1])
        sc1 = self.make_line_between(self.map, pc[0], pc[1], powerup_1[0], powerup_1[1])
        sc2 = self.make_line_between(self.map, pc[0], pc[1], powerup_2[0], powerup_2[1])

        #add extra lines if rooms of interest are next to each other
        if (not 1 in s1) or (not 1 in s2):
            extras.append(self.make_line_between(self.map, powerup_1[0], powerup_1[1], powerup_2[0], powerup_2[1]))
        if (not 1 in w1):
            extras.append(self.make_line_between(self.map, spawn_pos[0], spawn_pos[1], powerup_1[0], powerup_1[1]))
        if (not 1 in w2):
            extras.append(self.make_line_between(self.map, spawn_pos[0], spawn_pos[1], powerup_2[0], powerup_2[1]))


        # setup important rooms
        self.map[spawn_pos[0]][spawn_pos[1]] = self.spn
        self.map[win_pos[0]][win_pos[1]] = self.win
        self.map[powerup_1[0]][powerup_1[1]] = self.pwp.pop(random.randrange(0, len(self.pwp) - 1))
        self.map[powerup_2[0]][powerup_2[1]] = self.pwp.pop(random.randrange(0, len(self.pwp) - 1))
        self.map[pc[0]][pc[1]] = self.ctr

        #fill lines between rooms of interest with rooms
        for y in range(len(s1)):
            for x in range(len(s1[y])):
                if len(self.bsc) < 2:
                    raise ChildProcessError('map too large for how many rooms implemented')
                if s1[y][x] == 1 or (s1[y][x] == 2 and self.map[y][x] == None):
                    self.map[y][x] = (self.bsc.pop(random.randrange(0, len(self.bsc) - 1, 1)))
                elif s2[y][x] == 1 or (s2[y][x] == 2 and self.map[y][x] == None):
                    self.map[y][x] = (self.bsc.pop(random.randrange(0, len(self.bsc) - 1, 1)))
                elif w1[y][x] == 1 or (w1[y][x] == 2 and self.map[y][x] == None):
                    self.map[y][x] = (self.bsc.pop(random.randrange(0, len(self.bsc) - 1, 1)))
                elif w2[y][x] == 1 or (w2[y][x] == 2 and self.map[y][x] == None):
                    self.map[y][x] = (self.bsc.pop(random.randrange(0, len(self.bsc) - 1, 1)))
                elif sc1[y][x] == 1 or (sc1[y][x] == 2 and self.map[y][x] == None):
                    self.map[y][x] = (self.bsc.pop(random.randrange(0, len(self.bsc) - 1, 1)))
                elif sc2[y][x] == 1 or (sc2[y][x] == 2 and self.map[y][x] == None):
                    self.map[y][x] = (self.bsc.pop(random.randrange(0, len(self.bsc) - 1, 1)))
                else:
                    for extra in extras:
                        if extra[y][x] == 1:
                            self.map[y][x] = (self.bsc.pop(random.randrange(0, len(self.bsc) - 1, 1)))

        self.finish_map()