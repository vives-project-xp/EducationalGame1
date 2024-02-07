class Object:
    def __init__(self, game_state) -> None:
        self.image = None
        self.position = (0, 0)
        self.game_state = game_state

    def place(self, position):
        self.position = position

    def remove(self):
        self.position = (0, 0)