# NOTE: USE PYTHON 3!
# NOTE: all coordinates are in [y, x] form

# Debug mode: run in terminal, use arrow keys, ESC to quit
# LED mode: run with dance-mat input

from random import randint
from operator import add
from SnakeIO import LEDIO, DebugIO

def change_dir(curr, new):
    # If given the same direction, or the opposite, don't change direction
    if new == curr or new[0] == -curr[0] or new[1] == -curr[1]:
        return curr
    return new

# TODO: bounded mode
# TODO: streamline
# Return true iff the head of the snake is within bounds (for bounded mode)
# and does not hit itself
def legal_move(snake):
    if snake[0][0] == 0 or snake[0][0] == yLEDs-1 or snake[0][1] == 0 or snake[0][1] == xLEDs-1:
        return False
    if snake[0] in snake[1:]:
        return False
    return True

def run(snakeIO):
    xLEDs = 34
    yLEDs = 32

    score = 0
    snake = [[4,10], [4,9], [4,8]]
    food = [10,20]

    KEY_ESC = 27
    alive = True
    key = 0
    direction = snakeIO.get_start_dir()

    # Display start screen
    #curses.napms(1000)

    while alive:
        # Increase speed when snake is longer?
        #snakeIO.wait_for_input(150 - (len(snake)/5 + len(snake)/10)%120)
        snakeIO.wait_for_input(150)

        # Get key
        # get_keypress returns -1 if no key is pressed
        prevKey = key
        event = snakeIO.get_keypress()
        key = key if event == -1 else event

        # TODO: change control flow of get key press
        # Change direction if new, valid key pressed
        if key == KEY_ESC:
            break
        if key != prevKey:
            if key in snakeIO.keys_to_dirs: # TODO change to if then get, default one line
                direction = change_dir(direction, snakeIO.keys_to_dirs.get(key))

        # Add on the new head to the snake, check if legal
        snake.insert(0, list(map(add, snake[0], direction)))
        if not legal_move(snake):
            break

        # If food is eaten, generate new, otherwise remove tail
        if snake[0] == food:
            score += 1
            last = []
            food = [randint(1, yLEDs-2), randint(1, xLEDs-2)]
            while food in snake:
                food = [randint(1, yLEDs-2), randint(1, xLEDs-2)]
        else:
            trail = snake.pop()

        # Output new frame and score, respective IO class will update display as necessary
        snakeIO.output(snake, trail, food)
        snakeIO.debug_score(score)


    # Display game over screen


    snakeIO.cleanup()
    print("\nScore - " + str(score))

if __name__ == '__main__':
	# Set mode based on command line args
	# 0 = game mode
	# 1 = dev mode (don't use joysticks, terminal simulation)
    # 2 = dev mode as above but send output to simulation also
    # 3 = dev mode as above but send output to LEDs also
	assert (len(sys.argv) == 2), 'Incorrect number of arguments supplied'
    if sys.args[1] == 0:
        snakeIO = LEDIO()
    else:
        snakeIO = DebugIO()
    run(snakeIO)
