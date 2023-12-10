import logging
import random
from typing import List, Tuple

logging.basicConfig(level=30)
sort_logger = logging.getLogger('log1')

search_logger = logging.getLogger('search')
search_logger.setLevel(10)

ch = logging.StreamHandler()
ch.setLevel(10)
search_logger.addHandler(ch)


def create_sequence(qty: int) -> List[int]:
    seq_list = [random.randint(-10 ** 3, 10 **3) for _ in range(qty)]
    return seq_list


def bubble_sort(lst: List[int]) -> List[int]:

    for i in range(len(lst)):
        for k in range(1, len(lst)):
            if lst[k - 1] > lst[k]:
                lst[k -1], lst[k] = lst[k], lst[k - 1]

    return lst


def merge_sort(lst: List[int]) -> List[int]:
    sort_logger.info(f'Starting merge sorting - {lst}')

    def merge_fun(lst1: List[int], lst2: List[int]) -> List[int]:
        sort_logger.info(f'Starting mergering list1 - {lst1} / list2 - {lst2}')
        merged_list = []
        lst1_index = 0
        lst2_index = 0

        while lst2_index < len(lst2) and lst1_index < len(lst1):
            if lst1[lst1_index] < lst2[lst2_index]:
                merged_list.append(lst1[lst1_index])
                lst1_index += 1
            else:
                merged_list.append(lst2[lst2_index])
                lst2_index += 1

        merged_list += lst1[lst1_index: ] + lst2[lst2_index: ]
        sort_logger.info(f'Get mergering result - {merged_list}')
        return merged_list

    def sorting(lst: List[int]):
        sort_logger.info(f'Starting recursion sorting - {lst}')

        mid_index = len(lst) // 2
        left_list = lst[: mid_index]
        right_list = lst[mid_index:]

        sort_logger.info(f'Got lef_list - {left_list} and right_lisy {right_list}')
        if len(left_list) > 1:
            sort_logger.info(f'Condition len(left_list) > 1')
            left_list = sorting(left_list)
            sort_logger.info(f'Received left_list {left_list}')
        if len(right_list) > 1:
            sort_logger.info(f'Condition len(right_list) > 1')
            right_list = sorting(right_list)
            sort_logger.info(f'Received right_list {right_list}')

        res_list = merge_fun(left_list, right_list)
        sort_logger.info(f'Got result after mergering {res_list}')
        return res_list

    sorted_list = sorting(lst)
    return sorted_list


def binary_search(lst: List[int]):

    search_logger.info('Start binary searching')
    left_bound = 0
    right_bound = len(lst)

    while right_bound - left_bound > 2:
        middle = (left_bound + right_bound) // 2
        search_logger.info(f'Middle boundary is {middle}')

        if key_num > lst[middle]:
            search_logger.info(f'Worked the rule {key_num} > {lst[middle]}')
            left_bound = middle

        elif key_num < lst[middle]:
            search_logger.info(f'Worked the rule {key_num} < {lst[middle]}')
            right_bound = middle

    if lst[right_bound - 1] == key_num:
        return right_bound - 1, left_bound, right_bound
    return None, left_bound, right_bound


if __name__ == '__main__':
    n: int = int(input('Количество эл-в последовательности: '))
    seq_list = create_sequence(n)
    print(f'Дана последовательность {seq_list}')
    key_num: int = int(input('Искать индекс числа: '))

    sort_choice = int(input('Выбери сортировку (1 - пузырем. 2 - слиянием): '))
    sorted_seq_list = []
    if sort_choice == 1:
        sorted_seq_list = bubble_sort(seq_list)
    if sort_choice == 2:
        sorted_seq_list = merge_sort(seq_list)

    print(f'Отсортированный список: {sorted_seq_list}\n')

    result_ind, left_bound, right_bound = binary_search(sorted_seq_list)
    if result_ind:
        print(f'Индекс числа {key_num} находится под индексом {result_ind}')
    else:
        print(f'В заданной последовательности: {sorted_seq_list} числа {key_num} нет.\n'
              f'Число {key_num} находится в диапазоне индексов {left_bound} - {right_bound}')