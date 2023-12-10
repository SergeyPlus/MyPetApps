from square import Matrix, print_matrix
from typing import List


def count_sequences(matrix: List, n: int, m: int):
    B: List[List] = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            if matrix[i][j] == 1:
                B[i + 1][j + 1] = B[i + 1][j] + 1




    return B


if __name__ == '__main__':
    n = int(input('Количество строк: '))
    m = int(input('Количество элементов в строке: '))
    matrix = Matrix(n, m)
    matrix_obj = matrix.create_matrix()


    print('Матрица дано:')
    print_matrix(matrix_obj)

    print('Матрица В:')
    print_matrix(count_sequences(matrix_obj, n, m))

