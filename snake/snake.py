# SNAKES GAME
# Use ARROW KEYS to play, SPACE BAR for pausing/resuming and Esc Key for exiting

# NOTE: all coordinates are in [y, x] form

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
from operator import add
from SnakeIO import LEDIO, DebugIO

xLEDs = 34
yLEDs = 32

# Define key to move vector mapping
keys_to_dirs = {
    KEY_LEFT: [0, -1],
    KEY_RIGHT: [0, 1],
    KEY_UP: [-1, 0],
    KEY_DOWN: [1, 0]
}

# Output setup
curses.initscr()
win = curses.newwin(yLEDs, xLEDs, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

# Init
key = KEY_RIGHT
score = 0
snake = [[4,10], [4,9], [4,8]] #length 3 snake to start
food = [10,20]

# Output food
#win.addch(food[0], food[1], '*')

def get_keypress(win):
    return win.getch()

def update_LEDs(pixels):
    #write char to list
    #write list
    pass

def update_terminal(win, pixels):
    #write char
    pass

def change_direction(curr, new):
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

# Return the position after adding the two coordinates together
# Should only be used with a keys_to_dirs move vector
def move_one(curr, move):
    return list(map(add, curr, move))

def end_game():
    print("Game OVER")

KEY_ESC = 27
alive = True
direction = keys_to_dirs.get(KEY_RIGHT) # move to the right on startup

# Display start screen
curses.napms(1000)

snakeIO = DebugIO()

while alive:
    win.timeout(150 - (len(snake)/5 + len(snake)/10)%120) #increase speed when longer?



    # Get key
    prevKey = key
    event = snakeIO.get_keypress(win)#get_keypress(win)
    key = key if event == -1 else event # if get keypress returns -1, no new keypress

    # TODO: change control flow of get key press
    # Change direction if new, valid key pressed
    if key == KEY_ESC:
        break
    if key != prevKey:
        if key in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN]:
            direction = change_direction(direction, keys_to_dirs.get(key))

    # Add on the new head to the snake - remove the tail later [1]
    snake.insert(0, move_one(snake[0], direction))

    # Check for an illegal move
    if not legal_move(snake):
        break

    # Check if food is eaten
    if snake[0] == food:
        score += 1
        last = []
        food = [randint(1, yLEDs-2), randint(1, xLEDs-2)]
        # Make sure food is not generated inside of snake
        while food in snake:
            food = [randint(1, yLEDs-2), randint(1, xLEDs-2)]
    else:
        # [1] Did not eat food so remove tail of snake
        trail = snake.pop()

    # Output new frame, respective IO class will update display as necessary
    snakeIO.output(win, snake, trail, food)

    # Output debug info
    snakeIO.debug_score(win, score)

curses.napms(1000)

# Display lose msg



curses.endwin()
print("\nScore - " + str(score))
