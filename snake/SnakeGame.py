import csv


class SnakeGame:
    LB_FILE = "/Users/Matt/Projects/icah_fadecandy/snake/leader_board.csv"
    MAX_SNAKE_SCORE = 99999
    LEADER_BOARD_SIZE = 5

    def __init__(self, sim_io, led_io, mode):
        self.sim_io = sim_io
        self.led_io = led_io

        if mode == 'easy':
            self.walls_enabled = False
            self.speed_increases = False
        else:
            self.walls_enabled = True
            self.speed_increases = True

        self.leader_board = self.load_leader_board()

    def load_leader_board(self):
        with open(self.LB_FILE) as lb:
            reader = csv.reader(lb, delimiter=',')
            return {rows[0]: int(rows[1]) for rows in reader}

    def save_leader_board(self):
        with open(self.LB_FILE, 'w') as lb:
            for entry in self.leader_board:
                lb.write(entry + ", " + str(self.leader_board[entry]) + "\n")

    def add_score(self, score, name):
        # If less than max, add
        evict = False
        if len(self.leader_board) < self.LEADER_BOARD_SIZE:
            self.leader_board[name] = score
        else:
            for entry in self.leader_board:
                if score > self.leader_board[entry]:
                    self.leader_board[name] = score
                    evict = True
                    break
        # If leader board was full and one was added, evict one
        if evict:
            low_score = self.MAX_SNAKE_SCORE
            low_name = ''
            for entry in self.leader_board:
                if self.leader_board[entry] < low_score:
                    low_score = self.leader_board[entry]
                    low_name = entry
            self.leader_board.pop(low_name)

    def display_leader_board(self):
        self.sim_io.display_leader_board(self.leader_board)

    def get_walls_enabled(self):
        return self.walls_enabled

    def get_speed_increases(self):
        return self.speed_increases

    def cleanup(self):
        self.save_leader_board()
        self.sim_io.cleanup()
        self.led_io.cleanup()