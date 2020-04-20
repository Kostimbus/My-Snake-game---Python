from Snake.Snake import Snake
from Snake.Map import Map, PointType, Direc, Pos
import sys
import os.path


class Conf:
    def __init__(self):
        self.name = 'Ultimate Snake'

        self.snake_speed = 250
        self.curr_snake_speed = self.snake_speed
        self.snake_size = 20

        self.map_width = 800
        self.map_height = 600
        self.map_cols = 31
        self.map_rows = 31

        self.color_bg = '#252624'
        self.color_snake = '#104E8B'
        self.color_food = '#EE0000'
        self.color_wall = '#754600'

        self.init_direc = Direc.RIGHT
        self.init_bodies = [Pos(3, 6), Pos(3, 5), Pos(3, 4)]
        self.init_types = [PointType.HEAD] + [PointType.BODY] * 2


class Game:
    def __init__(self, conf):
        self.conf = conf
        self.map = Map(conf.map_rows, conf.map_cols)
        self.snake = Snake(self.map, conf.init_direc, conf.init_bodies, conf.init_types)
        self.nonpause = True
        self.score = -1
        self.new_record = False

    def main(self):
        if self.nonpause:
            self.snake.move()
        if self.map.create_apple():
            self.snake.add_body()
            self.score += 1
            self.conf.curr_snake_speed -= self.change_speed()

    def keybind(self):
        bind_list = (
                ('<w>', lambda e: self.update_direc(Direc.UP)),
                ('<a>', lambda e: self.update_direc(Direc.LEFT)),
                ('<s>', lambda e: self.update_direc(Direc.DOWN)),
                ('<d>', lambda e: self.update_direc(Direc.RIGHT)),
                ('<space>', lambda e: self._toggle_pause()),
                ('<Escape>', lambda e: self.__exit__()),
                ('<r>', lambda e: self.game_reset())
            )
        return bind_list

    def update_direc(self, new_direc):
        if (self.snake.direc_next.value - new_direc.value != 2) and (self.snake.direc_next.value - new_direc.value != -2):
            self.snake.direc_next = new_direc

    def game_reset(self):
        if self.new_record:
            with open(os.path.dirname(__file__) + "/../record.txt", "w") as f:                                  # path in CONST and WRITE and READ in FUNCTION !!!!!!!!!!   Remove debug in cmd for DIRECTION !!!! Better serialize !!!!
                f.write(str(self.score))
            self.new_record = False
        self.score = -1
        self.conf.curr_snake_speed = self.conf.snake_speed
        self.snake.reset()

    def _toggle_pause(self):
        if self.nonpause:
            self.nonpause = False
        else:
            self.nonpause = True

    def read_best_score(self):
        with open(os.path.dirname(__file__) + "/../record.txt", "r") as f:
            curr_best_score = int(f.read())
            print(curr_best_score)
            if self.score > curr_best_score:
                self.new_record = True
            return curr_best_score

    def change_speed(self):
        if self.score % 2 == 0 and self.conf.curr_snake_speed > 25:
            return 25
        else:
            return 0

    def __exit__(self):
        if self.new_record:
            with open(os.path.dirname(__file__) + "/../record.txt", "w") as f:
                f.write(str(self.score))
        sys.exit()

    def save(self):
        change = 0
        if self.nonpause:
            self.nonpause = False
            change = 1
        with open("D:\RGZ-UltraSnake_final\RGZ-UltraSnake\save.txt", "w") as f:
            f.write(str(self.map.apple.x))
            f.write(" ")
            f.write(str(self.map.apple.y))
            f.write("\n")
            f.write(str(self.snake.direc_next.value))
            f.write("\n")
            f.write(str(self.score))
            f.write("\n")
            f.write(str(self.conf.curr_snake_speed))
            f.write("\n")
            for i in range(self.snake.len()):
                f.write(str(self.snake.bodies[i].x))
                f.write(" ")
                f.write(str(self.snake.bodies[i].y))
                f.write("\n")
        if change:
            self.nonpause = True
            
    def load(self):
        change = 0
        if self.nonpause:
            self.nonpause = False
            change = 1
        with open("D:\RGZ-UltraSnake_final\RGZ-UltraSnake\save.txt", "r") as f:
            apple_pos = f.readline().split("\n")[0].split()
            self.map.apple = Pos(int(apple_pos[0]), int(apple_pos[1]))
            temp = int(f.readline().split("\n")[0])
            if temp == 1:
                load_direc = Direc.LEFT
            elif temp == 2:
                load_direc = Direc.UP
            elif temp == 3:
                load_direc = Direc.RIGHT
            else:
                load_direc = Direc.DOWN
            self.score = int(f.readline().split("\n")[0])
            self.conf.curr_snake_speed = int(f.readline().split("\n")[0])
            data = f.read().splitlines()
            load_bodies = []
            for i in range(len(data)):
                temp = data[i].split()
                load_bodies.append(Pos(int(temp[0]), int(temp[1])))
            load_types = [PointType.HEAD] + [PointType.BODY] * (len(data)-1)
            self.snake.load(load_bodies, load_types, load_direc)
        if change:
            self.nonpause = True
