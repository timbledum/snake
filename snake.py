"""Snake implemented with pyxel.

This is the game of snake in pyxel version!

Try and collect the tasty apples without running
into the side or yourself.

Controls are the arrow keys ← ↑ → ↓

Q: Quit the game
R: Restart the game

Created by Marcus Croucher in 2018.
"""

from collections import namedtuple, deque
from random import randint
import pyxel

Point = namedtuple("Point", ["x", "y"])  # Convenience class for coordinates

#############
# Constants #
#############

COL_BACKGROUND = 3
COL_BODY = 11
COL_HEAD = 7
COL_DEATH = 8
COL_APPLE = 8

TEXT_DEATH = ["GAME OVER", "(Q)UIT", "(R)ESTART"]
COL_TEXT_DEATH = 0
HEIGHT_DEATH = 5

WIDTH = 40
HEIGHT = 50

HEIGHT_SCORE = FONT_HEIGHT = pyxel.constants.FONT_HEIGHT
COL_SCORE = 6
COL_SCORE_BACKGROUND = 5

UP = Point(0, -1)
DOWN = Point(0, 1)
RIGHT = Point(1, 0)
LEFT = Point(-1, 0)

START = Point(5, 5 + HEIGHT_SCORE)

###################
# The game itself #
###################


class Snake:
    """The class that sets up and runs the game."""

    def __init__(self):
        """Initiate pyxel, set up initial game variables, and run."""

        pyxel.init(WIDTH, HEIGHT, caption="Snake!", scale=8, fps=22)
        self.music = Music()
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        """Initiate key variables (direction, snake, apple, score, etc.)"""

        self.direction = RIGHT
        self.snake = deque()
        self.snake.append(START)
        self.death = False
        self.score = 0
        self.generate_apple()

    ##############
    # Game logic #
    ##############

    def update(self):
        """Update logic of game. Updates the snake and checks for scoring/win condition."""

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
        """Watch the keys and change direction."""

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
        """Move the snake based on the direction."""

        old_head = self.snake[0]
        new_head = Point(old_head.x + self.direction.x, old_head.y + self.direction.y)
        self.snake.appendleft(new_head)
        self.popped_point = self.snake.pop()

    def check_apple(self):
        """Check whether the snake is on an apple."""

        if self.snake[0] == self.apple:
            self.score += 1
            self.music.sfx_apple()
            self.snake.append(self.popped_point)
            self.generate_apple()

    def generate_apple(self):
        """Generate an apple randomly."""
        snake_pixels = set(self.snake)

        self.apple = self.snake[0]
        while self.apple in snake_pixels:
            x = randint(0, WIDTH - 1)
            y = randint(HEIGHT_SCORE + 1, HEIGHT - 1)
            self.apple = Point(x, y)

    def check_death(self):
        """Check whether the snake has died (out of bounds or doubled up.)"""

        head = self.snake[0]
        if head.x < 0 or head.y <= HEIGHT_SCORE or head.x >= WIDTH or head.y >= HEIGHT:
            self.music.sfx_death()
            self.death = True  # Check out of bounds
        elif len(self.snake) != len(set(self.snake)):
            self.music.sfx_death()
            self.death = True  # Check having run into self

    ##############
    # Draw logic #
    ##############

    def draw(self):
        """Draw the background, snake, score, and apple OR the end screen."""

        if not self.death:
            pyxel.cls(col=COL_BACKGROUND)
            self.draw_snake()
            self.draw_score()
            pyxel.pix(self.apple.x, self.apple.y, col=COL_APPLE)

        else:
            self.draw_death()

    def draw_snake(self):
        """Draw the snake with a distinct head by iterating through deque."""

        for i, point in enumerate(self.snake):
            if i == 0:
                colour = COL_HEAD
            else:
                colour = COL_BODY
            pyxel.pix(point.x, point.y, col=colour)

    def draw_score(self):
        """Draw the score at the top."""

        score = "{:04}".format(self.score)
        pyxel.rect(0, 0, WIDTH, HEIGHT_SCORE, COL_SCORE_BACKGROUND)
        pyxel.text(1, 1, score, COL_SCORE)

    def draw_death(self):
        """Draw a blank screen with some text."""

        pyxel.cls(col=COL_DEATH)
        display_text = TEXT_DEATH[:]
        display_text.insert(1, "{:04}".format(self.score))
        for i, text in enumerate(display_text):
            y_offset = (FONT_HEIGHT + 2) * i
            text_x = self.center_text(text, WIDTH)
            pyxel.text(text_x, HEIGHT_DEATH + y_offset, text, COL_TEXT_DEATH)

    @staticmethod
    def center_text(text, page_width, char_width=pyxel.constants.FONT_WIDTH):
        """Helper function for calcuating the start x value for centered text."""

        text_width = len(text) * char_width
        return (page_width - text_width) // 2


class Music:
    def __init__(self):
        pyxel.sound(0).set(
            note="c3e3g3c4c4", tone="s", volume="4", effect=("n" * 4 + "f"), speed=7
        )
        pyxel.sound(1).set(
            "f3 b2 f2 b1  f1 f1 f1 f1",
            tone="p",
            volume=("4" * 4 + "4321"),
            effect=("n" * 7 + "f"),
            speed=9,
        )

    def sfx_apple(self):
        pyxel.play(0, 0)

    def sfx_death(self):
        pyxel.play(0, 1)

if __name__ == "__main__":
    Snake()
