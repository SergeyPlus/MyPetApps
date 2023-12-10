import random
from typing import List, Dict


class Cell:
    '''It's a simple class for cell which contents of
    - cel_number (will be passed during Board instance identifying)
    - cell_status will show which symbol pass to the cell
    - cell_value is necessary during winner checking
    '''
    cell_status = '_'
    cell_value = 0

    def __init__(self, number) -> None:
        self.cell_number = number


class Board:
    """The class identifies board list list and allow to work with cell instances"""
    board_list: List = []  # list of cells instance
    summ: int = 0

    @classmethod
    def __init__(cls, cell) -> None:
        """ The method creates list of cells - board list"""
        cls.board_list.append(cell)

    @classmethod
    def print_board(cls) -> None:
        """The method reflects board scheme"""
        print('***********ДОСКА************')
        for i in range(0, 9, 3):
            print('ячейка {}  ячейка {}  ячейка {}'.format(
                i + 1, i + 2, i + 3
            ))
            print('   {}         {}        {}'.format(
                cls.board_list[i].cell_status,
                cls.board_list[i + 1].cell_status,
                cls.board_list[i + 2].cell_status
            ))
        print('****************************')
        print()

    @classmethod
    def reflect_turn(cls, index, player_value) -> None:
        """
        The method reflects data (player_value) in particula Cell instance of Board list
        :param index:
        :param player_value:
        :return:
        """
        cls.board_list[index].cell_value = player_value

    @classmethod
    def check_winner(cls) -> int:
        """ The method checks a winner"""
        # it checks cells (1, 4, 7), (2, 5, 8), (3, 6, 9)
        for k in range(1, 4):
            for number in range(k, k + 7, 3):
                cls.summ += cls.board_list[number - 1].cell_value
            if cls.summ == 3 or cls.summ == 30:
                return cls.summ
            cls.summ = 0

        # it checks cells (1, 2, 3), (4, 5, 6), (7, 8, 9)
        for k in range(1, 8, 3):
            for number in range(k, k + 3):
                cls.summ += cls.board_list[number - 1].cell_value
            if cls.summ == 3 or cls.summ == 30:
                return cls.summ
            cls.summ = 0

        # it checks cells (1, 5, 9)
        cls.summ = sum([cls.board_list[number - 1].cell_value for number in range(1, 10, 4)])
        if cls.summ == 3 or cls.summ == 30:
            return cls.summ
        cls.summ = 0

        # it checks cells (3, 5, 7)
        cls.summ = sum([cls.board_list[number - 1].cell_value for number in range(3, 8, 2)])
        if cls.summ == 3 or cls.summ == 30:
            return cls.summ
        cls.summ = 0


class Players:
    """  The class initiate simple player profile. It contents:
     - player_choice - could be 'x' or '0'
     - player_turn - it's the dict wher key - player_choice and value - it's a weight of score (weight is necessary
     to calculate winner)
     - players_list - the list of Players instance"""
    player_turn: Dict[str, int] = {'x': 1, '0': 10}
    player_choice_sym: str = " "  # could be 'x' or '0'
    players_list: List = []

    def __init__(self) -> None:
        """
        Initialization of player instance. Player instance content name and player_choice_sym (symbol which is used
        by player for the game.
        Empty name is not possible)
        """
        while True:
            player_name: str = input('Укажите имя: ')
            if not player_name:
                print('Пустое имя недопустимо. Повторите ввод заново')
            else:
                self.player_name = player_name
                break
        self.players_list.append(self)

    def complete_players_profile(self) -> str:
        """ Method helps to User to make choice of symbol which is used for the game by User
        it's not possible to use any other symbol (even empty) instead of 'х' или '0' """
        print(f'{self.player_name} выбирает символ: "х" или "0"')
        while True:
            choice_sym: str = input(f'Итак, {self.player_name}, ваш выбор: ')
            if choice_sym == 'x' or choice_sym == '0':
                self.player_choice_sym = choice_sym
                return choice_sym
            print('Введено некорректное значение. Повторите ввод x или 0.')

    def take_turn(self, board_list):
        """ The method input from Player number of cell to where place symbol. If cell number is not integer
         from 1 till 9 it raised BaseException.
         If cell already boked by symbol 'x' or '0' it will be info that it's necessary to make another turn and
          choose empty cell

          Finally method return index of cell which Player choosed and int value"""
        print(f'Ход игрока: {self.player_name}')
        while True:
            try:
                index_field: int = int(input(f'Укажите номер ячейки для хода Игрока: {self.player_name} - '))
                if not 1 <= index_field <= 9:
                    raise BaseException

                if board_list[index_field - 1].cell_status == '_':
                    board_list[index_field - 1].cell_status = self.player_choice_sym
                    return index_field - 1, self.player_turn[self.player_choice_sym]
                print('Ячейка занята. Сделайте выбор свободной ячейки')

            except BaseException:
                print('Введено некорректное значение. Для выбора ячейки используйте номера от 1 до 9')


