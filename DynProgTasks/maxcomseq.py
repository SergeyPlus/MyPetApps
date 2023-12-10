import random
from typing import List


def set_sequence(number: int) -> List[int]:
    return [random.randint(0, 50) for _ in range(number)]


def find_max_common_subsequence(seq_1: List[int], seq_2: List[int]) -> int:
    F: List[List[int]] = [[0] * (len(seq_2) + 1) for _ in range(len(seq_1) + 1)]

    for i_line in range(1, len(seq_1) + 1):
        for i_elem in range(1, len(seq_2) + 1):
            if seq_1[i_line - 1] == seq_2[i_elem - 1]:
                F[i_line][i_elem] = 1 + F[i_line - 1][i_elem - 1]

            else:
                F[i_line][i_elem] = max(F[i_line - 1][i_elem], F[i_line][i_elem - 1])

    print(seq_1, seq_2, sep='\n')

    print()
    for i in F:
        print(i)

    return F[-1][-1]

if __name__ == '__main__':
    a = int(input('Последовательность А: '))
    b = int(input('Последовательность B: '))
    seq_A = set_sequence(a)
    seq_B = set_sequence(b)
    #seq_A = [2, 4, 9, 7, 3, 6, 12]
    #seq_B = [2, 3, 4, 12, 7, 8]
    print(f'Наибольшая общая подпоследовательность равна: '
          f'{find_max_common_subsequence(seq_A, seq_B)}')
