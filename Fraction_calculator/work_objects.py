from typing import Dict, Tuple, List, Callable
import logging
import subprocess
import re

formatt: str = "%(asctime)s : %(filename)s : %(funcName)s : %(lineno)s : %(message)s"
logging.basicConfig(level=10, format=formatt, filename='frac_log.log', filemode='a')
wo_logger = logging.getLogger()


class Fraction:
    def __init__(self, data: str):
        wo_logger.info(f"Initialization of data for Fraction instance {data.split(' ')}")
        self.numerator: int = int(data.split(' ')[0])
        self.denominator: int = int(data.split(' ')[-1])

    def __getitem__(self, item):
        return self.__dict__[item]


class Mixin:
    def _gcd(self, data: Tuple) -> int:
        wo_logger.info(f"Starting to find common divider")
        a: int = data[-2]
        b: int = data[-1]
        wo_logger.info(f"a = {a}, b = {b}")
        if a % b == 0:
            wo_logger.info(f"As {a} % {b} = {a % b} (Result should be 0). Commom divider founded - {b}")
            return b
        updated_data: Tuple = b, a % b
        wo_logger.info(f"Upgrade_data {updated_data}")
        result: int = self._gcd(updated_data)
        wo_logger.info(f"Returned result is  {result}")
        if result:
            return result

    def _get_whole_part(self, data: Tuple) -> Tuple:
        wo_logger.info(f"Getting whole part in fraction")
        a: int = data[0]
        b: int = data[-1]

        if a > b:
            c: int = a // b
            a: int = a - c * b
            wo_logger.info(f"There is a whole part, is {c}")
            return c, a, b
        wo_logger.info(f"There is no a whole part")
        return a, b

    def _simple_fraction(self, data: Tuple) -> Tuple:
        wo_logger.info(f'Fraction simplifying. in the beginning {data}')
        fr_data: Tuple = self._get_whole_part(data)
        common_divider: int = self._gcd(fr_data)
        fr_data_list: List = list(fr_data)
        fr_data_list[-1]: int = int(fr_data_list[-1] / common_divider)
        fr_data_list[-2]: int = int(fr_data_list[-2] / common_divider)
        fr_data: Tuple = tuple(fr_data_list)
        wo_logger.info(f'Final result {fr_data}')
        return fr_data

    def _print_fraction(self, data: Tuple) -> None:
        wo_logger.info(f"Printing info. Final data is {data}")
        if data[-2] == 0:
            data: List = list(data)
            data: List = data[: -2]
        answer: str = ''

        if not data:
            answer: str = '0'

        elif len(data) == 1:
            answer: str = f"{data[0]}"

        elif len(data) == 2:
            answer: str = "{numerator} / {denominator}".format(
                numerator=data[0],
                denominator=data[-1]
            )

        elif len(data) == 3:
            answer: str = "{whole_part} ({numerator} /  {denominator})".format(
                whole_part=data[0],
                numerator=data[1],
                denominator=data[-1]
            )

        row: str = "=" * 20
        print("{} \nОтвет: {} \n{}".format(
            row,
            answer,
            row
        ))

    def clear_screen(self) -> None:
        command: List = ["clear"]
        subprocess.run(command)


class Summ(Mixin):

    def __call__(self, fr_object_1: Fraction, fr_object_2: Fraction) -> None:
        wo_logger.info(f'This is __call__ from class {self}')
        self.fr_object_1: Fraction = fr_object_1
        self.fr_object_2: Fraction = fr_object_2
        self._make_action()

    def _make_action(self) -> None:
        wo_logger.info('Making action - summ')

        numerator: int = (self.fr_object_1['numerator'] * self.fr_object_2['denominator'] +
                          self.fr_object_2['numerator'] * self.fr_object_1['denominator'])

        denominator: int = (self.fr_object_1['denominator'] * self.fr_object_2['denominator'])
        wo_logger.info(f"Numerator - {numerator}, denominator - {denominator}")

        fr_data: Tuple = numerator, denominator
        fr_data: Tuple = self._simple_fraction(fr_data)
        self._print_fraction(fr_data)


