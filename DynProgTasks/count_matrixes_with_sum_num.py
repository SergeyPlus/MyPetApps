import random
from typing import List


def set_random_matrix(a: int, b: int) -> List[List[int]]:
    insert_list = [0] * (b + 1)
    random_matrix = [[0] + [random.randint(- 10 ** 3, 10 ** 3) for _ in range(b)] for _ in range(a + 1)]
    random_matrix[0] = insert_list

    print('Матрица')
    for line in random_matrix:
        print(line)
    return random_matrix

def count_matrix_sum_value(matrix: List[List[int]], number: int, a: int, b: int) -> int:
    insert_list = []
    F: List[List[List]] = [[insert_list] * (b + 1) for _ in range(a + 1)]
    for i in range(1, a + 1):
        for k in range(1, b + 1):
            F[i][k].append(matrix[i - 1][k - 1] + matrix[i - 1][k] + matrix[i][k - 1])




if __name__ == '__main__':
    a: int = int(input('Кол-во строк: '))
    b: int = int(input('Кол-во элементов: '))
    summ: int = int(input('Число: '))
    matrix = set_random_matrix(a, b)
    count_matrix_sum_value(matrix, summ, a, b)