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

    # Return the entire 2D grid (for rendering in the GUI)
    def get_grid(self):
        return self.grid


    def in_bounds(self, coord):
        # Check if a coordinate string (like "C4") is valid and on the board
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
        # Try to place a ship at a starting coordinate in the given orientation
        row, col = self.to_index(start_coord)
        new_positions = []
        # Build all the coordinates the ship would occupy
        for i in range(0, ship.length):
            if orientation == 'horizontal':
                row_index, col_index = (row, col + i)
            elif orientation == 'vertical':
                row_index, col_index = (row + i, col)

            # Immediately reject if any part goes out of bounds
            if not (0 <= row_index < self.size and 0 <= col_index < self.size):
                return False
            # Convert row/col indices back into "A1" style coordinate
            converted_positions = self.columns[col_index] + self.rows[row_index]
            new_positions.append(converted_positions)

        # Validate all positions:
        for position in new_positions:
            # Must be on the board
            if not self.in_bounds(position):
                return False
        # Must not overlap existing ships
        for position in new_positions:
            if not self.get(position) == '.':
                return False
        # Place the ship on the board (mark with 'S')
        for position in new_positions:
            self.set(position, 'S')
        # Save the ship's occupied positions and store the ship
        ship.positions = new_positions
        self.ships.append(ship)
        return True

    def fire_at(self, coord):
        # Handle firing at a coordinate (returns a result string)
        if not self.in_bounds(coord):
            return 'Invalid' # Shot outside of board
        # Prevent duplicate shots
        if self.get(coord) == 'X' or self.get(coord) == 'O':
            return 'Already Tried'
        # Otherwise evaluate the shot
        elif self.get(coord) == '.' or self.get(coord) == 'S':
            for ship in self.ships:
                if ship.occupies(coord): # Check if a ship is here
                    self.set(coord, 'X') # Mark as hit
                    ship.register_hit(coord)
                    # If this hit sank the ship
                    if ship.is_sunk() == True:
                        return 'Sunk {name}'.format(name = ship.name)
                    else:
                        return 'Hit'
            # If no ship was there mark miss
            self.set(coord, 'O')
            return 'Miss'



































