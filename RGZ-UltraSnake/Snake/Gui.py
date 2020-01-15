import tkinter
from Snake.Map import PointType, Pos


class Gui(tkinter.Tk):
    def __init__(self, title, game=None):
        super().__init__()
        super().title(title)
        super().resizable(width=False, height=False)
        super().configure(background=game.conf.color_bg)

        if game is not None:
            self.game = game
            self.snake = game.snake

        self.canvas = tkinter.Canvas(
            self,
            bg=self.game.conf.color_bg,
            width=self.game.conf.map_width,
            height=self.game.conf.map_height,
            highlightthickness=0
        )

        self.init_widgets()
        self.init_keybindings(self.game.keybind())

    @staticmethod
    def start(game):
        window = Gui(game.conf.name, game)
        window.show(game.main)

    def show(self, game_loop=None):
        def loop():
            if callable(game_loop):
                game_loop()
            if self.game.nonpause:
                if not self.snake.dead:
                    self.update_contents()
                    self.after(self.game.conf.curr_snake_speed, loop)
                else:
                    self.canvas.create_text(300, 300, text="You lost", fill="green", font="Arial 40")
                    self.after(self.game.conf.curr_snake_speed, loop)
            else:
                self.after(self.game.conf.curr_snake_speed, loop)

        self.after(100, loop)
        self.mainloop()

    def init_keybindings(self, keybindings):
        if keybindings:
            for kb in keybindings:
                self.bind(kb[0], kb[1])

    def init_widgets(self):
        self.canvas.pack(side=tkinter.LEFT)
        button_save = tkinter.Button(self.canvas, width=12, text="Save", command=self.game.save)
        button_save.pack()
        button_load = tkinter.Button(self.canvas, width=12, text="Load", command=self.game.load)
        button_load.pack()
        self.canvas.create_window((700, 300), window=button_save)
        self.canvas.create_window((700, 330), window=button_load)

    def update_contents(self):
        self.canvas.delete("deleted")
        self.draw_bg()
        self.draw_map_contents()
        self.draw_score()

    def draw_bg(self):
        self.canvas.create_rectangle(0, 0, self.game.conf.map_width, self.game.conf.map_height, fill=self.game.conf.color_bg,
                                     outline='', tag="deleted")

    def draw_map_contents(self):
        for i in range(self.game.map.num_rows - 1):
            for j in range(self.game.map.num_cols - 1):
                self.draw_grid(j * self.game.conf.snake_size, i * self.game.conf.snake_size,
                               self.game.map.point(Pos(i + 1, j + 1)).type)

    def draw_grid(self, x, y, t):
        color = 0
        if t == PointType.HEAD:
            color = self.game.conf.color_snake
        if t == PointType.BODY:
            color = self.game.conf.color_snake
        if t == PointType.FOOD:
            color = self.game.conf.color_food
        if t == PointType.WALL:
            color = self.game.conf.color_wall
        if color == self.game.conf.color_food:
            self.canvas.create_oval(x, y, x + self.game.conf.snake_size, y + self.game.conf.snake_size, fill=color,\
                                    tag="deleted")
        elif color != 0:
            self.canvas.create_rectangle(x, y, x + self.game.conf.snake_size, y + self.game.conf.snake_size,\
                                         fill=color, tag="deleted")

    def draw_score(self):
        self.canvas.create_text(700, 50, text="Your score:" + str(self.game.score), fill="#104E8B", font="Arial 17")
        if not self.game.new_record or self.game.conf.curr_snake_speed == self.game.conf.snake_speed-25:
            self.canvas.create_text(700, 100, text="Your best score:" + str(self.game.read_best_score()),
                                    fill="#104E8B", font="Arial 17", tag="deleted")
        else:
            self.canvas.create_text(700, 100, text="New best score!",
                                    fill="#104E8B", font="Arial 17", tag="deleted")
