from abc import ABC, abstractmethod

# for DebugIO
import curses
import opc
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

xLEDs = 34
yLEDs = 32


class SnakeIO(ABC):
    @abstractmethod
    def get_keypress(self):
        """Get a keypress"""

    @abstractmethod
    def display_leader_board(self, leaders):
        """Display the leader board from a dictionary passed in (5 entries only)"""

    @abstractmethod
    def output(self, snake, trail, food):
        """Update the display"""

    @abstractmethod
    def cleanup(self):
        """Cleanup the input"""


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
        # need to include for 1px border on each side
        self.win = curses.newwin(yLEDs + 2, xLEDs + 2, 0, 0)
        self.win.keypad(1)
        curses.noecho()
        curses.curs_set(0)
        self.win.border(0)
        self.win.nodelay(1)

    def start_screen_on(self):
        self.win.addstr(14, 10, "PRESS ENTER")
        self.win.addstr(15, 11, "TO START")

    def display_menu(self):
        self.win.addstr(10, 8, '> 1. Play')
        self.win.addstr(12, 10, '2. Leaderboard')
        self.win.addstr(14, 10, '3. Settings')
        self.win.addstr(16, 10, '4. Exit')

    def menu_action(self, menu_pos, key):
        if key == 121:  # 'y'
            return -menu_pos

        if key == KEY_UP:
            if menu_pos == 1:
                return menu_pos
            self.win.addstr(10 + 2 * (menu_pos - 1), 8, ' ')
            self.win.addstr(10 + 2 * (menu_pos - 2), 8, '>')
            return menu_pos - 1

        elif key == KEY_DOWN:
            if menu_pos == 4:
                return menu_pos
            self.win.addstr(10 + 2 * (menu_pos - 1), 8, ' ')
            self.win.addstr(10 + 2 * menu_pos, 8, '>')
            return menu_pos + 1

        return menu_pos

    def get_start_dir(self):
        return self.keys_to_dirs.get(KEY_RIGHT)

    def wait_for_input(self, milli):
        self.win.timeout(milli)

    def get_keypress(self):
        return self.win.getch()

    # TODO: protect from names/scores that are too long
    def display_leader_board(self, leaders):
        self.clear()
        self.win.addstr(2, 12, "Leaderboard")
        rank = 1
        for leader in sorted(leaders.items(), key=lambda kv: kv[1], reverse=True):
            self.win.addstr(2 + rank * 2, 4, str(rank))
            self.win.addstr(2 + rank * 2, 5, ". ")
            self.win.addstr(2 + rank * 2, 7, leader[0])
            self.win.addstr(2 + rank * 2, 30, str(leader[1]))

    # Write the head of the snake
    # Erase the snake's trail, if there is one
    # Write the food
    def output(self, snake, trail, food):
        # need to include for 1px border on each side of sim
        self.win.addch(food[0] + 1, food[1] + 1, self.FOOD_CHAR)
        self.win.addch(snake[0][0] + 1, snake[0][1] + 1, self.SNAKE_CHAR)
        if trail: self.win.addch(trail[0] + 1, trail[1] + 1, self.TRAIL_CHAR)

    def clear(self):
        self.win.clear()
        self.win.border(0)

    # TODO make this more general, add more decoration etc
    def debug_score(self, score):
        self.win.addstr(33, 2, "Score: " + str(score))

    def debug(self, string):
        self.win.addstr(33, 2, string)

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
        self.pixels = [(0, 0, 0)] * self.NUM_LEDS

    def get_keypress(self):
        pass

    def calc_pixel_array_pos(self, x, y):
        return 55 + (x * self.LEDS_PER_STRIP) + ((x % 2) * self.LEDS_PER_STRIP) + (((x + 1) % 2) * y) + (
                (x % 2) * -y) + ((x % 2) * -1)

    def display_leader_board(self, leaders):
        pass

    # Not currently needed as we do not store state of the whole grid
    # def matrixToArray(matrix):
    #	for x in range(xLEDs):
    #		for y in range(yLEDs):
    #			pixels[calc_pixel_array_pos(x,y)] = matrix[x][y]

    # Build a pixel list by:
    # Writing the head of the snake
    # Erasing the snake's trail, if there is one
    # Writing the food
    # NOTE: x, y coordinates are given as (y, x) so must reverse
    def output(self, snake, trail, food):
        self.pixels[self.calc_pixel_array_pos(snake[0][1], snake[0][0])] = self.SNAKE_PIXEL
        self.pixels[self.calc_pixel_array_pos(trail[1], trail[0])] = self.TRAIL_PIXEL
        self.pixels[self.calc_pixel_array_pos(food[1], food[0])] = self.FOOD_PIXEL
        self.client.put_pixels(self.pixels)

    def cleanup(self):
        pass


if __name__ == '__main__':
    print('Instance:', isinstance(LEDIO(), SnakeIO))
