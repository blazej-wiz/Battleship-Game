from src.board import Board
from src.battleships import Ship

class Game:
    def __init__(self, player1_name, player2_name, fleet1, fleet2):
        # Initialize players
        self.player1_name = player1_name
        self.player2_name = player2_name

        # Each player gets their own board
        self.board_p1 = Board()
        self.board_p2 = Board()

        # Each player starts with a copy of their fleet (list of ships to place)
        self.fleet1 = fleet1
        self.fleet2 = fleet2

        # Track whose turn it is (1 = Player 1, 2 = Player 2)
        self.current_player = 1

    def place_ship(self, player, ship_name, length, coord, orientation):
        # Place a ship on the given players board at the specified coordinate
        # and Removes the ship from the players fleet if placed successfully
        ship = Ship(ship_name, length)
        if player == 1:
            success = self.board_p1.place_ship(ship, coord, orientation)
            if success:
                self.fleet1.remove((ship_name, length))
            return success
        elif player == 2:
            success = self.board_p2.place_ship(ship, coord, orientation)
            if success:
                self.fleet2.remove((ship_name, length))
            return success
        return False

    def place_fleet(self, player):
        # Check if a players fleet has been completely placed
        # Returns True if no ships left to place
        if player == 1:
            return len(self.fleet1) == 0
        elif player == 2:
            return len(self.fleet2) == 0
        return False

    def fire(self, player, coord):
        # Handle firing at the opponents board
        # Returns the result string ('Hit', 'Miss', 'Sunk' etc)
        if player == 1:
            return self.board_p2.fire_at(coord)
        elif player == 2:
            return self.board_p1.fire_at(coord)
        return 'Invalid player'

    def get_board(self, player):
        # Return the grid of the specified players board for display in GUI
        if player == 1:
            return self.board_p1.get_grid()
        elif player == 2:
            return self.board_p2.get_grid()
        return None

    def is_game_over(self):
        # Check if all ship of a player are sunk
        # Returns
        # 0 = Games still going
        # 1 = Player 1 wins
        # 2 = Player 2 wins

        # Check player 1 ships
        all_sunk_p1 = True
        for ship in self.board_p1.ships:
            if not ship.is_sunk():
                all_sunk_p1 = False
                break

        # Check player 2 ships
        all_sunk_p2 = True
        for ship in self.board_p2.ships:
            if not ship.is_sunk():
                all_sunk_p2 = False
                break

        if all_sunk_p1:
            return 2
        if all_sunk_p2:
            return 1
        return 0


    def switch_turn(self):
        # Switch the current player
        self.current_player = 2 if self.current_player == 1 else 1
























# fleet1 = [('Destroyer', 3)]
# fleet2 = [('Bob', 2)]
#
# player_1 = input('Enter Player 1 name:')
# player_2 = input('Enter Player 2 name:')
#
# board_p1 = Board()
# board_p2 = Board()
#
#
# def prompt_for_coord(board):
#     while True:
#         coord_input = input('Enter the coordinate:').upper()
#         coord_input = coord_input.replace(' ', '')
#         if not board.in_bounds(coord_input):
#             print('Invalid Coord')
#         else:
#             return coord_input
#             break
#
# def prompt_for_orientation():
#     while True:
#         orientation_input = input('Enter the orientation (H/V): ').upper()
#         orientation_input = orientation_input.replace(' ', '')
#         if orientation_input == 'H':
#             return 'horizontal'
#
#         elif orientation_input == 'V':
#             return 'vertical'
#
#         else:
#             print('Invalid orientation, try again')
#
#
# def place_one_ship(board, player_name, ship_name, length):
#     print('{name} place your {ship_name}, {length}'.format(name = player_name, ship_name = ship_name, length = length))
#     while True:
#         coord_input = prompt_for_coord(board)
#         orientation_input = prompt_for_orientation()
#         ship = Ship(ship_name, length)
#         placement = board.place_ship(ship, coord_input, orientation_input)
#         if placement == True:
#             print('Placed succesfully!')
#
#             break
#         else:
#             print('Invalid placement (overlap/out of bounds). Try again')
#
#
# def place_fleet(board, player_name, fleet):
#     print('{player_name}, place your fleet'.format(player_name = player_name))
#     for ship_name, length in fleet:
#         place_one_ship(board, player_name, ship_name, length)
#         board.render()
#
#
# # place_fleet(board_p1, player_1, fleet1)
# # place_fleet(board_p2, player_2, fleet2)
#
# def prompt_for_fire(board):
#     while True:
#         coord_input = prompt_for_coord(board)
#         if not board.get(coord_input) == 'X' and not board.get(coord_input) == 'O':
#             return coord_input
#         else:
#             print('Already fired at that coord, try again')
#
# def take_turn(attacker_name, defender_board):
#     print('{player_name} turn'.format(player_name = attacker_name))
#     coord = prompt_for_fire(defender_board)
#     result = defender_board.fire_at(coord)
#     print('{player_name} fired at', coord, ':', result.format(player_name = attacker_name))
#     defender_board.render()
#
# def all_sunk(board):
#     for ship in board.ships:
#         if not ship.is_sunk():
#             return False
#     return True
#
#
# attacker_name = player_1
# defender_board = board_p2
# while True:
#     take_turn(attacker_name, defender_board)
#     if all_sunk(defender_board):
#         print('Game Over! {player_name} wins!'.format(player_name = attacker_name))
#         break
#     if attacker_name == player_1 and defender_board == board_p2:
#         attacker_name = player_2
#         defender_board = board_p1
#     else:
#         attacker_name = player_1
#         defender_board = board_p2
#
#






