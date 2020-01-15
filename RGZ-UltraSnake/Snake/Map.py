from enum import Enum
import random


class Map:
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.content = [[Point() for _ in range(num_cols)] for _ in range(num_rows)]
        self.reset()

    def reset(self, load=False):

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self.content[i][j].type = PointType.EMPTY
        if load:
            self.point(self.apple).type = PointType.FOOD
        for j in range(self.num_cols):
            self.content[0][j].type = PointType.WALL
            self.content[int(self.num_rows)-2][j].type = PointType.WALL
        for i in range(self.num_rows):
            self.content[i][0].type = PointType.WALL
            self.content[i][int(self.num_cols)-2].type = PointType.WALL

    def num_rows(self):
        return self.num_rows

    def num_cols(self):
        return self.num_cols

    def point(self, pos):
        return self.content[pos.x-1][pos.y-1]

    def create_apple(self):
        for i in range(self.num_rows - 2):
            for j in range(self.num_cols - 2):
                if self.point(Pos(i + 1, j + 1)).type == PointType.FOOD:
                    self.apple = Pos(i+1, j+1)
                    return False
        flag = True
        while flag:
            a = random.randint(2, self.num_cols - 2)
            b = random.randint(2, self.num_rows - 2)
            if self.point(Pos(a, b)).type != PointType.EMPTY:
                continue
            else:
                self.point(Pos(a, b)).type = PointType.FOOD
                self.apple = Pos(a, b)
                flag = False
        return True

    def is_empty(self, pos):
        return (self.point(pos).type == PointType.EMPTY or \
                                        self.point(pos).type == PointType.FOOD)


class PointType(Enum):
    EMPTY = 0
    FOOD = 2
    HEAD = 100
    BODY = 200
    WALL = 666


class Point:
    def __init__(self):
        self._type = PointType.EMPTY

    def type(self):
        return self._type

    def type(self, val):
        self._type = val


class Direc(Enum):
    NONE = 0
    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4


class Pos:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def adj(self, direc):
        if direc == Direc.LEFT:
            return Pos(self.x, self.y - 1)
        elif direc == Direc.RIGHT:
            return Pos(self.x, self.y + 1)
        elif direc == Direc.UP:
            return Pos(self.x - 1, self.y)
        elif direc == Direc.DOWN:
            return Pos(self.x + 1, self.y)
        else:
            return None
