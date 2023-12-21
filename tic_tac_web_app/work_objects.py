from typing import Dict, List, Tuple
import random
import logging
from logging import config
from enum import Enum
from werkzeug.security import check_password_hash
from data_base import UserDbInterface, UserDb
from config import LoggerConfig

wo_logger = logging.getLogger('wo_logger')
wo_logger.propagate = False
config.dictConfig(LoggerConfig.log_config_dict)


class Players:
    """
    Monostate class allows to initialize instances and deal with them as with Dict
    """
    players_data = {
        'name_1': '',
        'name_2': '',
        'sym_1': '0',
        'sym_2': 'x',
        'score_1': 0,
        'score_2': 0
    }

    def __init__(self):
        self.__dict__ = self.players_data

    def __getattr__(self, item):
        """
        In order to predict mistake of specifying of not exists attribute during developing
        """
        raise AttributeError('Please choose key in accordance with specified in players_data')

    def __repr__(self):
        return '; '.join([f'{key}: {value}' for key, value in self.players_data.items()])

    @classmethod
    def clear_for_new_game(cls):
        cls.name_1 = ''
        cls.name_2: str = ''
        cls.score_1: int = 0
        cls.score_2: int = 0
        cls.sym_1: str = ''
        cls.sym_2: str = ''


class Constants(Enum):
    CROSS: int = 1
    ZERO: int = 10
    SYM_CROSS: str = 'x'
    SYM_ZERO: str = '0'


