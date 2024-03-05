class Resolution:
    def __init__(self):
        self.width = 1920
        self.height = 1000
        self.GRID_SIZE = self.width // 32

    def set_resolution(self, width, height):
        self.width = width
        self.height = height
        self.GRID_SIZE = self.width // 32 


