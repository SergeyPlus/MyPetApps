import unittest
from typing import Dict, List, Tuple

from work_objects import GameManager


class TestGame(unittest.TestCase):

    def setUp(self) -> None:
        self.game_manager = GameManager()

    def tearDown(self) -> None:
        default_game_data = {
            'game_field': [0] * 9,
            'tic_tac_table': {},
            'game_render_form': 'game',
            'winner': ''
        }
        for key, value in default_game_data.items():
            self.game_manager[key] = value
        self.game_manager.players.clear_for_new_game()

    def test_context_game_defaulting(self):
        expect_game_context: Dict = {
            'game_field': [0] * 9,
            'tic_tac_table': {},
            'game_render_form': 'game',
            'winner': ''
        }

        test_game_context: Dict = {
            'game_field': [0, 1, 10, 0, 0, 0, 0, 0, 1],
            'tic_tac_table': {'nod_1': 'x'},
            'game_render_form': 'game',
            'winner': 'Sergey'
        }

        for key, value in test_game_context.items():
            self.game_manager[key] = value

        self.game_manager.restart_game_with_same_players()
        result: Dict = self.game_manager["game_data"]
        self.assertEqual(expect_game_context, result, "The data in game_context didn\'t cleared")

    def test_type_response_from_player_for_game_manager(self):
        """
        game_manager attribute should be dict type case otherwise
        TypeError should be raisen
        """
        test_list: List = []
        test_string: str = ''
        test_int: int = 0
        test_tuple: Tuple = ()

        with self.assertRaises(TypeError):
            self.game_manager(test_list)
            self.game_manager(test_string)
            self.game_manager(test_int)
            self.game_manager(test_tuple)

    def test_checking_of_more_than_two_symbols_quantity_per_turn(self) -> None:
        """
        It checks if Player put 2 symbols instead of 1
        """
        test_value: Dict = {
            'sym_0': '', 'sym_1': 'x', 'sym_2': None,
            'sym_3': '', 'sym_4': '', 'sym_5': '0',
            'sym_6': '', 'sym_7': None, 'sym_8': ''
        }

        with self.assertRaises(ValueError):
            self.game_manager(test_value)

    def test_checking_of_empty_symbols_quantity_per_turn(self) -> None:
        """
        It checks if Player put a symbol, it's not possible to send empty cells during turn
        """
        test_value: Dict = {
            'sym_0': '', 'sym_1': '', 'sym_2': None,
            'sym_3': '', 'sym_4': '', 'sym_5': '',
            'sym_6': '', 'sym_7': None, 'sym_8': ''
        }

        with self.assertRaises(ValueError):
            self.game_manager(test_value)

    def test_field_completing_after_player_turn_zero(self) -> None:
        """
        It checks index to where should be added game_field value and value itself.
        In case if player turn is "x" value 1
        In case if player turn is "0" value 10
        """
        expect_res_zero: List = [0, 0, 0, 0, 0, 0, 0, 0, 10]

        test_value_zero: Dict = {
            'sym_0': '', 'sym_1': '', 'sym_2': None,
            'sym_3': '', 'sym_4': '', 'sym_5': '',
            'sym_6': '', 'sym_7': None, 'sym_8': '0'
        }

        self.game_manager(test_value_zero)
        result: List = self.game_manager["game_data"]['game_field']
        self.assertEqual(expect_res_zero, result, "Game_field was recorded with mistake")

    def test_field_completing_after_player_turn_cross(self) -> None:
        """
        It checks index to where should be added game_field value and value itself.
        In case if player turn is "x" value 1
        In case if player turn is "0" value 10
        """

        expect_res: List = [0, 0, 0, 0, 1, 0, 0, 0, 0]
        test_value: Dict = {
            'sym_0': '', 'sym_1': '', 'sym_2': None,
            'sym_3': '', 'sym_4': 'x', 'sym_5': '',
            'sym_6': '', 'sym_7': None, 'sym_8': ''
        }
        self.game_manager(test_value)
        result: List = self.game_manager["game_data"]['game_field']
        self.assertEqual(expect_res, result, "Game_field was recorded with mistake")

    def test_field_completing_if_player_response_more_than_nine_keys(self) -> None:
        """
        It checks if there will be response from player with dict more than 9 keys.
        In this case should be raised IndexError
        """

        test_value: Dict = {
            'sym_0': '', 'sym_1': '', 'sym_2': None,
            'sym_3': '', 'sym_4': 'x', 'sym_5': '',
            'sym_6': '', 'sym_7': None, 'sym_8': '', 'sym_9': ''
        }
        with self.assertRaises(IndexError):
            self.game_manager(test_value)

    def test_checking_of_symbol_value_from_player(self) -> None:
        """
        Duting the game player should use the only "x" or "0" per turn.
        In case of other symbol ValueError should be raised
        """
        test_value: Dict = {
            'sym_0': '', 'sym_1': 'd', 'sym_2': None,
            'sym_3': '', 'sym_4': '', 'sym_5': '',
            'sym_6': '', 'sym_7': None, 'sym_8': ''
        }

        with self.assertRaises(ValueError):
            self.game_manager(test_value)

    def test_calculation_for_winner_search(self) -> None:
        """
        # It simulates win situation 
        # """
        test_game_context: Dict = {
            'game_field': [0, 0, 1, 0, 0, 1, 0, 0, 0],
            'tic_tac_table': {
                'nod_0': '', 'nod_1': '', 'nod_2': '__x__',
                'nod_3': '', 'nod_4': '', 'nod_5': '__x__',
                'nod_6': '', 'nod_7': '', 'nod_8': ''
            },
            'game_render_form': 'game',
            'winner': ''
        }

        for key, value in test_game_context.items():
            self.game_manager[key] = value

        test_players_data: Dict = {
            'name_1': 'Player_1',
            'name_2': 'Player_2',
            'sym_1': '0',
            'sym_2': 'x',
            'score_1': 0,
            'score_2': 0
        }

        for key, value in test_players_data.items():
            self.game_manager[key]: Dict = value

        test_response: Dict = {
            'sym_0': '', 'sym_1': '', 'sym_2': None,
            'sym_3': '', 'sym_4': '', 'sym_5': None,
            'sym_6': '', 'sym_7': '', 'sym_8': 'x'
        }
        self.game_manager(test_response)

        expect_players_data: Dict = {
            'name_1': 'Player_1',
            'name_2': 'Player_2',
            'sym_1': '0',
            'sym_2': 'x',
            'score_1': 0,
            'score_2': 1
        }

        self.assertEqual(expect_players_data, self.game_manager["players_data"], "Incorrect game result")

    def test_checking_of_field_completing_after_win_situation(self) -> None:
        """
        It simulates win situation and checks that finaly all empty cells in tic_tac_field will be 
        completed by __finalize_field method
        """
        test_game_context: Dict = {
            'game_field': [0, 0, 1, 0, 0, 1, 0, 0, 0],
            'tic_tac_table': {
                'nod_0': '', 'nod_1': '', 'nod_2': '__x__',
                'nod_3': '', 'nod_4': '', 'nod_5': '__x__',
                'nod_6': '', 'nod_7': '', 'nod_8': ''
            },
            'game_render_form': 'game',
            'winner': ''
        }

        for key, value in test_game_context.items():
            self.game_manager[key] = value

        test_players_data: Dict = {
            'name_1': 'Player_1',
            'name_2': 'Player_2',
            'sym_1': '0',
            'sym_2': 'x',
            'score_1': 0,
            'score_2': 0
        }
        for key, value in test_players_data.items():
            self.game_manager[key]: Dict = value

        test_value: Dict = {
            'nod_0': '', 'nod_1': '', 'nod_2': None,
            'nod_3': '', 'nod_4': '', 'nod_5': None,
            'nod_6': '', 'nod_7': '', 'nod_8': 'x'
        }
        self.game_manager(test_value)

        expect_value: Dict = {
            'nod_0': '_____', 'nod_1': '_____', 'nod_2': '__x__',
            'nod_3': '_____', 'nod_4': '_____', 'nod_5': '__x__',
            'nod_6': '_____', 'nod_7': '_____', 'nod_8': '__x__'
        }

        self.assertDictEqual(
            expect_value, self.game_manager["game_data"]['tic_tac_table'], "Tic-tac_table completed incorrectly")

    def test_win_win_situation(self) -> None:
        """
        It simulates win-win situation 
        """
        test_game_context: Dict = {
            'game_field': [1, 10, 1,
                           1, 10, 1,
                           10, 1, 0],
            'tic_tac_table': {
                'sym_0': 'x', 'sym_1': '0', 'sym_2': 'x',
                'sym_3': 'x', 'sym_4': '0', 'sym_5': 'x',
                'sym_6': '0', 'sym_7': 'x', 'sym_8': ''},
            'game_render_form': 'game',
            'winner': ''
        }
        for key, value in test_game_context.items():
            self.game_manager[key] = value

        test_players_data: Dict = {
            'name_1': 'Player_1',
            'name_2': 'Player_2',
            'sym_1': '0',
            'sym_2': 'x',
            'score_1': 0,
            'score_2': 0
        }

        for key, value in test_players_data.items():
            self.game_manager[key] = value

        test_value: Dict = {
            'sym_0': None, 'sym_1': None, 'sym_2': None,
            'sym_3': None, 'sym_4': None, 'sym_5': None,
            'sym_6': None, 'sym_7': None, 'sym_8': '0'
        }
        self.game_manager(test_value)
        expect_players_data = {
            'name_1': 'Player_1',
            'name_2': 'Player_2',
            'sym_1': '0',
            'sym_2': 'x',
            'score_1': 1,
            'score_2': 1
        }

        self.assertEqual(
            expect_players_data, self.game_manager["players_data"],
            "Win-win situation works incorrect as incorrect game result")
        self.assertTrue(
            self.game_manager["game_data"]['winner'] != '',
            'Win-win situation works incorrect as there is no winner value')