class Game:

    # This list contents of 0 by default and this list collects values of each turn made by Players during the round of
    # game. If Player puts "X" correspondent value of the list will be incremented by 1, if "0" incremented by 10
    GAME_FIELD: List[int] = [0] * 9
    tic_tac_table: Dict = {}
    flag = 0
    winner = None

    @classmethod
    def restart_game_with_same_players(cls) -> None:
        """
        It clears attrs GAME_FIELD, winner and tic_tac_table.
        Flag is stays up because Players shouldn't be changed.
        """
        cls.winner = ''
        cls.tic_tac_table.clear()
        cls.GAME_FIELD = [0] * 9
        wo_logger.info(
            f'Data cleared: [GAME_FIELD: {cls.GAME_FIELD}, winner: {cls.winner}, tic_tac_table: {cls.tic_tac_table}]')

    @classmethod
    def restart_game_with_new_players(cls) -> None:
        """
        It clears attrs GAME_FIELD, winner, tic_tac_table and flag.
        """
        players = Players()
        cls.winner = ''
        cls.tic_tac_table.clear()
        cls.GAME_FIELD = [0] * 9
        cls.flag = 0

        players.players_data = {
            'name_1': '',
            'name_2': '',
            'sym_1': '0',
            'sym_2': 'x',
            'score_1': 0,
            'score_2': 0
        }

        wo_logger.info(
            f'Data cleared: '
            f'[GAME_FIELD: {cls.GAME_FIELD}, winner: {cls.winner}, '
            f'tic_tac_table: {cls.tic_tac_table}, flag = {cls.flag}]')
        wo_logger.info(f'Players_data cleared as well: {players}')

    @classmethod
    def complete_field(cls, turn_dict) -> Dict:
        """
        This function puts integers into game_field according to Players turns. Index of game_field identifying
        through key of received dict (turn_dic) - the last symbol is a number of cell.
        """
        wo_logger.info(f'Starting completing game field')
        player_turn: str = ''
        node_index: int = 0
        for key, value in turn_dict.items():
            if value:
                player_turn: str = turn_dict[key]
                node_index: int = int(key[-1])

                cls.tic_tac_table[key] = f'__{value}__'
                break
        wo_logger.info(f'Received symbol is {player_turn} and index for game_field {node_index}')

        if player_turn.lower() == Constants.SYM_CROSS.value:
            cls.GAME_FIELD[node_index] = Constants.CROSS.value
            wo_logger.info(f'Value to the game_field list - {1}')
        if player_turn == Constants.SYM_ZERO.value:
            cls.GAME_FIELD[node_index] = Constants.ZERO.value
            wo_logger.info(f'Value to the game_field list - {10}')

        return cls.tic_tac_table

    @classmethod
    def check_winner(cls) -> None:
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
        wo_logger.info(f'Starting checking of the winner')
        summ: int = 0
        horizontal_check: List[int] = []
        vertical_check: List[int] = []

        # horizontal checking
        for i in range(0, len(cls.GAME_FIELD), 3):
            for k in range(3):
                k += i
                if k < (i + 2):
                    summ += cls.GAME_FIELD[k]
                elif k == (i + 2):
                    summ += cls.GAME_FIELD[k]
                    horizontal_check.append(summ)
                    summ = 0
        wo_logger.info(f'Calculated horizontal list {vertical_check}')

        # vertical checking
        for i in range(3):
            for k in range(0, len(cls.GAME_FIELD), 3):
                k += i
                if k < (i + 6):
                    summ += cls.GAME_FIELD[k]
                elif k == (i + 6):
                    summ += cls.GAME_FIELD[k]
                    vertical_check.append(summ)
                    summ = 0
        wo_logger.info(f'Calculated vertical list {horizontal_check}')

        # diagonal checking
        diagonal_check_1 = sum([cls.GAME_FIELD[i] for i in (0, 4, 8)])
        wo_logger.info(f'Calculated diagonal 1 {diagonal_check_1}')

        diagonal_check_2 = sum([cls.GAME_FIELD[i] for i in (2, 4, 6)])
        wo_logger.info(f'Calculated diagonal 2 {diagonal_check_2}')

        if 3 in horizontal_check or 3 in vertical_check or diagonal_check_1 == 3 or diagonal_check_2 == 3:
            cls.__identify_winner(Constants.SYM_CROSS.value)

        if 30 in horizontal_check or 30 in vertical_check or diagonal_check_1 == 30 or diagonal_check_2 == 30:
            cls.__identify_winner(Constants.SYM_ZERO.value)

    @classmethod
    def __identify_winner(cls, sym) -> None:
        """
        It initializes winner value. Put their Player instance
        """
        wo_logger.info(f'There is a win situation with {sym}')
        players = Players()
        if sym == players.players_data['sym_1']:
            cls.winner = players.players_data['name_1']
            players.players_data['score_1'] += 1
        else: # sym == players.players_data['sym_2']
            cls.winner = players.players_data['name_2']
            players.players_data['score_2'] += 1
        wo_logger.info(
            f'Winner name {Game.winner}. Score player_1 and player_2 {players}')

    @classmethod
    def identify_symbol(cls) -> None:
        """
        The function identifies who plays by "X" automatically
        """
        rand_num: int = random.randint(0, 1)
        players = Players()
        if rand_num:
            players.players_data['sym_1'] = 'x'
            players.players_data['sym_2'] = '0'
        wo_logger.info(
            f'Identified symbols for Player_1 and Player_2 {players}')

    @classmethod
    def check_symbols_quantity_for_turn(cls, resp: Dict) -> bool:
        """
        The function checks quantity symbols which player put during his turn. It's not possible make
        more than 1 symbols
        """
        wo_logger.info(f'Starting checking of symbols quantity per 1 turn')
        count: int = 0
        for key, value in resp.items():

            if value == Constants.SYM_CROSS.value or value == Constants.SYM_ZERO.value:
                count += 1

            if count > 1:
                wo_logger.debug(f'Error: Player puts 2 symbols')
                return False
        return count == 1

    @classmethod
    def finalize_field(cls) -> Dict:
        """
        In case of win situation it's necessary to render final field and in this case empty cells
        should be completed by such symbols _____
        """
        for key, value in cls.tic_tac_table.items():
            if not value:
                cls.tic_tac_table[key] = '_____'
        wo_logger.info(f'Finalizing field starting. From now all field cells are completed {cls.tic_tac_table}')
        return cls.tic_tac_table


class Login:
    """
    Includes methods which allows to check login and password during log in
    """
    @classmethod
    def check_login(cls, form) -> bool:
        """
        Checks is there login in tic_tac.db if login is existed User cannot take it and should create new one
        """
        user_data: UserDb = UserDbInterface.get_user_data(form.login.data)
        return not user_data['login']

    @classmethod
    def check_login_and_password(cls, form) -> bool:
        """
        Checks are there password and login in tic_tac.db. If so the User is authorized.
        """
        user_data: UserDb = UserDbInterface.get_user_data(form.login.data)
        return user_data['login'] == form.login.data and check_password_hash(user_data['password'], form.password.data)


if __name__ == '__main__':
    ...