
import unittest
from work import *
class TestBinaryOperations(unittest.TestCase):

    # Тесты для to_binary
    def test_to_binary(self):
        self.assertEqual(to_binary(0), '00000000')  # Ноль
        self.assertEqual(to_binary(1), '00000001')  # Положительное число
        self.assertEqual(to_binary(-1), '10000001')  # Отрицательное число
        self.assertEqual(to_binary(127), '01111111')  # Максимальное положительное 7-битное число
        self.assertEqual(to_binary(-128), '110000000')  # Минимальное отрицательное 8-битное число

    # Тесты для to_invert
    def test_to_invert(self):
        self.assertEqual(to_invert('00000000'), '00000000')  # Ноль
        self.assertEqual(to_invert('11111111'), '10000000')  # Все биты установлены
        self.assertEqual(to_invert('10101010'), '11010101')  # Чередующиеся биты

    # Тесты для to_dop
    def test_to_dop(self):
        self.assertEqual(to_dop('00000000'), '00000000')  # Ноль
        self.assertEqual(to_dop('10000001'), '11111111')  # Отрицательное число
        self.assertEqual(to_dop('10101010'), '11010110')  # Чередующиеся биты

    # Тесты для sum_dop
    def test_sum_dop(self):
        self.assertEqual(sum_dop('00000001', '00000001'), ('00000010', 2))  # 1 + 1 = 2
        self.assertEqual(sum_dop('10000001', '00000001'), ('10000010', -126))  # -127 + 1 = -126
        self.assertEqual(sum_dop('11111111', '00000001'), ('00000000', 0))  # -1 + 1 = 0
        self.assertEqual(sum_dop('01111111', '00000001'), ('10000000', -128))  # 127 + 1 = -128 (переполнение)

    # Тесты для to_negative_in_twos_complement
    def test_to_negative_in_twos_complement(self):
        self.assertEqual(to_negative_in_twos_complement('00000001'), '11111111')  # 1 -> -1
        self.assertEqual(to_negative_in_twos_complement('00000010'), '11111110')  # 2 -> -2

    # Тесты для subtract_positive_numbers
    def test_subtract_positive_numbers(self):
        self.assertEqual(subtract_positive_numbers('00001000', '00000010'), ('00000110', 6))  # 8 - 2 = 6
        self.assertEqual(subtract_positive_numbers('00000010', '00001000'), ('11111010', -6))  # 2 - 8 = -6

    # Тесты для multiply_binary_strings
    def test_multiply_binary_strings(self):
        self.assertEqual(multiply_binary_strings('1010', '0011'), '11110')  # 10 * 3 = 30
        self.assertEqual(multiply_binary_strings('1111', '0001'), '1111')  # 15 * 1 = 15
        self.assertEqual(multiply_binary_strings('0000', '1111'), '0')  # 0 * 15 = 0

    # Тесты для divide_binary_strings
    def test_divide_binary_strings(self):
        self.assertEqual(divide_binary_strings('1010', '0010'), ('00000101.00000', 5.0))  # 10 / 2 = 5
        self.assertEqual(divide_binary_strings('1100', '0011'), ('00000100.00000', 4.0))  # 12 / 3 = 4
        self.assertEqual(divide_binary_strings('1010', '0000'), "Ошибка: деление на ноль")  # Деление на ноль

    # Тесты для binary_to_decimal
    def test_binary_to_decimal(self):
        self.assertEqual(binary_to_decimal('00000000'), 0)  # Ноль
        self.assertEqual(binary_to_decimal('00000001'), 1)  # 1
        self.assertEqual(binary_to_decimal('11111111'), 255)  # 255

    # Тесты для float_to_ieee754
    def test_positive_number(self):
        result = float_to_ieee754(12.375)
        self.assertEqual(result, '01000001010001100000000000000000')

    def test_negative_number(self):
        result = float_to_ieee754(-12.375)
        self.assertEqual(result, '11000001010001100000000000000000')

    def test_zero(self):
        result = float_to_ieee754(0)
        self.assertEqual(result, '00000000000000000000000000000000')

    def test_small_positive_number(self):
        result = float_to_ieee754(0.15625)
        self.assertEqual(result, '00111110000101000000000000000000')

    def test_small_negative_number(self):
        result = float_to_ieee754(-0.15625)
        self.assertEqual(result, '10111110000101000000000000000000')

    def test_large_positive_number(self):
        result = float_to_ieee754(123456.789)
        self.assertEqual(result, '01000111111100010010000001100100')

    def test_large_negative_number(self):
        result = float_to_ieee754(-123456.789)
        self.assertEqual(result, '11000111111100010010000001100100')

    def test_fractional_part_only(self):
        result = float_to_ieee754(0.5)
        self.assertEqual(result, '00111111010000000000000000000000')

    def test_integer_part_only(self):
        result = float_to_ieee754(10.0)
        self.assertEqual(result, '01000001001000000000000000000000')

    def test_very_small_number(self):
        result = float_to_ieee754(1.17549435e-38)
        self.assertEqual(result, '00000000000000000000000000000000')

    def test_very_large_number(self):
        result = float_to_ieee754(3.4028235e+38)
        self.assertEqual(result, '01111111011111111111111111111111')

    # Тесты для ieee754_to_float
    def test_ieee754_to_float(self):
        self.assertEqual(ieee754_to_float('00000000000000000000000000000000'), 0.0)  # Ноль
        self.assertEqual(ieee754_to_float('00111111100000000000000000000000'), 1.0)  # 1.0
        self.assertEqual(ieee754_to_float('10111111100000000000000000000000'), -1.0)  # -1.0


    def test_sum_floats_ieee754(self):
        self.assertEqual(sum_floats_ieee754(1.0, 1.0), (2.0, '01000000000000000000000000000000'))  # 1.0 + 1.0 = 2.0
        self.assertEqual(sum_floats_ieee754(1.0, 2.0), (3.0, '01000000010000000000000000000000'))  # 0.5 + 0.25 = 0.75
        with self.assertRaises(ValueError):  # Ошибка при отрицательных числах
            sum_floats_ieee754(-1.0, 1.0)






if __name__ == 'main':
    unittest.main()
