from abc import ABC, abstractmethod

# for DebugIO
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

xLEDs = 34
yLEDs = 32

class SnakeIO(ABC):
    @abstractmethod
    def get_keypress(self, win):
        '''Get a keypress'''

    @abstractmethod
    def output(self, win, snake, trail, food):
        '''Update the display'''

    @abstractmethod
    def cleanup(self):
        '''Cleanup the input'''

@SnakeIO.register
class DebugIO(SnakeIO):
    SNAKE_CHAR = '#'
    FOOD_CHAR = '*'
    TRAIL_CHAR = ' '

    # Define key to move vector mapping
    keys_to_dirs = {
        KEY_LEFT: [0, -1],
        KEY_RIGHT: [0, 1],
        KEY_UP: [-1, 0],
        KEY_DOWN: [1, 0]
    }

    def __init__(self):
        curses.initscr()
        self.win = curses.newwin(yLEDs, xLEDs, 0, 0)
        self.win.keypad(1)
        curses.noecho()
        curses.curs_set(0)
        self.win.border(0)
        self.win.nodelay(1)

    def get_start_dir(self):
        return self.keys_to_dirs.get(KEY_RIGHT)

    def wait_for_input(self, milli):
        self.win.timeout(milli)

    def get_keypress(self):
        return self.win.getch()

    # Write the head of the snake
    # Erase the snake's trail, if there is one
    # Write the food
    def output(self, snake, trail, food):
        self.win.addch(food[0], food[1], self.FOOD_CHAR)
        self.win.addch(snake[0][0], snake[0][1], self.SNAKE_CHAR)
        if trail: self.win.addch(trail[0], trail[1], self.TRAIL_CHAR)

    # TODO make this more general, add more decoration etc
    def debug_score(self, score):
        self.win.addstr(31, 2, "Score: " + str(score))

    def cleanup(self):
        curses.endwin()

@SnakeIO.register
class LEDIO(SnakeIO):
    LEDS_PER_STRIP = 32
    NUM_LEDS = 1088 + 55

    SNAKE_PIXEL = (255, 255, 255)
    FOOD_PIXEL = (0, 255, 0)
    TRAIL_PIXEL = (0, 0, 0)

    def __init__(self):
        self.client = opc.Client('localhost:7890')
        self.pixels = pixels = [ (0,0,0) ] * NUM_LEDS

    def get_keypress(self, win):
        pass


    def calcPixelArrayPos(x, y):
    	return 55 + (x * LEDS_PER_STRIP) + ((x % 2 ) * LEDS_PER_STRIP) + (((x + 1) % 2) * y) + ((x % 2) * -y) + ((x % 2) * -1)

    # Not currently needed as we do not store state of the whole grid
    #def matrixToArray(matrix):
    #	for x in range(xLEDs):
    #		for y in range(yLEDs):
    #			pixels[calcPixelArrayPos(x,y)] = matrix[x][y]

    # Build a pixel list by:
    # Writing the head of the snake
    # Erasing the snake's trail, if there is one
    # Writing the food
    # NOTE: x, y coordinates are given as (y, x) so must reverse
    def output(self, snake, trail, food):
        self.pixels[calcPixelArrayPos(snake[0][1], snake[0][0])] = SNAKE_PIXEL
        self.pixels[calcPixelArrayPos(trail[1], trail[0])] = TRAIL_PIXEL
        self.pixels[calcPixelArrayPos(food[1], food[0])] = FOOD_PIXEL
        self.client.put_pixels(self.pixels)

    def cleanup(self):
        pass

if __name__ == '__main__':
    print ('Instance:', isinstance(LEDIO(), SnakeIO))
