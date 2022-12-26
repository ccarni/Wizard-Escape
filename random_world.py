import world
import random
import numpy as np

class RandomWorld(world.World):
    # returns a line on a grid between two points
    def make_line_between(self, mat, x, y):
        x0, y0, x1, y1 = x[0], x[1], y[0], y[1]
        pts = np.array(list(mat.copy()))
        if not (0 <= x0 <= pts.shape[0] and 0 <= x1 <= pts.shape[0] and
                0 <= y0 <= pts.shape[1] and 0 <= y1 <= pts.shape[1]):
            raise ValueError('Invalid coordinates.')
        if (x0, y0) == (x1, y1):
            pts[x0, y0] = 2
            return pts
        # Swap axes if Y slope is smaller than X slope
        transpose = abs(x1 - x0) < abs(y1 - y0)
        if transpose:
            pts = pts.T
            x0, y0, x1, y1 = y0, x0, y1, x1
        # Swap line direction to go left-to-right if necessary
        if x0 > x1:
            x0, y0, x1, y1 = x1, y1, x0, y0
        # Compute intermediate coordinates using line equation
        prev_y = -100
        for x in range(x0, x1 + 1):
            y = round(((y1 - y0) / (x1 - x0)) * (x - x0) + y0)
            if (y != prev_y) and (prev_y != -100):
                pts[x, prev_y] = 1
            pts[x, y] = 1
            prev_y = y
        # Write line ends
        pts[x0, y0] = 2
        pts[x1, y1] = 2
        return pts if not transpose else pts.T

    def setup_g_neighbors(self, room_classes, rooms_layout):

        layout_classes = rooms_layout
        for row in range(len(rooms_layout)):
            for col in range(len(rooms_layout[row])):
                if rooms_layout[row][col] != None: layout_classes[row][col] = (rooms_layout[row][col])

        self.setup_neighbors(room_classes, rooms_layout)

    def finish_map(self):
        # remove the classes not in the map
        rooms_in_map = []
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                if not self.map[row][col] == None:
                    rooms_in_map.append(self.map[row][col])
        for room in self.rooms:
            if not room in rooms_in_map:
                self.room_classes.remove(room)

        # Add Nones around the map so that we don't get an index error
        final_map = [[None for i in range(self.width + 2)] for j in range(self.height + 2)]
        for i in range(self.height):
            final_map[i + 1] = [None] + self.map[i] + [None]

        row_pop_offset = 0
        # squishes map to remove horizontal blank space
        for i in range(self.height):
            if final_map[i + 1 + row_pop_offset] == [None for j in range(self.width + 2)]:
                final_map.pop(i + 1 + row_pop_offset)
                row_pop_offset -= 1

        # squishes map to remove vertical blank space
        # get columns
        column_index = []
        column_pop_offset = 0
        for col in range(self.width):
            column = []
            for row in range(len(final_map) - 2):
                column.append(final_map[row + 1][col + 1])
            if column == [None for item in range(len(final_map) - 2)]:
                column_index.append(col + 1)
        # remove columns
        for i in column_index:
            for row in final_map:
                row.pop(i + column_pop_offset)
            column_pop_offset -= 1

        self.map = final_map

        self.setup_g_neighbors(self.room_classes, self.map)

        # sets the starting room
        self.current_room = self.spn
        self.visited_rooms.append(self.current_room)

    def __init__(self, runner, width, height):
        world.World.__init__(self, runner)
        self.width = width
        self.height = height