class Difference(Summ):

    def make_action(self) -> None:
        wo_logger.info('Making action - difference')
        numerator: int = (self.fr_object_1['numerator'] * self.fr_object_2['denominator'] -
                          self.fr_object_2['numerator'] * self.fr_object_1['denominator'])

        denominator: int = (self.fr_object_1['denominator'] * self.fr_object_2['denominator'])
        wo_logger.info(f"Numerator - {numerator}, denominator - {denominator}")
        fr_data: Tuple = numerator, denominator
        fr_data: Tuple = self._simple_fraction(fr_data)
        self._print_fraction(fr_data)


class Multiple(Summ):
    def make_action(self) -> None:
        wo_logger.info('Making action - multiplication')
        numerator: int = self.fr_object_1['numerator'] * self.fr_object_2['numerator']

        denominator: int = self.fr_object_1['denominator'] * self.fr_object_2['denominator']
        wo_logger.info(f"Numerator - {numerator}, denominator - {denominator}")
        fr_data: Tuple = numerator, denominator
        fr_data: Tuple = self._simple_fraction(fr_data)
        self._print_fraction(fr_data)


class Divide(Summ):

    def make_action(self) -> None:
        wo_logger.info('Making action - divide')
        numerator: int = self.fr_object_1['numerator'] * self.fr_object_2['denominator']

        denominator: int = self.fr_object_1['denominator'] * self.fr_object_2['numerator']
        wo_logger.info(f"Numerator - {numerator}, denominator - {denominator}")
        fr_data: Tuple = numerator, denominator
        fr_data: Tuple = self._simple_fraction(fr_data)
        self._print_fraction(fr_data)


class Action:
    _fraction_actions: Dict = {
        '+': Summ,
        '-': Difference,
        '*': Multiple,
        '/': Divide
    }

    def __init__(self, sign: str):
        wo_logger.info(f"{self.__class__} initializing symbol: {sign}")
        self.sign_type: str = sign

    def get_sign_type(self) -> Callable:
        action_class: Callable = self._fraction_actions[self.sign_type]
        action_instance: Callable = action_class()
        wo_logger.info(f"Parent class {action_instance.__class__}")
        return action_instance


class WorkWithData:

    def __call__(self, data) -> str:
        wo_logger.info(f"Calling instance of class {self.__class__}, with data {data}")
        self.data: str = data
        self._check_format()
        new_data: str = self._upgrade_format()
        return new_data

    def _check_format(self) -> None:
        wo_logger.info(f"Checking format of data {self.data}")
        pattern_wo_whole_part = r'^\d{1,} / \d{1,}'
        pattern_with_whole_part = r'^\d{1,} \(\d{1,} / \d{1,}\)'
        counter: int = 0
        for pattern in pattern_wo_whole_part, pattern_with_whole_part:
            if not re.findall(pattern, self.data):
                counter += 1
        wo_logger.info(f"Counter = {counter}")
        if counter == 2:
            wo_logger.info(f"Not correct data")
            raise ValueError
        wo_logger.info(f"Correct data")

    def _upgrade_format(self) -> str:
        wo_logger.info(f"Upgrading format data if needed. Data {self.data}")
        new_data: str = self.data
        if len(self.data.split(' ')) == 4:
            wo_logger.info(f"Upgrading is needed.")
            denominator: str = self.data.split(' ')[-1].strip(')')
            wo_logger.info(f"Denominator is {denominator}, type is {type(denominator)}")
            numerator: int = int(self.data.split(' ')[1].strip('(')) + int(denominator) * int(self.data.split(' ')[0])
            wo_logger.info(f"Numerator is {numerator}, type is {type(numerator)}")
            new_data: str = "{} / {}".format(numerator, denominator)
        wo_logger.info(f"Returned data is {new_data},  type {type(new_data)}")
        return new_data


if __name__ == '__main__':
    ...