class Game:
    """ The class identifies sequence of game"""
    game_line_list: List = []

    @classmethod
    def play_game(cls, player) -> bool:
        """ The method recieve instance of Player. It means that this Player ahs to take turn. It calls appropriate
        method. The result of the turn reflects in the board and finally cheking of winner happens"""
        Board.print_board()
        index, player_value = player.take_turn(Board.board_list)
        Board.reflect_turn(index, player_value)
        result = Board.check_winner()
        if result == 3 or result == 30:
            print(f'***{player.player_name} - ПОБЕДИТЕЛЬ!!!***\n'
                  f'     Прими наши поздравления!')
            return True

    @classmethod
    def identify_game_seq_list(cls, index_player) -> List[int]:
        """ The method identifies sequence of turns which will be made by Players for the game
        of 1st player start the game the sequnse will be [0, 1, 0, .. n] if 2nd [1, 0, 1, 0, .. n]"""
        return [0 if n % 2 == 0 else 1 for n in range(9)] if index_player == 0 \
            else [1 if n % 2 == 0 else 0 for n in range(9)]


def complete_profile_players() -> None:
    """ The function randomly identifies Player and call method complete_players_profile for appropriate Player
    and finally it pass symbol for the rest Player.
    It happens automatically
    """
    print('Кинем монетку кто будет выбирать за кого играть: за х-ки или 0-ки')
    random_index: int = random.randint(0, 1)
    choice: str = Players.players_list[random_index].complete_players_profile()

    for key in Players.player_turn.keys():
        if key != choice:
            Players.players_list[1 - random_index].player_choice_sym = key
            print(f'{Players.players_list[1 - random_index].player_name}, вы играете "{key}"-ми\n')
            break


def clarify_first_turn() -> List[int]:
    """ it identifies whose turn first and return sequnce of game turns"""
    print('Кинем монетку кто ходит первым.')
    random_index_player: int = random.randint(0, 1)
    print(f'Первым ходит {Players.players_list[random_index_player].player_name}')
    return Game.identify_game_seq_list(random_index_player)


print('**********УЧАСТНИКИ**********')
print('Игрок 1', end=': ')
player_1 = Players()
print('Игрок 2', end=': ')
player_2 = Players()
print('*****************************\n')

complete_profile_players()
game_list: List[int] = clarify_first_turn()

# create Board which contents of instances of Cell. For each Cell instance passing number which further will reflect
# number of cells in the game
for number in range(1, 10):
    cell = Cell(number)
    Board(cell)

# gaming is here. Each Player turn based on list sequence.
for index in game_list:
    if Game.play_game(Players.players_list[index]):
        Board.print_board()
        break
else:
    print(f'{player_1.player_name}, {player_2.player_name}, победила - ДРУЖБА!!!')
