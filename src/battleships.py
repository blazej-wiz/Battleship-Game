class Ship:
    def __init__(self, name: str, length: int):
        # Each ship has a name (e.g., "Destroyer") and a length (number of cells it occupies)
        self.name = name
        self.length = length
        # List of coordinates this ship occupies on the board
        self.positions = []
        # List of coordinates where this ship has been hit
        self.hits = []

    def occupies(self, coord):
        # Return true if the ship currently occupies the given coordinate
        if coord in self.positions:
            return True
        else:
            return False

    def register_hit(self, coord):
        # Mark a hit on this ship at the given coordinate, but only if:
        # - The ship actually occupies that coordinate
        # - The coordinate hasn’t already been recorded as a hit
        if self.occupies(coord) and coord not in self.hits:
            self.hits.append(coord)

    def is_sunk(self):
        # A ship is sunk if all of its positions have been hit
        for pos in self.positions:
            if pos not in self.hits:
                return False
        return True




