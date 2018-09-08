# NOTE: USE PYTHON 3!
# NOTE: all coordinates are in [y, x] form

# Debug mode: run in terminal, use arrow keys, ESC to quit
# LED mode: run with dance-mat input

from random import randint
from operator import add

from SnakeGame import SnakeGame
from SnakeIO import LEDIO, DebugIO

xLEDs = 34
yLEDs = 32


def change_dir(curr, new):
    # If given the same direction, or the opposite, don't change direction
    if new == curr or new[0] == -curr[0] or new[1] == -curr[1]:
        return curr
    return new


# TODO: streamline
# Return true iff the head of the snake is within bounds (for bounded mode)
# and does not hit itself
def legal_move(snake, s):
    if snake.get_walls_enabled():
        if s[0][0] == -1 or s[0][0] == yLEDs or s[0][1] == -1 or s[0][1] == xLEDs:
            return False
    # Teleport
    else:
        # y
        if s[0][0] == -1:
            s[0][0] = yLEDs - 1
        elif s[0][0] == yLEDs:
            s[0][0] = 0

        # x
        if s[0][1] == -1:
            s[0][1] = xLEDs - 1
        elif s[0][1] == xLEDs:
            s[0][1] = 0

    if s[0] in s[1:]:
        return False
    return True


def beast(snake):
    pass


def leader_board(snake):
    snake.display_leader_board()
    key = -1
    while key < 0:
        snake.sim_io.wait_for_input(200)
        key = snake.sim_io.get_keypress()
    snake.sim_io.clear()


def settings(snake):
    pass


# Entry point
# Navigate with arrow keys
# press 'y' to enter menu option
def menu(snake):
    while True:
        menu_option = 1
        snake.sim_io.display_menu()

        # While enter not pressed
        while menu_option > 0:
            # Wait for input
            key = -1
            while key < 0:
                snake.sim_io.wait_for_input(200)
                key = snake.sim_io.get_keypress()

            # return -1 for select current option, update display inside this
            menu_option = snake.sim_io.menu_action(menu_option, key)

        snake.sim_io.clear()

        # Play
        if menu_option == -1:
            run(snake)

        # Leaderboard
        elif menu_option == -2:
            leader_board(snake)

        # Settings
        elif menu_option == -3:
            settings(snake)

        # BEAST MODE (TODO)
        elif menu_option == -4:
            # beast(snake)
            break


def run(snake):
    score = 0
    snake_pixels = [[4, 10], [4, 9], [4, 8]]
    food = [10, 20]
    trail = []

    KEY_ESC = 27
    key = -1
    direction = snake.sim_io.get_start_dir()

    # Display start screen, wait for a keypress
    snake.sim_io.start_screen_on()
    while key < 0:
        snake.sim_io.wait_for_input(200)
        key = snake.sim_io.get_keypress()
    snake.sim_io.clear()

    while True:
        if snake.get_speed_increases():
            snake.sim_io.wait_for_input(int(200 - (len(snake_pixels) * 4) % 140))
        else:
            snake.sim_io.wait_for_input(160)

        # Get key
        # get_keypress returns -1 if no key is pressed
        prevKey = key
        event = snake.sim_io.get_keypress()
        key = key if event == -1 else event

        # TODO: change control flow of get key press
        # Change direction if new, valid key pressed
        if key == KEY_ESC:
            break
        if key != prevKey:
            if key in snake.sim_io.keys_to_dirs:  # TODO change to if then get, default one line
                direction = change_dir(direction, snake.sim_io.keys_to_dirs.get(key))

        # Add on the new head to the snake, check if legal
        snake_pixels.insert(0, list(map(add, snake_pixels[0], direction)))
        if not legal_move(snake, snake_pixels):
            break

        # If food is eaten, generate new, otherwise remove tail
        if snake_pixels[0] == food:
            score += 1
            last = []
            food = [randint(1, yLEDs - 2), randint(1, xLEDs - 2)]
            while food in snake_pixels:
                food = [randint(1, yLEDs - 2), randint(1, xLEDs - 2)]
        else:
            trail = snake_pixels.pop()

        # Output new frame and score, respective IO class will update display as necessary
        snake.led_io.output(snake_pixels, trail, food)
        snake.sim_io.output(snake_pixels, trail, food)
        snake.sim_io.debug_score(score)

    # Add to high scores if in competition mode - set name first
    # snake.add_score(score, name)

    # TODO: Display game over screen

    snake.sim_io.clear()


# TODO: add modes 3 and 4
if __name__ == '__main__':
    # Set mode based on command line args
    # 0 = game mode
    # 1 = dev mode - terminal simulation, with output to open_gl also
    # 2 = dev mode - as above but send output to LEDs not open_gl
    # assert (len(sys.argv) == 2), 'Incorrect number of arguments supplied'

    snake_game = SnakeGame(DebugIO(), LEDIO(), "hard")
    menu(snake_game)
    snake_game.cleanup()
