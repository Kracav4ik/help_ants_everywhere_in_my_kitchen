#!/usr/bin/env python
from ants import *
from time import time
import sys


def add2(a, b): return a[0] + b[0], a[1] + b[1]


def sub2(a, b): return a[0] - b[0], a[1] - b[1]


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


def get_neighbours(loc, rows, cols):
    deltas = [
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1)]
    if loc not in _neighbours_cache:
        _neighbours_cache[loc] = tuple(mod_by_num2_0(add2(loc, delta_rot), rows, cols) for delta_rot in deltas)
    return _neighbours_cache[loc]


def bfs_find_path(ants, ant_loc, target):
    """ 
    :type ants: Ants
    :rtype: List
    """
    black = set()
    grey = {ant_loc}
    new_grey = set()
    p2p = {}

    food_set = set(ants.food_list)
    my_ants = set(ants.my_ants())
    while len(grey) > 0:
        for loc in grey:
            for neighbour in get_neighbours(loc, ants.rows, ants.cols):
                a = ants.map[neighbour[0]][neighbour[1]] == WATER
                b = neighbour in black
                c = neighbour in grey
                d = neighbour in new_grey
                e = neighbour in p2p
                f = neighbour in my_ants
                if a or b or c or d or e or f:
                    continue
                new_grey.add(neighbour)
                p2p[neighbour] = loc
                if neighbour in food_set:
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
    return []


class MyBot:
    def __init__(self):
        self.ant2path = {}
        pass

    def do_setup(self, ants):
        pass

    def path2directions(self, param, ant_loc, ants):
        deltas = {
            (ants.rows-1, 0): 'n',
            (0, 1): 'e',
            (1, 0): 's',
            (0, ants.cols-1): 'w',
        }
        self.ant2path[ant_loc] = deltas[mod_by_num2_0(sub2(param, ant_loc), ants.rows, ants.cols)]

    def do_turn(self, ants):
        orders = []
        target = {}
        t = 0
        for ant_loc in ants.my_ants():
            if ant_loc not in self.ant2path:
                self.ant2path[ant_loc] = []
            start = time()
            debug(len(ants.my_ants()))
            path = bfs_find_path(ants, ant_loc, target)
            time_start = time() - start
            debug('bfs->')
            debug(time_start)
            t += time_start
            if t > 2:
                break
            if not path:
                orders.append(ant_loc)
            elif path not in orders:
                start = time()
                orders.append(path)
                self.path2directions(path, ant_loc, ants)
                if not self.ant2path[ant_loc]:
                    self.ant2path[ant_loc].append('w')
                ants.issue_order((ant_loc, self.ant2path[ant_loc][0]))
                time_start = time() - start
                debug('what else?->')
                debug(time_start)
                t += time_start


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
