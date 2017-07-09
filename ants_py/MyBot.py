#!/usr/bin/env python
from ants import *
from time import time
import sys


def dist(a, b): return a * a + b * b


def dist_p(a): return a[0] * a[0] + a[1] * a[1]


def dist2(a, b): return dist_p(sub2(a, b))


def add2(a, b): return a[0] + b[0], a[1] + b[1]


def sub2(a, b):
    if type(a[0]) == str and type(b[0]) == int or type(a[1]) == str and type(b[1]) == int:
        print()
    return a[0] - b[0], a[1] - b[1]


def div_by_num(a, b): return a[0] / b, a[1] / b


def mul_by_num(a, b): return a[0] * b, a[1] * b


def mod_by_num(a, b): return a[0] % b, a[1] % b


def div_by_num2_0(a, b, c): return a[0] / b, a[1] / c


def mod_by_num2_0(a, b, c): return a[0] % b, a[1] % c


def debug(*args):
    return
    with open('../fuck.u', 'a+') as f:
        print(*args, file=f)


_neighbours_cache = {}


def get_neighbours(loc):
    return _neighbours_cache[loc]


def bfs_find_path(ants, ant_loc, target, target_set):
    """ 
    :type ants: Ants
    :rtype: List
    """
    black = set()
    grey = {ant_loc}
    new_grey = set()
    p2p = {}

    while len(grey) > 0:
        for loc in grey:
            for neighbour in get_neighbours(loc):
                a = ants.map[neighbour[0]][neighbour[1]] == WATER
                b = neighbour in black
                c = neighbour in grey
                d = neighbour in new_grey
                e = neighbour in p2p
                if a or b or c or d or e:
                    continue
                new_grey.add(neighbour)
                p2p[neighbour] = loc
                if neighbour in target_set:
                    if neighbour in target:
                        continue
                    last = neighbour
                    target[neighbour] = last
                    res = [neighbour]
                    while last in p2p and last != ant_loc:
                        res.insert(0, p2p[last])
                        last = p2p[last]
                    debug('PRIIIINT')
                    debug(last)
                    return res[1]
        black.update(grey)
        grey = new_grey
        new_grey = set()
    return tuple()


def alternative_path(ant_loc, ants):
    for direction in ['w', 'n', 'e', 's']:
        destination = ants.destination(ant_loc, direction)
        if ants.passable(destination):
            return destination


class MyBot:
    def __init__(self):
        self.ant2path = {}
        pass

    def do_setup(self, ants):
        deltas = [
            (-1, 0),
            (0, 1),
            (1, 0),
            (0, -1)]
        for y in range(len(ants.map)):
            for x in range(len(ants.map[y])):
                loc = (y, x)
                if loc not in _neighbours_cache:
                    _neighbours_cache[loc] = tuple(
                        mod_by_num2_0(add2(loc, delta_rot), ants.rows, ants.cols) for delta_rot in deltas)

    def path2directions(self, param, ant_loc, ants):
        deltas = {
            (ants.rows - 1, 0): 'n',
            (0, 1): 'e',
            (1, 0): 's',
            (0, ants.cols - 1): 'w',
        }
        num___ = mod_by_num2_0(sub2(param, ant_loc), ants.rows, ants.cols)
        if num___ not in deltas:
            self.ant2path[ant_loc] = 'n'
        else:
            self.ant2path[ant_loc] = deltas[num___]

    def do_turn(self, ants):
        difficult = False
        target = {}
        my_ants = ants.my_ants()
        enemy_hills = ants.enemy_hills()
        enemy_ants = ants.enemy_ants()
        orders = {ant: ant for ant in my_ants}
        for i, ant_loc in enumerate(my_ants):
            if ant_loc not in self.ant2path:
                self.ant2path[ant_loc] = []
            start = time()
            debug(len(my_ants))
            new_loc = ()
            if not difficult:
                if enemy_hills and all(dist2(ant_loc, enemy) < 90 for enemy in enemy_hills):
                    new_loc = bfs_find_path(ants, ant_loc, target, set(enemy_hills))
                elif enemy_ants and all(dist2(ant_loc, enemy) < 90 for enemy in enemy_ants):
                    new_loc = bfs_find_path(ants, ant_loc, target, set(enemy_ants))
                elif any(dist2(food, ant_loc) < 150 for food in ants.food_list):
                    new_loc = bfs_find_path(ants, ant_loc, target, set(ants.food_list))
            if not new_loc:
                new_loc = alternative_path(ant_loc, ants)
            time_start = time() - start
            debug('bfs->')
            debug(time_start)
            if new_loc not in orders:
                orders[new_loc] = ant_loc
                self.path2directions(new_loc, ant_loc, ants)
                if not self.ant2path[ant_loc]:
                    continue
                ants.issue_order((ant_loc, self.ant2path[ant_loc][0]))
            if ants.time_remaining() < 200:
                difficult = True


if __name__ == '__main__':
    # ants = Ants()
    # ants.map = {
    #     0: {0: LAND, 1: LAND, 2: LAND, 3: LAND, 4: LAND, 5: LAND},
    #     1: {0: LAND, 1: LAND, 2: LAND, 3: LAND, 4: LAND, 5: LAND},
    #     2: {0: LAND, 1: LAND, 2: LAND, 3: LAND, 4: WATER, 5: LAND},
    #     3: {0: LAND, 1: LAND, 2: LAND, 3: WATER, 4: FOOD, 5: WATER},
    #     4: {0: LAND, 1: LAND, 2: LAND, 3: WATER, 4: LAND, 5: WATER},
    #     5: {0: LAND, 1: LAND, 2: LAND, 3: LAND, 4: LAND, 5: LAND},
    # }
    # ants.food_list.append((3, 4))
    # ants.rows = 6
    # ants.cols = 6
    # MyBot().path2directions(bfs_find_path(ants, (0, 0), {}), (0, 0), ants)
    try:
        import psyco

        psyco.full()
    except ImportError:
        pass
    try:
        Ants.run(MyBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
