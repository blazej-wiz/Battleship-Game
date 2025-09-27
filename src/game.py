from src.board import Board
from src.battleships import Ship

fleet = [('Destroyer', 3), ('Alpha', 5)]

player_1 = input('Enter Player 1 name:')
player_2 = input('Enter Player 2 name:')

board_p1 = Board()


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








