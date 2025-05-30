import random

def find_max_words(words):
    size = len(words[0])
    n = len(words)
    active_flags = [1] * n

    for bit_pos in range(size):
        has_one = False
        for i in range(n):
            if active_flags[i] == 1 and words[i][bit_pos] == 1:
                has_one = True
                break

        if has_one:
            for i in range(n):
                if active_flags[i] == 1 and words[i][bit_pos] == 0:
                    active_flags[i] = 0

        if sum(active_flags) == 1:
            break

    max_indices = [i for i, flag in enumerate(active_flags) if flag == 1]
    return max_indices

def ordered_selection_sort(words):
    words = words[:]
    n = len(words)
    sorted_words = []
    active_indices = list(range(n))

    while active_indices:
        active_words = [words[i] for i in active_indices]
        max_local_indices = find_max_words(active_words)
        max_global_indices = [active_indices[i] for i in max_local_indices]

        for idx in max_global_indices:
            sorted_words.append(words[idx])

        active_indices = [i for i in active_indices if i not in max_global_indices]

    sorted_words.reverse()  # по возрастанию
    return sorted_words

def create_random_matrix(size):
    return [[random.randint(0, 1) for _ in range(size)] for _ in range(size)]

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(str(bit) for bit in row))
    print()

def sort_matrix_rows(matrix):
    sorted_matrix = ordered_selection_sort(matrix)
    return sorted_matrix


