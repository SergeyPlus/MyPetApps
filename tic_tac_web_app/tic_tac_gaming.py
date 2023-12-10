from typing import Dict, List
import random
import logging

logging.basicConfig(level=10, format='%(asctime)s : %(message)s')
logger = logging.getLogger(__name__)


# This list contents of 0 by default and this list collects values of each turn made by Players during the round of
# game. If Player puts "X" correspondent value of the list will be incremented by 1, if "0" incremented by 10
game_field: List[int] = [0] * 9


def complete_field(turn_dict: Dict) -> None:
    """
    This function puts integers into game_field according to Players turns. Index of game_field identifying
    through key of received dict (turn_dic) - the last symbol is a number of cell.
    """
    logger.info(f'Starting completing game field')
    player_turn: str = ''
    node_index: int = 0
    for key, value in turn_dict.items():
        if value:
            player_turn: str = turn_dict[key]
            node_index: int = int(key[-1])
            break
    logger.info(f'Received symbol is {player_turn} and index for game_field {node_index}')

    if player_turn.lower() == 'x':
        game_field[node_index] = 1
        logger.info(f'Value to the game_field list - {1}')
    if player_turn == '0':
        game_field[node_index] = 10
        logger.info(f'Value to the game_field list - {10}')


def check_winner() -> str:
    """
    If summ is 30 winner the player who puts '0'.
    If summ is 3 winner the player who puts 'x'.
    Checking makes based on inspection of sum cells in horizontal
    _ _ _
    _ _ _
    X X X

    or vertical
    _ _ X
    _ _ X
    _ _ X

    or diagonals
    X _ X
    _ X _
    X _ X
    """
    logger.info(f'Starting checking of the winner')
    summ: int = 0
    horizontal_check: List[int] = []
    vertical_check: List[int] = []

    # horizontal checking
    for i in range(0, len(game_field), 3):
        for k in range(3):
            k += i
            if k < (i + 2):
                summ += game_field[k]
            elif k == (i + 2):
                summ += game_field[k]
                horizontal_check.append(summ)
                summ = 0
    logger.info(f'Calculated horizontal list {vertical_check}')

    # vertical checking
    for i in range(3):
        for k in range(0, len(game_field), 3):
            k += i
            if k < (i + 6):
                summ += game_field[k]
            elif k == (i + 6):
                summ += game_field[k]
                vertical_check.append(summ)
                summ = 0
    logger.info(f'Calculated vertical list {horizontal_check}')

    # diagonal checking
    diagonal_check_1 = sum([game_field[i] for i in (0, 4, 8)])
    logger.info(f'Calculated diagonal 1 {diagonal_check_1}')

    diagonal_check_2 = sum([game_field[i] for i in (2, 4, 6)])
    logger.info(f'Calculated diagonal 2 {diagonal_check_2}')

    if 3 in horizontal_check or 3 in vertical_check or diagonal_check_1 == 3 or diagonal_check_2 == 3:
        return 'x'

    if 30 in horizontal_check or 30 in vertical_check or diagonal_check_1 == 30 or diagonal_check_2 == 30:
        return '0'




def identify_symbol() -> str:
    """
    The function identifies who plays by "X" automatically
    """
    rand_num: int = random.randint(0, 1)
    if rand_num:
        logger.info(f'Automatically chosen "X" for player')
        return 'x'


def check_symbols_quantity_for_turn(resp: Dict) -> bool:
    """
    The function checks quantity symbols which player put during his turn. It's not possible make
    more than 1 symbols
    """
    logger.info(f'Starting checking of symbols quantity per 1 turn')
    count: int = 0
    for key, value in resp.items():

        if value == 'x' or value == '0' or value == 'X':

            count += 1
        if count > 1:
            logger.debug(f'Player puts 2 symbols')
            return False
    if count == 0:
        return False

    logger.debug(f'Player puts 1 symbols')
    return True


if __name__ == '__main__':
    pass