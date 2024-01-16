#!/usr/bin/env python3
from work_objects import Fraction, Sign
from typing import Tuple


if __name__ == '__main__':

    while True:
        fraction_1 = input('Введите дробь №1: ')
        fraction_2 = input('Введите дробь №2: ')
        sign = input('Знак: ')

        fr_object_1: Fraction = Fraction(fraction_1)
        fr_object_2: Fraction = Fraction(fraction_2)

        action_object = Sign(sign).get_sign_type()
        result = action_object(fr_object_1, fr_object_2)

        print(result.make_action())

        next_step: str = input('Продолжить? (да \ нет):  ')
        if next_step == 'да':
            continue
        break
