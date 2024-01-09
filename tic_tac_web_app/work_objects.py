from typing import Any, Dict, List, Tuple
import random
import logging
from logging import config
from enum import Enum
from werkzeug.security import check_password_hash
from flask_mail import Message

from app import mail
from data_base import UserDbInterface, UserDb
from config import LoggerConfig

wo_logger = logging.getLogger('wo_logger')
wo_logger.propagate = False
config.dictConfig(LoggerConfig.log_config_dict)


class Players:
    """
    Monostate class allows to initialize instances and deal with them as with Dict
    """
    _players_data = {
        'name_1': '',
        'name_2': '',
        'sym_1': '0',
        'sym_2': 'x',
        'score_1': 0,
        'score_2': 0
    }

    def __init__(self):
        self.__dict__ = self._players_data

    def __repr__(self):
        return '; '.join([f'{key}: {value}' for key, value in self._players_data.items()])
    
    def clear_for_new_game(self):
        self.name_1 = ''
        self.name_2: str = ''
        self.score_1: int = 0
        self.score_2: int = 0
        self.sym_1: str = ''
        self.sym_2: str = ''

    def create_players_profiles(self, players_form) -> None:
        """
        This method set players names into players class and identifies symbols which players
        use during the game
        """

        self._players_data['name_1'] = players_form.player_1_name.data
        self._players_data['name_2'] = players_form.player_2_name.data
        self._identify_symbol()
 

    def _identify_symbol(self) -> None:
        """
        The function identifies who plays by "X" automatically
        """
        rand_num: int = random.randint(0, 1)
        if rand_num:
            self._players_data['sym_1'] = 'x'
            self._players_data['sym_2'] = '0'
        wo_logger.info(
            f'Identified symbols for Player_1 and Player_2 {self._players_data}')


class Constants(Enum):
    CROSS: int = 1
    ZERO: int = 10
    SYM_CROSS: str = 'x'
    SYM_ZERO: str = '0'


class Game:

    # This list contents of 0 by default and this list collects values of each turn made by Players during the round of
    # game. If Player puts "X" correspondent value of the list will be incremented by 1, if "0" incremented by 10

    _game_data: Dict = {
        'game_field': [0] * 9,
        'tic_tac_table': {},
        'game_render_form': 'set_player_names',
        'winner': ''
    }


    def __init__(self):
        self.__dict__ = self._game_data


    def __repr__(self):
        return '; '.join([f'{key}: {value}' for key, value in self._game_data.items()])
    

    def _complete_field(self, turn_dict: Dict) -> None:
        """
        This function puts integers into game_field according to Players turns. Index of game_field identifying
        through key of received dict (turn_dic) - the last symbol is a number of cell.
        """
        
        wo_logger.info(f'Starting completing game field')
        player_turn: str = ''
        node_index: int = 0
        for key, value in turn_dict.items():
            if value:
                player_turn: str = value
                node_index: int = int(key[-1])

                self._game_data['tic_tac_table'][key] = f'__{value}__'
                wo_logger.info(f"The turn was recorded in Game successfully {self._game_data.get('tic_tac_table')}")
                break
        wo_logger.info(f'Received symbol is {player_turn} and index for game_field {node_index}')

        if player_turn.lower() == Constants.SYM_CROSS.value:
            self._game_data['game_field'][node_index] = Constants.CROSS.value
            wo_logger.info(f'Value to the game_field list - {1}')
        elif player_turn == Constants.SYM_ZERO.value:
            self._game_data['game_field'][node_index] = Constants.ZERO.value
            wo_logger.info(f'Value to the game_field list - {10}')
        else:
            raise ValueError('Player puts incorrect symbol')


    def _horizontal_check(self) -> List[int]:
        """
        Checking of values on horizontal lines
        _ _ _
        _ _ _
        X X X
        """
        horizontal_check: List[int] = []
        summ: int = 0
        for i in range(0, len(self._game_data['game_field']), 3):
            for k in range(3):
                k += i
                summ += self._game_data['game_field'][k]
                if k == (i + 2):
                    horizontal_check.append(summ)
                    summ = 0
        wo_logger.info(f'Calculated horizontal list {horizontal_check}')
        return horizontal_check


    def _vertical_check(self) -> List[int]:
        """
        Checking of values on vertical lines 
        _ _ X
        _ _ X
        _ _ X
        """
        vertical_check: List[int] = []
        summ: int = 0
        for i in range(3):
            for k in range(0, len(self._game_data['game_field']), 3):
                k += i
                summ += self._game_data['game_field'][k]
                if k == (i + 6):
                    vertical_check.append(summ)
                    summ = 0
        wo_logger.info(f'Calculated vertical list {vertical_check}')
        return vertical_check


    def _diagonals_check(self) -> Tuple:
        """
        Checking of values on diagonals lines 
        X _ X
        _ X _
        X _ X
        """

        diagonal_check_1 = sum([self._game_data['game_field'][i] for i in (0, 4, 8)])
        wo_logger.info(f'Calculated diagonal_1 {diagonal_check_1}')

        diagonal_check_2 = sum([self._game_data['game_field'][i] for i in (2, 4, 6)])
        wo_logger.info(f'Calculated diagonal_2 {diagonal_check_2}')
        return diagonal_check_1, diagonal_check_2


    def _check_winner(self) -> None:
        """
        If summ is 30 winner the player who puts '0'.
        If summ is 3 winner the player who puts 'x'.
        Checking makes based on inspection of sum cells in horizontal        
        """
        wo_logger.info(f'Starting checking of the winner')
        horizontal_check: List[int] = self._horizontal_check()
        vertical_check: List[int] = self._vertical_check()
        diagonals_check: List = self._diagonals_check()
        

        if 3 in horizontal_check or 3 in vertical_check or 3 in diagonals_check:
            self._identify_winner(Constants.SYM_CROSS.value)

        elif 30 in horizontal_check or 30 in vertical_check or 30 in diagonals_check:
            self._identify_winner(Constants.SYM_ZERO.value)

        wo_logger.info(f'Before win-win checking. {self._game_data}')
        if not self._game_data['winner'] and len(self._game_data.get('tic_tac_table', {})) == 9:
            wo_logger.info(f"Win - Win situation")
            self._identify_winner('win-win')
        
 
    def _identify_winner(self, sym) -> None:
        """
        It initializes winner value. Put their Player instance
        """
        wo_logger.info(f'There is a win situation with {sym}')
        players = Players()
        if sym == players._players_data['sym_1']:
            self._game_data['winner'] = players._players_data['name_1']
            players._players_data['score_1'] += 1
        elif sym == players._players_data['sym_2']:
            self._game_data['winner'] = players._players_data['name_2']
            players._players_data['score_2'] += 1
        else:
            players._players_data['score_1'] += 1
            players._players_data['score_2'] += 1
            self._game_data['winner'] = f" both players {players._players_data['name_1']} and {players._players_data['name_2']} win"
        wo_logger.info(
            f'Winner name {self}. Score player_1 and player_2 {players}')
        self._finalize_field()


    def _check_symbols_quantity_for_turn(self, resp: Dict) -> bool:
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


    def _finalize_field(self) -> None:
        """
        In case of win situation it's necessary to render final field and in this case empty cells
        should be completed by such symbols _____
        """
        for key, value in self._game_data['tic_tac_table'].items():
            wo_logger.info(f'From __finalize_field {key} , {value}')
            if not value:
                self._game_data['tic_tac_table'][key] = '_____'
        wo_logger.info(f'Finalizing field starting. From now all field cells are completed {self._game_data}')


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


