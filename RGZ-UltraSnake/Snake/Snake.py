from collections import deque
from Snake.Map import PointType


class Snake:
    def __init__(self, map, init_direc, init_bodies, init_types):
        self.map = map
        self.init_direc = init_direc
        self.init_bodies = init_bodies
        self.init_types = init_types
        self.reset(False)
        self.dead = False

    def reset(self, reset_map=True):
        self.dead = False
        self.direc = self.init_direc
        self.direc_next = self.direc
        self.bodies = deque(self.init_bodies)

        if reset_map:
            self.map.reset()

        for i, pos in enumerate(self.bodies):
            self.map.point(pos).type = self.init_types[i]
        return 0

    def load(self, load_bodies, load_types, load_direc):
        self.bodies = deque(load_bodies)
        self.direc_next = load_direc
        self.map.reset(True)
        for i, pos in enumerate(self.bodies):
            self.map.point(pos).type = load_types[i-1]

    def bodies(self):
        return self.bodies

    def len(self):
        return len(self.bodies)

    def head(self):
        if not self.bodies:
            return None
        return self.bodies[0]

    def tail(self):
        if not self.bodies:
            return None
        return self.bodies[-1]

    def move(self, new_direc=None):
        if new_direc is not None:
            self.direc_next = new_direc
        new_head = self.head().adj(self.direc_next)
        if self.map.is_empty(new_head):
            self.map.point(self.head()).type = PointType.BODY
            self.bodies.appendleft(new_head)
            self.map.point(new_head).type = PointType.HEAD
            self._rm_tail()
        else:
            self.dead = True

    def _rm_tail(self):
        self.map.point(self.tail()).type = PointType.EMPTY
        self.bodies.pop()

    def add_body(self):
        new_body = self.tail()
        self.bodies.append(new_body)
        self.map.point(new_body).type = PointType.BODY

