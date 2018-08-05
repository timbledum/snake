from collections import namedtuple, deque
import pyxel

Point = namedtuple('Point', ['x', 'y'])

COL_BACKGROUND = 3
COL_BODY = 11
COL_HEAD = 7

UP = Point(0, -1)
DOWN = Point(0, 1)
RIGHT = Point(1, 0)
LEFT = Point(-1, 0)

START = Point(5, 5)

class App:
    
    def __init__(self):
        pyxel.init(40, 80)
        
        self.direction = RIGHT
        self.snake = deque()
        self.snake.append(START)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.update_direction()
        self.update_snake()

        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

    def update_direction(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.direction = UP
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.direction = DOWN
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.direction = LEFT
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.direction = RIGHT

    def update_snake(self):
        old_head = self.snake[0]
        new_head = Point(old_head.x + self.direction.x, old_head.y + self.direction.y)
        self.snake.appendleft(new_head)
        self.snake.pop()

    def draw(self):
        pyxel.cls(col=COL_BACKGROUND)
        for i, point in enumerate(self.snake):
            if i == 0:
                colour = COL_HEAD
            else:
                colour = COL_BODY

            pyxel.pix(point.x, point.y, col=colour)

App()