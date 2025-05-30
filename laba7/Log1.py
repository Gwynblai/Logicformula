import random

def create_random_matrix(size=16):
    return [[random.randint(0, 1) for _ in range(size)] for _ in range(size)]

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(str(bit) for bit in row))
    print()

def read_bit_column_diagonal(matrix, bit_index):
    size = len(matrix)
    column = []
    for row in range(size):
        diag_row = (row + bit_index) % size
        column.append(matrix[diag_row][bit_index])
    return column

def read_word_by_index(matrix, col_index):
    size = len(matrix)
    word = []
    for i in range(size):
        row = (i + col_index) % size
        word.append(matrix[row][col_index])
    return word

def f6(x1, x2):  # XOR
    return 1 if ((not x1 and x2) or (x1 and not x2)) else 0

def f9(x1, x2):  # XNOR
    return 1 if ((x1 and x2) or (not x1 and not x2)) else 0

def f4(x1, x2):  # !x1 * x2
    return 1 if (not x1 and x2) else 0

def f11(x1, x2):  # x1 + !x2
    return 1 if (x1 or not x2) else 0

def write_word_by_index(matrix, col_index, word):
    size = len(matrix)
    for i in range(size):
        row = (i + col_index) % size
        matrix[row][col_index] = word[i]

def apply_logical_function_to_word(matrix, fun, col1, col2, result_col):
    word1 = read_word_by_index(matrix, col1)
    word2 = read_word_by_index(matrix, col2)
    result = [fun(word1[i], word2[i]) for i in range(len(word1))]
    write_word_by_index(matrix, result_col, result)



def add_fields_in_rows(matrix, key):
    """
    Сложение полей A и B в строках, где первые 3 бита равны ключу.
    V = биты 0–2, A = 3–6, B = 7–10, результат S = 11–15.
    """
    key_bits = [int(b) for b in key]

    for row in matrix:
        V = row[0:3]
        if V == key_bits:
            A_bits = row[3:7]
            B_bits = row[7:11]

            A = int(''.join(map(str, A_bits)), 2)
            B = int(''.join(map(str, B_bits)), 2)

            S = A + B

            # Перевод в 5-битный формат
            S_bits = [(S >> (4 - j)) & 1 for j in range(5)]

            # Запись результата обратно в строку
            row[11:16] = S_bits






