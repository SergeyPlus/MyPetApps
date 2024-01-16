from typing import Dict, Tuple
import logging

logging.basicConfig(level=10)
wo_logger = logging.getLogger()


class Fraction:
    def __init__(self, data: str):
        wo_logger.info(data.split(' '))
        self.numerator: int = int(data.split(' ')[0])
        self.denominator: int = int(data.split(' ')[-1])

    def __getitem__(self, item):
        return self.__dict__[item]


class EvklidMixin:
    ...


class Summ:

    def __call__(self, fr_object_1, fr_object_2):
        wo_logger.info(f'This is __call__ from class {self}')
        self.fr_object_1: Fraction = fr_object_1
        self.fr_object_2: Fraction = fr_object_2
        return self

    def make_action(self) -> Tuple:
        wo_logger.info('Making action - summ')

        numerator: int = (self.fr_object_1['numerator'] * self.fr_object_2['denominator'] +
                          self.fr_object_2['numerator'] * self.fr_object_1['denominator'])

        denominator: int = (self.fr_object_1['denominator'] * self.fr_object_2['denominator'])

        wo_logger.info(f"Numerator - {numerator}, denominator - {denominator}")
        return numerator, denominator


class Difference(Summ):

    def make_action(self) -> Tuple:
        wo_logger.info('Making action - difference')
        numerator: int = (self.fr_object_1['numerator'] * self.fr_object_2['denominator'] -
                          self.fr_object_2['numerator'] * self.fr_object_1['denominator'])

        denominator: int = (self.fr_object_1['denominator'] * self.fr_object_2['denominator'])
        wo_logger.info(f"Numerator - {numerator}, denominator - {denominator}")
        return numerator, denominator


class Multiple(Summ):
    def make_action(self) -> Tuple:
        wo_logger.info('Making action - multiplication')
        numerator: int = self.fr_object_1['numerator'] * self.fr_object_2['numerator']

        denominator: int = self.fr_object_1['denominator'] * self.fr_object_2['denominator']
        wo_logger.info(f"Numerator - {numerator}, denominator - {denominator}")
        return numerator, denominator


class Divide(Summ):

    def make_action(self) -> Tuple:
        wo_logger.info('Making action - divide')
        numerator: int = self.fr_object_1['numerator'] * self.fr_object_2['denominator']

        denominator: int = self.fr_object_1['denominator'] * self.fr_object_2['numerator']
        wo_logger.info(f"Numerator - {numerator}, denominator - {denominator}")
        return numerator, denominator


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