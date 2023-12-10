import unittest
from app import app
from datetime import datetime
import re


class TestApplication(unittest.TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()
        self.base_url = '/find_price/'

    def test_can_receive_error_message(self) -> None:
        """The test allows to check possibility of server to generate errors in case of incorrect dates.
        If test passed it means that server processed incorrect dates and returned to User proper message"""
        # scenarios with mistakes
        scenario = 'date=15012023&date=17.01.2023'
        #scenario = 'date=Hello_world&date=17.01.2023'
        #scenario = 'date=17.01.2023'
        #scenario = 'date=28.01.2023&date=17.01.2023'
        #scenario = 'date=15/01/2023&date=17.01.2023'

        #day = datetime.now().day
        #month = str(datetime.now().month)
        #year = str(datetime.now().year)
        # scenario = "date=datetime.strptime('{}.{}.{}'.format(str(day + 3), month, year), '%d.%m.%Y')&" + \
        #            "date=datetime.strptime('{}.{}.{}'.format(str(day + 10), month, year), '%d.%m.%Y')"

        resp = self.app.get(self.base_url + '?{}'.format(scenario)).data.decode()
        self.assertTrue('Ошибка' in resp, 'Что-то пошло не так')

    def test_can_receive_price_data(self) -> None:
        """
        The test checks that server returns correct price data
        :return:
        """
        scenario = '?date=14.01.2023&date=15.01.2023'
        resp = self.app.get(self.base_url + scenario).data.decode()
        expected_answer = "4 089,96"
        self.assertTrue(re.findall(expected_answer, resp), 'Что-то пошло не так')

    def test_can_receive_empty_message(self) -> None:
        """ The test checks that if there is no price on metalls for specified date and in this case server returns
        appropriate message"""
        scenario = '?date=15.01.2023&date=15.01.2023'
        resp = self.app.get(self.base_url + scenario).data.decode()
        expected_answer = "Измените диапазон"
        self.assertTrue(expected_answer in resp, 'Что-то пошло не так')


if __name__ == "__main__":
    unittest.main()