class SendMail:
    
    @classmethod
    def send_mail(password: str, login: str):
        """
        The method send the message with password to the User email which is used during
        registration
        """
        user_data: UserDb = UserDbInterface.get_user_data(login)
        subject = 'From Tic-tac app'
        email_message: str = (f'Hello {user_data["name"]}! '
                                f'\nThis is tic_tac support team. Your NEW password is {password}. '
                                f'\n\nLooking forward You playing in our app!')
        msg = Message(body=email_message,
                        sender='seregasun@list.ru',
                        recipients=[user_data["email"]],
                        subject=subject)
        mail.send(msg)


class GameManager:
    """
    The class constructor initializing instances of Plasyers nd Game classes 
    """
    def __init__(self):
        self.players = Players()
        self.game = Game()
        
        
    def __getitem__(self, key: str):
        
        if key == 'game_data':
            return self.game._game_data
        elif key == 'players_data':
            return self.players._players_data
        
        raise KeyError('Please use correct keys for getting data from game and player instances')
    
    def __setitem__(self, key: str, value):
        
        if key in self.game._game_data:
            self.game._game_data[key] = value
        elif key in self.players._players_data:
            self.players._players_data[key] = value
        else:
            raise KeyError('Please use correct keys for getting data from game and player instances')

    def game_manager(self, response: Dict) -> None:
        """
        The method calls functions __complete_field and __check_winner after symbols per turn
        checking
        """
        wo_logger.info(f'Game manager is starting to work.')
        if not isinstance(response, dict):
            raise TypeError('The response type for game_manager method should be a dict')
        
        elif len(response) != 9:
            raise IndexError('The response should consists of 9 keys and values pairs')
        
        if not self.game._check_symbols_quantity_for_turn(response):
            raise ValueError("The checking of symbols quantity passed not well")
                
        wo_logger.info(f'The checking of symbols quantity passed well')
                
        self.game._complete_field(response)
        self.game._check_winner()
        wo_logger.info(f'Game context {self["game_data"]}')

    def restart_game_with_same_players(self) -> None:
        """
        It clears attrs GAME_FIELD, winner and tic_tac_table.
        Game_render_form is stays up because Players shouldn't be changed.
        """
        
        self['game_data']['winner'] = ''
        self['game_data']['tic_tac_table'].clear()
        self['game_data']['game_field'] = [0] * 9

        wo_logger.info(
            f'Data updated: {self["game_data"]}')

    def restart_game_with_new_players(self) -> None:
        """
        It clears attrs game_field, winner, tic_tac_table and game_render_for.
        """
   
        self.restart_game_with_same_players()
        self['game_data']['game_render_form'] = 'set_player_names'

        self.players._players_data = {
            'name_1': '',
            'name_2': '',
            'sym_1': '0',
            'sym_2': 'x',
            'score_1': 0,
            'score_2': 0
        }

        wo_logger.info(f'Data cleared: {self}')
        wo_logger.info(f'Players_data cleared as well: {self.players}')

    def change_reneder_form(self, regim: str) -> None:
        """
        It changes forms for rendering during a game. 
        If regim is "game" it renders form with game field
        If regim is "set_player_names" it renders form with players introduction
        """
        self['game_data']['game_render_form'] = regim




if __name__ == '__main__':
    ...