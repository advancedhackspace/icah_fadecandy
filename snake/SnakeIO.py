class DebugIO():
    SNAKE_CHAR = '#'
    FOOD_CHAR = '*'
    TRAIL_CHAR = ' '

    def setup(self):
        '''Setup the input'''
        pass

    def get_keypress(self, win):
        '''Get a keypress'''
        return win.getch()

    # Write the head of the snake
    # Erase the snake's trail, if there is one
    # Write the food
    def output(self, win, snake, trail, food):
        win.addch(food[0], food[1], self.FOOD_CHAR)
        win.addch(snake[0][0], snake[0][1], self.SNAKE_CHAR)
        if trail: win.addch(trail[0], trail[1], self.TRAIL_CHAR)

    # TODO make this more general, add more decoration etc
    def debug_score(self, win, score):
        win.addstr(31, 2, "Score: " + str(score))

    def cleanup(self):
        '''Cleanup the input'''
        pass

class LEDIO():
    def setup(self):
        pass