class Simple(RandomWorld):
    def __init__(self, runner, width, height):
        RandomWorld.__init__(self, runner, width, height)

        self.map = [[None for i in range(self.width)] for j in range(self.height)]

        self.rooms = []
        self.spn = None
        self.pwp = []
        self.win = None
        self.bsc = []

        def make_rooms():
            # make level shorthand
            def ml(filename, tag=None):
                return self.make_level(filename, tag)

            # spawn
            r = ml('levelspawn', 'spawn')
            self.spn = r

            # weapon rooms
            for i in range(3):
                r = ml(f'levelweapon{i + 1}', 'weapon')
                self.pwp.append(r)

            # basic rooms
            for i in range (19):
                r = ml(f'level{i + 1}')
                self.bsc.append(r)

            # win room
            r = ml('level20', 'win')
            self.win = r

            # spwn and win in [] so it doesn't break
            room_lists = [[self.spn], self.bsc, self.pwp, [self.win]]

            for lst in room_lists:
                for item in lst:
                    self.rooms.append(item)

        make_rooms()

        # spread is added and stops things from being too close to the center (doesn't limit distance to the edge for obvious reasons)
        spread = 1

        # a function so I can rerun it as needed
        def create_random_map():
            # random positions in corresponding quadrants 1, 2, 3, and 4
            q1 = [random.randrange((self.width / 2) + spread, self.width), random.randrange(0, (self.height / 2) - spread)]
            q2 = [random.randrange(0, (self.width / 2) - spread), random.randrange(0, (self.height / 2) - spread)]
            q3 = [random.randrange(0, (self.width / 2) - spread), random.randrange((self.height / 2) + spread, self.height)]
            q4 = [random.randrange((self.width / 2) + spread, self.width), random.randrange((self.height / 2) + spread, self.height)]
            positions = [q1, q2, q3, q4]

            # grabs a random quadrant
            spawn_index = random.randrange(0, len(positions))
            # spawn_index = 0

            # layout = [win, pwp room options]
            layout_preset = random.choice(['diagonal', 'square'])

            if layout_preset == 'diagonal':
                layout = [2, 1, 3]
                if random.getrandbits(1): layout = [layout[0], layout[2], layout[1]]  # allow for random variation bewteen positions as it won't make the generation drastically different

            if layout_preset == 'square':
                layout = [1, 3, 2]

            # puts positions in the right quadrants
            spawn_pos = positions[spawn_index]
            win_pos = positions[spawn_index - layout[0]]
            powerup_1 = positions[spawn_index - layout[1]]
            powerup_2 = positions[spawn_index - layout[2]]

            # make 'lines' between rooms of interest
            s1 = self.make_line_between(self.map, spawn_pos, powerup_1)
            w1 = self.make_line_between(self.map, powerup_1, powerup_2)
            w2 = self.make_line_between(self.map, powerup_2, win_pos)

            # so it doesn't break on rerun
            pwp_rooms = self.pwp.copy()

            # setup important
            self.map[spawn_pos[0]][spawn_pos[1]] = self.spn
            self.map[win_pos[0]][win_pos[1]] = self.win
            self.map[powerup_1[0]][powerup_1[1]] = pwp_rooms.pop(random_range(0, len(pwp_rooms)))
            self.map[powerup_2[0]][powerup_2[1]] = pwp_rooms.pop(random_range(0, len(pwp_rooms)))

            points_of_interest = [s1, w1, w2]

            bsc_rooms = self.bsc.copy()

            # fill lines between rooms of interest with rooms
            for y in range(len(s1)):
                for x in range(len(s1[y])):
                    for poi in points_of_interest:
                        if poi[y][x] == 1:
                            # check if map is too large
                            if len(bsc_rooms) == 0:
                                prRed('map too large for how many rooms implemented')
                                self.map = [[None for i in range(self.width)] for j in range(self.height)]
                                create_random_map()
                                return
                            # create a room
                            self.map[y][x] = (bsc_rooms.pop(random_range(0, len(bsc_rooms))))

            self.finish_map()
            print(f'layout: {layout_preset}')

        create_random_map()


# custom function with a crash handler in case min and max are 0
def random_range(minimum, maximum):
    if minimum == maximum or maximum == 0:
        return minimum
    else:
        return random.randrange(minimum, maximum)

def prRed(skk):
    print("\033[91m {}\033[00m" .format(skk))
