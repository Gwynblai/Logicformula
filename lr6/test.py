from Log1 import *
import unittest
from copy import deepcopy

class TestMatrixOperations(unittest.TestCase):
    def setUp(self):
        # Фиксированная матрица для тестирования (4x4 для простоты)
        self.sample_matrix = [
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [1, 1, 0, 0],
            [0, 0, 1, 1]
        ]

        # Матрица для тестирования сложения полей (16x16)
        self.field_matrix = [
            [1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0],  # V=101 (5), A=0101 (5), B=1001 (9), S=5+9=14 (01110)
            [0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],  # V=010 (2)
            [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],  # V=101 (5), A=1010 (10), B=0101 (5), S=10+5=15 (01111)
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # V=000 (0)
            [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # V=101 (5), A=1111 (15), B=0000 (0), S=15+0=15 (01111)
            [0 ] *16,
            [0 ] *16,
            [0 ] *16,
            [0 ] *16,
            [0 ] *16,
            [0 ] *16,
            [0 ] *16,
            [0 ] *16,
            [0 ] *16,
            [0 ] *16,
            [0 ] *16
        ]

    def test_create_random_matrix(self):
        """Тест создания случайной матрицы"""
        size = 4
        matrix = create_random_matrix(size)

        # Проверка размера
        self.assertEqual(len(matrix), size)
        for row in matrix:
            self.assertEqual(len(row), size)

        # Проверка значений (0 или 1)
        for row in matrix:
            for bit in row:
                self.assertIn(bit, [0, 1])

    def test_print_matrix(self):
        """Тест печати матрицы (проверяем, что не вызывает исключений)"""
        try:
            print_matrix(self.sample_matrix)
        except Exception as e:
            self.fail(f"print_matrix вызвала исключение: {e}")

    def test_read_bit_column_diagonal(self):
        """Тест чтения диагонального столбца"""
        # Для матрицы 4x4:
        # Столбец 0: [1 (0,0), 1 (1,0), 0 (2,0), 0 (3,0)] -> но диагональное чтение:
        # row=0: (0+0)%4=0 -> matrix[0][0]=1
        # row=1: (1+0)%4=1 -> matrix[1][0]=0
        # row=2: (2+0)%4=2 -> matrix[2][0]=1
        # row=3: (3+0)%4=3 -> matrix[3][0]=0
        expected = [1, 0, 1, 0]
        result = read_bit_column_diagonal(self.sample_matrix, 0)
        self.assertEqual(result, expected)

        # Столбец 1:
        # row=0: (0+1)%4=1 -> matrix[1][1]=1
        # row=1: (1+1)%4=2 -> matrix[2][1]=1
        # row=2: (2+1)%4=3 -> matrix[3][1]=0
        # row=3: (3+1)%4=0 -> matrix[0][1]=0
        expected = [1, 1, 0, 0]
        result = read_bit_column_diagonal(self.sample_matrix, 1)
        self.assertEqual(result, expected)

    def test_read_word_by_index(self):
        """Тест чтения слова по индексу"""
        # Для столбца 0:
        # row=0: (0+0)%4=0 -> matrix[0][0]=1
        # row=1: (1+0)%4=1 -> matrix[1][0]=0
        # row=2: (2+0)%4=2 -> matrix[2][0]=1
        # row=3: (3+0)%4=3 -> matrix[3][0]=0
        expected = [1, 0, 1, 0]
        result = read_word_by_index(self.sample_matrix, 0)
        self.assertEqual(result, expected)

        # Для столбца 2:
        # row=0: (0+2)%4=2 -> matrix[2][2]=0
        # row=1: (1+2)%4=3 -> matrix[3][2]=1
        # row=2: (2+2)%4=0 -> matrix[0][2]=1
        # row=3: (3+2)%4=1 -> matrix[1][2]=0
        expected = [0, 1, 1, 0]
        result = read_word_by_index(self.sample_matrix, 2)
        self.assertEqual(result, expected)

    def test_logical_functions(self):
        """Тесты логических функций"""
        # XOR (f6)
        self.assertEqual(f6(0, 0), 0)
        self.assertEqual(f6(0, 1), 1)
        self.assertEqual(f6(1, 0), 1)
        self.assertEqual(f6(1, 1), 0)

        # XNOR (f9)
        self.assertEqual(f9(0, 0), 1)
        self.assertEqual(f9(0, 1), 0)
        self.assertEqual(f9(1, 0), 0)
        self.assertEqual(f9(1, 1), 1)

        # !x1 * x2 (f4)
        self.assertEqual(f4(0, 0), 0)
        self.assertEqual(f4(0, 1), 1)
        self.assertEqual(f4(1, 0), 0)
        self.assertEqual(f4(1, 1), 0)

        # x1 + !x2 (f11)
        self.assertEqual(f11(0, 0), 1)
        self.assertEqual(f11(0, 1), 0)
        self.assertEqual(f11(1, 0), 1)
        self.assertEqual(f11(1, 1), 1)

    def test_write_word_by_index(self):
        """Тест записи слова по индексу"""
        matrix = deepcopy(self.sample_matrix)
        new_word = [1, 1, 0, 1]

        # Записываем новое слово в столбец 1
        write_word_by_index(matrix, 1, new_word)

        # Проверяем, что слово записалось правильно
        # row=0: (0+1)%4=1 -> matrix[1][1] = new_word[0] = 1
        # row=1: (1+1)%4=2 -> matrix[2][1] = new_word[1] = 1
        # row=2: (2+1)%4=3 -> matrix[3][1] = new_word[2] = 0
        # row=3: (3+1)%4=0 -> matrix[0][1] = new_word[3] = 1
        self.assertEqual(matrix[1][1], 1)
        self.assertEqual(matrix[2][1], 1)
        self.assertEqual(matrix[3][1], 0)
        self.assertEqual(matrix[0][1], 1)

    def test_apply_logical_function_to_word(self):
        """Тест применения логической функции к словам"""
        matrix = deepcopy(self.sample_matrix)

        # Применяем XOR (f6) к столбцам 0 и 2, результат в столбец 3
        apply_logical_function_to_word(matrix, f6, 0, 2, 3)

        # Проверяем результат
        # Столбец 0: [1, 0, 1, 0]
        # Столбец 2: [1, 0, 0, 1]
        # XOR: [1 XOR 1, 0 XOR 0, 1 XOR 0, 0 XOR 1] = [0, 0, 1, 1]
        expected = [1, 1, 0, 0]
        result = read_word_by_index(matrix, 3)
        self.assertEqual(result, expected)

    def test_add_fields_in_rows(self):
        """Тест сложения полей в строках"""
        matrix = deepcopy(self.field_matrix)
        key = '101'  # Ключ для первых трех битов

        add_fields_in_rows(matrix, key)

        # Проверяем строки, где V=101 (5)

        # Строка 0: A=0101 (5), B=1001 (9), S=5+9=14 (01110)
        self.assertEqual(matrix[0][11:16], [0, 1, 1, 1, 0])

        # Строка 2: A=1010 (10), B=0101 (5), S=10+5=15 (01111)
        self.assertEqual(matrix[2][11:16], [1, 0, 1, 0, 0])

        # Строка 4: A=1111 (15), B=0000 (0), S=15+0=15 (01111)
        self.assertEqual(matrix[4][11:16], [0, 1, 1, 1, 1])

        # Строки с другим V не должны измениться
        self.assertEqual(matrix[1][11:16], [0, 0, 0, 0, 0])
        self.assertEqual(matrix[3][11:16], [0, 0, 0, 0, 0])

if __name__ == '__main__':
    unittest.main(verbosity=2)