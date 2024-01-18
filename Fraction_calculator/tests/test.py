import unittest
import main
import work_objects
from typing import List


class MainTest(unittest.TestCase):

    def setUp(self) -> None:
        self.file_main = main
        self.file_work_object = work_objects

        self.object = work_objects.WorkWithData()
        self.action_object = work_objects.Action

    def test_checking_input_format(self):
        test_scenarios: List = [
            '2.5 / 3', '22/ 349', '22 /349', '222(22586 / 333339)',
            '222 (22586/ 333339)', '222(22586/333339)', '578 (2 / -3)',
            '578 (-2 / -3)', '578 2 / -3)', '578 (2 / -3', 'a (2 / -3)',
            '-58 (3 / 4)'
        ]
        for scenario in test_scenarios:
            with self.assertRaises(ValueError):
                self.object(scenario)

    def test_getting_updating_format(self):
        test_scenarios: List = [
            '1 (2 / 5)', '3 / 4', '178 (345 / 679)'
        ]
        expected_results: List = [
            '7 / 5', '3 / 4', '121207 / 679'
        ]

        for i in range(len(test_scenarios)):
            result: str = self.object(test_scenarios[i])
            self.assertTrue(result == expected_results[i], "Функция не корректно обрабатывает данные")

    def test_checking_sign(self):
        test_scenarios: List = [' *', 'q', ', ', 'plus', '^']
        for scenario in test_scenarios:
            with self.assertRaises(ValueError):
                self.file_main.check_sign(scenario)

    def test_action_class_can_return_correct_object(self):
        test_sign: List = ['*', '+', '-', '/']
        expected_classes: List = [self.file_work_object.Multiple, self.file_work_object.Summ,
                                  self.file_work_object.Difference, self.file_work_object.Divide]

        for i in range(len(test_sign)):
            result_object = self.action_object(test_sign[i]).get_sign_type()
            self.assertTrue(isinstance(result_object, expected_classes[i]), 'class Action возвращает некорректный объект')

