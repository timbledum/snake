from collections import namedtuple, deque
from random import randint
import pyxel

Point = namedtuple("Point", ["x", "y"])

COL_BACKGROUND = 3
COL_BODY = 11
COL_HEAD = 7
COL_DEATH = 8
COL_APPLE = 8

TEXT_DEATH = ["GAME OVER", "(Q)UIT", "(R)ESTART"]
COL_TEXT_DEATH = 0
HEIGHT_DEATH = 20

WIDTH = 60
HEIGHT = 80

HEIGHT_SCORE = FONT_HEIGHT = pyxel.constants.FONT_HEIGHT
COL_SCORE = 6
COL_SCORE_BACKGROUND = 5

UP = Point(0, -1)
DOWN = Point(0, 1)
RIGHT = Point(1, 0)
LEFT = Point(-1, 0)

START = Point(5, 5 + HEIGHT_SCORE)

class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT)
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.direction = RIGHT
        self.snake = deque()
        self.snake.append(START)
        self.death = False
        self.score = 0
        self.generate_apple()

    def update(self):
        if not self.death:
            self.update_direction()
            self.update_snake()
            self.check_death()
            self.check_apple()

        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_R, 0, 0):
            self.reset()

    def update_direction(self):
        if pyxel.btn(pyxel.KEY_UP):
            if self.direction is not DOWN:
                self.direction = UP
        elif pyxel.btn(pyxel.KEY_DOWN):
            if self.direction is not UP:
                self.direction = DOWN
        elif pyxel.btn(pyxel.KEY_LEFT):
            if self.direction is not RIGHT:
                self.direction = LEFT
        elif pyxel.btn(pyxel.KEY_RIGHT):
            if self.direction is not LEFT:
                self.direction = RIGHT

    def update_snake(self):
        old_head = self.snake[0]
        new_head = Point(old_head.x + self.direction.x, old_head.y + self.direction.y)
        self.snake.appendleft(new_head)
        self.popped_point = self.snake.pop()

    def check_apple(self):
        if self.snake[0] == self.apple:
            self.score += 1
            self.snake.append(self.popped_point)
            self.generate_apple()

    def generate_apple(self):
        x = randint(0, WIDTH - 1)
        y = randint(HEIGHT_SCORE + 1, HEIGHT - 1)
        self.apple = Point(x, y)

    def check_death(self):
        head = self.snake[0]
        if (
            head.x < 0
            or head.y <= HEIGHT_SCORE
            or head.x >= WIDTH
            or head.y >= HEIGHT
        ):
            self.death = True # Check out of bounds
        elif len(self.snake) != len(set(self.snake)):
            self.death = True # Check having run into self

    def draw(self):
        if not self.death:
            pyxel.cls(col=COL_BACKGROUND)
            self.draw_snake()
            self.draw_score()
            pyxel.pix(self.apple.x, self.apple.y, col=COL_APPLE)

        else:
            self.draw_death()

    def draw_snake(self):
        for i, point in enumerate(self.snake):
            if i == 0:
                colour = COL_HEAD
            else:
                colour = COL_BODY
            pyxel.pix(point.x, point.y, col=colour)

    def draw_score(self):
            score = "{:04}".format(self.score)
            pyxel.rect(0, 0, WIDTH, HEIGHT_SCORE, COL_SCORE_BACKGROUND)
            pyxel.text(1, 1, score, COL_SCORE)

    def draw_death(self):
        pyxel.cls(col=COL_DEATH)
        for i, text in enumerate(TEXT_DEATH):
            y_offset = (FONT_HEIGHT + 2) * i
            text_x = center_text(text, WIDTH)
            pyxel.text(text_x, HEIGHT_DEATH + y_offset, text, COL_TEXT_DEATH)


def center_text(text, page_width, char_width=pyxel.constants.FONT_WIDTH):
    text_width = len(text) * char_width
    return (page_width - text_width) // 2


App()
