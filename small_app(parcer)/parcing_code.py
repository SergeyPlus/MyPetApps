import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from time import sleep

headers = {'User': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0'}


def get_dict_with_data(date_start, date_end) -> str:
    """The function make parcing of CB web-site and searches prices on metalls
    based on requested date period
    """
    sleep(3)
    url: str = 'https://www.cbr.ru/hd_base/metall/metall_base_new/?UniDbQuery.Posted=True&UniDbQuery.' \
          'From={0}&UniDbQuery.To={1}&UniDbQuery.Gold=true&UniDbQuery.Silver=true&UniDbQuery.' \
          'Platinum=true&UniDbQuery.Palladium=true&UniDbQuery.so=1'.format(date_start, date_end)

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    data_metals_list = soup.find_all("th", class_="right")
    metals_names_list: List[str] = [str(metal_name)[18:-5] for metal_name in data_metals_list]

    data_dates_list = soup.find_all('td', class_="")
    dates_list: List[str] = [str(date)[4: -5] for date in data_dates_list]

    data_prices_list = soup.find_all('td', class_="right")
    prices_list: List[str] = [str(price)[18: -7] for price in data_prices_list]

    total_dict: Dict[str, Dict[str, str]] = {}
    # example: {'25.01.2023': {'золото': '00', 'серебро': '00','платина': '00', 'палладий': '00'}
    day_dict: Dict[str, str] = {}

    price_index = 0
    for count in range(len(dates_list)):
        for i in range(len(metals_names_list)):
            day_dict[metals_names_list[i].lower()] = prices_list[price_index]
            price_index += 1

        total_dict[dates_list[count]] = day_dict
        day_dict = {}

    result = ['Дата: {} - Цена: {}<br>'.format(key, value) for key, value in total_dict.items()]

    return ''.join(result)


if __name__ == "__main__":
    get_dict_with_data(date_start=None, date_end=None)
