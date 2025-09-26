class Ship:
    def __init__(self, name: str, length: int):
        self.name = name
        self.length = length
        self.positions = []
        self.hits = []

    def occupies(self, coord):
        if coord in self.positions:
            return True
        else:
            return False

    def register_hit(self, coord):
        if self.occupies(coord) and coord not in self.hits:
            self.hits.append(coord)

    def is_sunk(self):
        for pos in self.positions:
            if pos not in self.hits:
                return False
        return True




