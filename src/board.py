from src.battleships import Ship


class Board:
    def __init__(self):
        # Board is always 10x10
        self.size = 10
        # Row labels (numbers shown on the left in render)
        self.rows = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        # Column labels (letters shown across the top in render)
        self.columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        # The grid itself: a 2D list of dots ('.') for empty cells
        self.grid = [['.' for i in range(self.size)] for i in range(self.size)]
        self.ships = []

    def render(self):
        # Print header row with column letters
        print("   " + " ".join(self.columns))
        # Print each row with its row number and contents
        row_number = 1
        for row in self.grid:
            # rjust(2) makes single digits align with "10"
            print(str(row_number).rjust(2), ' '.join(row))
            row_number += 1
        return

    def in_bounds(self, coord):
        valid = True
        letter_part = coord[0]
        number_part = coord[1:]
        if (letter_part not in self.columns) or (number_part not in self.rows):
            valid = False
        return valid

    def to_index(self, coord):
        letter_part = coord[0]
        number_part = coord[1:]
        # Column index is position of the letter in self.columns
        col_index = self.columns.index(letter_part)
        # Row index is position of the number in self.rows
        row_index = self.rows.index(number_part)
        # Return in (row, col) order, since grid is accessed as grid[row][col]
        return (row_index, col_index)

    def get(self, coord: str):
        # Return the symbol stored at a given coordinate.
        row, col = self.to_index(coord)
        return self.grid[row][col]

    def set(self, coord: str, value: str):
        #Set a symbol at a given coordinate (e.g. place ship or mark hit)
        row, col = self.to_index(coord)
        self.grid[row][col] = value
        return

    def place_ship(self, ship, start_coord, orientation):
        row, col = self.to_index(start_coord)
        new_positions = []
        for i in range(0, ship.length):
            if orientation == 'horizontal':
                row_index, col_index = (row, col + i)
            elif orientation == 'vertical':
                row_index, col_index = (row + i, col)
            if not (0 <= row_index < self.size and 0 <= col_index < self.size):
                return False
            converted_positions = self.columns[col_index] + self.rows[row_index]
            new_positions.append(converted_positions)
        for position in new_positions:
            if not self.in_bounds(position):
                return False
        for position in new_positions:
            if not self.get(position) == '.':
                return False
        for position in new_positions:
            self.set(position, 'S')
        ship.positions = new_positions
        self.ships.append(ship)
        return True

    def fire_at(self, coord):
        if not self.in_bounds(coord):
            return 'Invalid'
        if self.get(coord) == 'X' or self.get(coord) == 'O':
            return 'Already Tried'
        elif self.get(coord) == '.' or self.get(coord) == 'S':
            for ship in self.ships:
                if ship.occupies(coord):
                    self.set(coord, 'X')
                    ship.register_hit(coord)
                    if ship.is_sunk() == True:
                        return 'Sunk {name}'.format(name = ship.name)
                    else:
                        return 'Hit'
            self.set(coord, 'O')
            return 'Miss'



































