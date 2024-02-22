class Game:
    def __init__(self):
        self.ready = False
        self.player = 'yellow'
        self.col = None
        self.running = False
        self.row_counter = None
        self.error = None
        self.turn = None
        self.starter = None

    def connected(self):
        return self.ready
