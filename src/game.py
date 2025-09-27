from src.board import Board
from src.battleships import Ship

fleet1 = [('Destroyer', 3)]
fleet2 = [('Bob', 2)]

player_1 = input('Enter Player 1 name:')
player_2 = input('Enter Player 2 name:')

board_p1 = Board()
board_p2 = Board()


def prompt_for_coord(board):
    while True:
        coord_input = input('Enter the coordinate:').upper()
        coord_input = coord_input.replace(' ', '')
        if not board.in_bounds(coord_input):
            print('Invalid Coord')
        else:
            return coord_input
            break

def prompt_for_orientation():
    while True:
        orientation_input = input('Enter the orientation (H/V): ').upper()
        orientation_input = orientation_input.replace(' ', '')
        if orientation_input == 'H':
            return 'horizontal'

        elif orientation_input == 'V':
            return 'vertical'

        else:
            print('Invalid orientation, try again')


def place_one_ship(board, player_name, ship_name, length):
    print('{name} place your {ship_name}, {length}'.format(name = player_name, ship_name = ship_name, length = length))
    while True:
        coord_input = prompt_for_coord(board)
        orientation_input = prompt_for_orientation()
        ship = Ship(ship_name, length)
        placement = board.place_ship(ship, coord_input, orientation_input)
        if placement == True:
            print('Placed succesfully!')

            break
        else:
            print('Invalid placement (overlap/out of bounds). Try again')


def place_fleet(board, player_name, fleet):
    print('{player_name}, place your fleet'.format(player_name = player_name))
    for ship_name, length in fleet:
        place_one_ship(board, player_name, ship_name, length)
        board.render()


# place_fleet(board_p1, player_1, fleet1)
# place_fleet(board_p2, player_2, fleet2)

def prompt_for_fire(board):
    while True:
        coord_input = prompt_for_coord(board)
        if not board.get(coord_input) == 'X' and not board.get(coord_input) == 'O':
            return coord_input
        else:
            print('Already fired at that coord, try again')

def take_turn(attacker_name, defender_board):
    print('{player_name} turn'.format(player_name = attacker_name))
    coord = prompt_for_fire(defender_board)
    result = defender_board.fire_at(coord)
    print('{player_name} fired at', coord, ':', result.format(player_name = attacker_name))
    defender_board.render()

def all_sunk(board):
    for ship in board.ships:
        if not ship.is_sunk():
            return False
    return True


attacker_name = player_1
defender_board = board_p2
while True:
    take_turn(attacker_name, defender_board)
    if all_sunk(defender_board):
        print('Game Over! {player_name} wins!'.format(player_name = attacker_name))
        break
    if attacker_name == player_1 and defender_board == board_p2:
        attacker_name = player_2
        defender_board = board_p1
    else:
        attacker_name = player_1
        defender_board = board_p2








