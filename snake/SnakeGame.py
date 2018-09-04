import csv


class SnakeGame:
    LB_FILE = "leader_board.csv"

    def __init__(self, sim_io, led_io, mode):
        self.sim_io = sim_io
        self.led_io = led_io

        # TODO: define different modes later
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

    # TODO
    def add_score(self):
        for entry in self.leader_board:
            pass

    def get_walls_enabled(self):
        return self.walls_enabled

    def get_speed_increases(self):
        return self.speed_increases

    def cleanup(self):
        self.save_leader_board()
        self.sim_io.cleanup()
        self.led_io.cleanup()