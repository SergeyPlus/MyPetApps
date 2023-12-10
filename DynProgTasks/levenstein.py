
def hello_levenstein(seq_1, seq_2):
    F = [[(i + k) if i * k == 0 else 0 for i in range(len(seq_1) + 1)] for k in range(len(seq_2) + 1)]

    for i in range(len(seq_2)):
        for k in range(len(seq_1)):
            if seq_2[i] == seq_1[k]:
                F[i + 1][k + 1] = F[i][k]
            else:
                F[i + 1][k + 1] = 1 + min(F[i][k + 1], F[i + 1][k])
    # for elem in F:
    #     print(elem)

    return F[-1][-1]


if __name__ == '__main__':
    word_1: str = input('Слово 1: ')
    word_2: str = input('Слово 2: ')

    min_quant_of_edit: int = hello_levenstein(word_1, word_2)

    print(f'Минимальное количество изменений: {min_quant_of_edit}')