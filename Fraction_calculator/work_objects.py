from typing import Dict, Tuple, List
import logging
import subprocess

logging.basicConfig(level=10, filemode='a', filename='log.txt')
wo_logger = logging.getLogger()


class Fraction:
    def __init__(self, data: str):
        wo_logger.info(f"Initialization of data for Fraction instance {data.split(' ')}")
        self.numerator: int = int(data.split(' ')[0])
        self.denominator: int = int(data.split(' ')[-1])

    def __getitem__(self, item):
        return self.__dict__[item]


class Mixin:
    def gcd(self, data: Tuple) -> int:
        wo_logger.info(f"Starting to find common divider")
        a: int = data[0]
        b: int = data[-1]
        if a % b == 0:
            wo_logger.info(f"Commom divider founded - {b}")
            return b
        updated_data: Tuple = b, a % b
        result: int = self.gcd(updated_data)
        if result:
            return result

    def get_whole_part(self, data: Tuple) -> Tuple:
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

    def simple_fraction(self, data: Tuple) -> Tuple:
        wo_logger.info(f'Fraction simplifying. in the beginning {data}')
        fr_data: Tuple = self.get_whole_part(data)
        common_divider: int = self.gcd(fr_data)
        fr_data_list: List = list(fr_data)
        fr_data_list[-1]: int = int(fr_data_list[-1] / common_divider)
        fr_data_list[-2]: int = int(fr_data_list[-2] / common_divider)
        fr_data: Tuple = tuple(fr_data_list)
        wo_logger.info(f'Final result {fr_data}')
        return fr_data

    def print_fraction(self, data: Tuple) -> None:
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

    def __call__(self, fr_object_1, fr_object_2):
        wo_logger.info(f'This is __call__ from class {self}')
        self.fr_object_1: Fraction = fr_object_1
        self.fr_object_2: Fraction = fr_object_2
        return self

    def make_action(self) -> None:
        wo_logger.info('Making action - summ')

        numerator: int = (self.fr_object_1['numerator'] * self.fr_object_2['denominator'] +
                          self.fr_object_2['numerator'] * self.fr_object_1['denominator'])

        denominator: int = (self.fr_object_1['denominator'] * self.fr_object_2['denominator'])
        wo_logger.info(f"Numerator - {numerator}, denominator - {denominator}")

        fr_data: Tuple = numerator, denominator
        fr_data: Tuple = self.simple_fraction(fr_data)
        self.print_fraction(fr_data)



class Difference(Summ):

    def make_action(self) -> None:
        wo_logger.info('Making action - difference')
        numerator: int = (self.fr_object_1['numerator'] * self.fr_object_2['denominator'] -
                          self.fr_object_2['numerator'] * self.fr_object_1['denominator'])

        denominator: int = (self.fr_object_1['denominator'] * self.fr_object_2['denominator'])
        wo_logger.info(f"Numerator - {numerator}, denominator - {denominator}")
        fr_data: Tuple = numerator, denominator
        fr_data: Tuple = self.simple_fraction(fr_data)
        self.print_fraction(fr_data)


class Multiple(Summ):
    def make_action(self) -> None:
        wo_logger.info('Making action - multiplication')
        numerator: int = self.fr_object_1['numerator'] * self.fr_object_2['numerator']

        denominator: int = self.fr_object_1['denominator'] * self.fr_object_2['denominator']
        wo_logger.info(f"Numerator - {numerator}, denominator - {denominator}")
        fr_data: Tuple = numerator, denominator
        fr_data: Tuple = self.simple_fraction(fr_data)
        self.print_fraction(fr_data)


class Divide(Summ):

    def make_action(self) -> None:
        wo_logger.info('Making action - divide')
        numerator: int = self.fr_object_1['numerator'] * self.fr_object_2['denominator']

        denominator: int = self.fr_object_1['denominator'] * self.fr_object_2['numerator']
        wo_logger.info(f"Numerator - {numerator}, denominator - {denominator}")
        fr_data: Tuple = numerator, denominator
        fr_data: Tuple = self.simple_fraction(fr_data)
        self.print_fraction(fr_data)


class Sign:
    _fraction_actions: Dict = {
        '+': Summ,
        '-': Difference,
        '*': Multiple,
        '/': Divide
    }

    def __init__(self, sign: str):
        wo_logger.info(f"Sign __init__, symbol: {sign}")
        self.sign_type: str = sign

    def get_sign_type(self):
        result = self._fraction_actions[self.sign_type]
        action_object = result()
        wo_logger.info(f"Parent class {action_object.__class__}")
        return action_object


if __name__ == '__main__':
    ...