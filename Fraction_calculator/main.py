#!/usr/bin/env python3
from work_objects import Fraction, Action, WorkWithData
from typing import Callable
import re


def print_format_info() -> None:
    print("Формат для ввода дроби: \n"
          "- без целой части ХХ / ХХ \n"
          "- с целой частью ХХ (ХХ / XX), где ХХ любое целое число; \n"
          "Данный скрипт пока работает только для положительных дробей.")


def check_sign(data: str) -> None:
    if data not in '+-/*':
        raise ValueError


if __name__ == '__main__':
    print_format_info()
    dater: WorkWithData = WorkWithData()
    while True:
        try:
            fraction_1 = input('Введите дробь №1: ')
            fraction_1: str = dater(fraction_1)
            fraction_2 = input('Введите дробь №2: ')
            fraction_2: str = dater(fraction_2)
            sign = input('Знак: ')
            check_sign(sign)
        except ValueError:
            print('Введены некорректные данные. Пвторите ввод.')
            continue

        print("Дробное выражение: ({}) {} ({})".format(
            fraction_1, sign, fraction_2
        ))

        fr_object_1: Fraction = Fraction(fraction_1)
        fr_object_2: Fraction = Fraction(fraction_2)

        action_object: Callable = Action(sign).get_sign_type()
        result_instance = action_object(fr_object_1, fr_object_2)

        next_step: str = input('Продолжить? (да \ нет):  ')
        if next_step == 'да':
            result_instance.clear_screen()
            continue
        break
