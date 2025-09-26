class Board:
    def __init__(self):
        self.size = 10
        self.rows = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        self.grid = [['.' for i in range(self.size)] for i in range(self.size)]

    def render(self):
        # header row (pad 3 spaces so row numbers fit underneath)
        print("   " + " ".join(self.columns))

        row_number = 1
        for row in self.grid:
            # use rjust(2) so "1" becomes " 1" and lines up with "10"
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




board = Board()

board.in_bounds('C4')



























