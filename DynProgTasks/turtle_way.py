import random
from square import print_matrix
from typing import List


def create_matrix(m, n) -> List[List]:
    matrix: List[List] = [[0] + [random.randint(0, 100) for _ in range(n)] for _ in range(m)]
    matrix.append([0] * (n + 1))
    return matrix


def count_turtle_way(matrix: List[List], m: int, n: int) -> None:

    for i_line in range(m - 1, -1, -1):
        for i_elem in range(1, n + 1):
            matrix[i_line][i_elem] += max(matrix[i_line][i_elem - 1], matrix[i_line + 1][i_elem])

    turtle_way: List[List] = [['-'] * (n + 1) for _ in range(m + 1)]
    i_line = 0
    i_elem = n

    turtle_way[i_line][i_elem] = 'F'
    while i_elem != 0 and i_line != m + 1:
        if matrix[i_line][i_elem - 1] >= matrix[i_line + 1][i_elem]:
            i_line = i_line
            i_elem = i_elem - 1
        elif matrix[i_line][i_elem - 1] <= matrix[i_line + 1][i_elem]:
            i_line = i_line + 1
            i_elem = i_elem
        turtle_way[i_line][i_elem] = '*'

    turtle_way[m - 1][1] = 'S'
    turtle_way = cut_matrix(turtle_way)

    print('\nДзен черепашки: ')
    print_matrix(turtle_way)


def cut_matrix(get_matrix: List[List]) -> List[List]:
    cut_matrix_list = [line[1: ] for line in get_matrix[: -1]]
    return cut_matrix_list


if __name__ == '__main__':
    m: int = int(input('Количество строк: '))
    n: int = int(input('Количество эл-в в строке: '))
    matrix = create_matrix(m, n)

    print(f'\nНайти путь с максимальной стоимостью из ячейкии строка {m + 1}, элемент {n + 1} в матрице: ')
    mat = matrix[:]
    mat = cut_matrix(mat)
    print_matrix(mat)

    count_turtle_way(matrix, m, n)