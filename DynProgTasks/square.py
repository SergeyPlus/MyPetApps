import random
from typing import List


class Matrix:
    matrix_sched = []

    def __init__(self, m: int, n: int):
        self._m = m # Quantity of lines in matrix
        self._n = n # Quantity of elements in each line

    def create_matrix(self):
        for _ in range(self._m):
            insert_list = [random.choice([0, 1]) for _ in range(self._n)]
            self.matrix_sched.append(insert_list)
        return self.matrix_sched


def count_tables(matrix: List[List], m: int, n: int):
    B = [[0] * (n + 1) for _ in range(m + 1)]
    result_dict = {}
    for i in range(1, m + 1): #  lines
        for k in range(1, n + 1): # elements q-ty
            if matrix[i - 1][k - 1] == 1:
                B[i][k] = min(B[i][k - 1], B[i - 1][k], B[i - 1][k - 1]) + 1

            if B[i][k] > 1:
                result_dict[i - (B[i][k] - 1), k - (B[i][k] - 1)] = B[i][k]

    return result_dict


def print_matrix(value):
    for elem in value:
        print(elem)


if __name__ == '__main__':
    m = int(input('Количество строк: '))
    n = int(input(('Количество элементов строки: ')))
    matrix = Matrix(m, n)
    matrix_obj = matrix.create_matrix()
    res = count_tables(matrix_obj, m, n)

    print('\nМатрица: ')
    print_matrix(matrix_obj)

    print(f'\nВ матрице можно найти {len(res)} квадратов.')
    if res:
        number = 1
        for key, value in res.items():
            print('Квадрат №{number}: \n'
                  '     размер: {size} ячеек; координаты: строка-{cord_line} / элемент-{size_number};\n'.format(
                    number=number,
                    size=value ** 2,
                    cord_line=key[0],
                    size_number=key[1]
        ))
            number += 1
