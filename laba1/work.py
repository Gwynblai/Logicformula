def to_binary(n):
    # Если число равно 0, возвращаем 8 нулей
    if n == 0:
        return '0' * 8

    # Определяем, является ли число отрицательным
    is_negative = n < 0
    n = abs(n)  # Берем модуль числа для преобразования

    binary = ''
    while n > 0:
        binary = str(n % 2) + binary
        n = n // 2

    # Добавляем ведущие нули до 7 бит
    while len(binary) < 7:
        binary = '0' + binary  # Добавляем ноль в начало строки

    # Если число было отрицательным, устанавливаем старший бит в 1
    if is_negative:
        binary = '1' + binary
    else:
        binary = '0' + binary

    return binary

def to_invert(binary):
    if binary[0] == '1':  # Проверяем, является ли число отрицательным
        inverted_binary = binary[0]  # Сохраняем знаковый бит
        for bit in binary[1:]:
            inverted_binary += '0' if bit == '1' else '1'
        return inverted_binary
    else:
        return binary  # Для положительных чисел возвращаем исходное значение

def to_dop(binary):
    inv=to_invert(binary)
    if binary[0] == '1':  # Если число отрицательное
        bina = ''  # Начинаем с пустой строки для результата
        carry = 1  # Начинаем с 1 для добавления
        for bit in reversed(inv):  # Итерируем по инвертированным битам
            if bit == '1' and carry == 1:
                bina += '0'
            elif bit == '0' and carry == 1:
                bina += '1'
                carry = 0
            else:
                bina += bit
        return bina[::-1]  # Возвращаем в правильном порядке
    else:
        return binary  # Для положительных чисел возвращаем сам бинарный код


def sum_dop(stroka2, inverted_binary):
    bi = ''
    carry = 0  # Переменная для переноса

    # Итерируем по инвертированным битам и другой строке
    for bit, bit1 in zip(reversed(inverted_binary), reversed(stroka2)):
        total = carry + int(bit) + int(bit1)

        if total == 0:
            bi += '0'
            carry = 0
        elif total == 1:
            bi += '1'
            carry = 0
        elif total == 2:  # 1 + 1
            bi += '0'
            carry = 1
        elif total == 3:  # 1 + 1 + 1 (с переносом)
            bi += '1'
            carry = 1

    # Если остался перенос, добавляем его
    if carry:
        bi += '1'

    result_binary = bi[::-1]  # Возвращаем в правильном порядке
    result_binary = result_binary[-8:]  # Ограничиваем до 8 бит

    # Преобразуем двоичное представление в десятичное
    if len(result_binary) == 8 and result_binary[0] == '1':  # Если отрицательное число
        inverted = ''.join('1' if b == '0' else '0' for b in result_binary)  # Инвертируем биты
        result_decimal = - (int(inverted, 2) + 1)  # Получаем десятичное значение
    else:
        result_decimal = int(result_binary, 2)

    return result_binary, result_decimal  # Возвращаем как двоичное, так и десятичное представление

def to_negative_in_twos_complement(binary):
    inverted = ''.join('1' if b == '0' else '0' for b in binary)
    return sum_dop(inverted, '00000001')[0]  # Возвращаем только двоичное представление

def subtract_positive_numbers(minuend, subtrahend):
    """Вычитает одно положительное число из другого."""
    # Преобразуем вычитаемое число в отрицательное представление
    negative_subtrahend = to_negative_in_twos_complement(subtrahend)
    # Складываем уменьшаемое с отрицательным вычитаемым
    return sum_dop(minuend, negative_subtrahend)

def multiply_binary_strings(bin1, bin2):
    # Инициализация массива для хранения результатов
    results = [0] * (len(bin1) + len(bin2))

    # Умножение каждого разряда
    for i in range(len(bin1)):
        for j in range(len(bin2)):
            results[i + j] += int(bin1[len(bin1) - 1 - i]) * int(bin2[len(bin2) - 1 - j])

    # Обработка переносов
    carry = 0
    for i in range(len(results)):
        results[i] += carry
        carry = results[i] // 2
        results[i] %= 2

    # Удаление ведущих нулей
    while len(results) > 1 and results[-1] == 0:
        results.pop()

    # Формирование строки результата
    result_str = ''.join(map(str, results[::-1]))

    return result_str

def binary_to_decimal(bin_str):

        return int(bin_str, 2)  # Для положительных чисел просто возвращаем десятичное значение

def divide_binary_strings(bin1, bin2):
    # Преобразуем двоичные строки в десятичные
    num1 = binary_to_decimal(bin1)
    num2 = binary_to_decimal(bin2)

    # Проверка на деление на ноль
    if num2 == 0:
        return "Ошибка: деление на ноль"

    # Получаем целую часть
    integer_part = num1 // num2
    remainder = num1 % num2

    # Начинаем работу с дробной частью
    decimal_part = []
    for _ in range(5):  # Ограничение до 5 знаков после запятой
        remainder *= 2  # Умножаем на 2 для двоичной дроби
        decimal_digit = remainder // num2
        decimal_part.append(str(decimal_digit))
        remainder %= num2

    # Преобразуем целую часть в двоичный формат
    binary_integer_part = to_binary(integer_part)
    binary_decimal_part = ''.join(decimal_part)

    # Формируем результат в двоичном формате
    if binary_decimal_part:
        binary_result = f"{binary_integer_part}.{binary_decimal_part}"
    else:
        binary_result = binary_integer_part

    # Преобразуем целую часть в десятичный формат
    decimal_result = integer_part

    # Преобразуем дробную часть в десятичный формат
    for idx, digit in enumerate(decimal_part):
        decimal_result += int(digit) / (2 ** (idx + 1))

    # Округляем результат до 5 знаков после запятой
    decimal_result = round(decimal_result, 5)

    return binary_result, decimal_result

def float_to_ieee754(num):
    sign_bit = '1' if num < 0 else '0'
    if num == 0:
        return '0' * 32

    num = abs(num)
    integer_part = int(num)
    fractional_part = num - integer_part

    integer_binary = bin(integer_part)[2:] if integer_part > 0 else ''
    fractional_binary = ''

    while fractional_part and len(fractional_binary) < 23:
        fractional_part *= 2
        bit = int(fractional_part)
        fractional_binary += str(bit)
        fractional_part -= bit

    if integer_binary:
        exponent = len(integer_binary) - 1
    elif '1' in fractional_binary:
        exponent = -fractional_binary.index('1') - 1
    else:
        return '0' * 32

    exponent_bits = bin(exponent + 127)[2:].zfill(8)
    mantissa_bits = (integer_binary[1:] + fractional_binary).ljust(23, '0')[:23]

    return f'{sign_bit}{exponent_bits}{mantissa_bits}'

def ieee754_to_float(ieee_binary):
    sign = int(ieee_binary[0])
    exponent = int(ieee_binary[1:9], 2) - 127
    mantissa = ieee_binary[9:]

    if exponent == -127 and all(b == '0' for b in mantissa):
        return 0.0

    mantissa_value = 1

    for i, bit in enumerate(mantissa):
        if bit == '1':
            mantissa_value += 2 ** -(i + 1)

    return (-1) ** sign * mantissa_value * (2 ** exponent)

def sum_floats_ieee754(first_float, second_float):
    if first_float < 0 or second_float < 0:
        raise ValueError("Error Sign Value.")

    first_binary = float_to_ieee754(first_float)
    second_binary = float_to_ieee754(second_float)

    first_exponent = int(first_binary[1:9], 2)
    first_mantissa = int(first_binary[9:], 2)

    second_exponent = int(second_binary[1:9], 2)
    second_mantissa = int(second_binary[9:], 2)

    first_mantissa |= (1 << 23)
    second_mantissa |= (1 << 23)

    if first_exponent > second_exponent:
        second_mantissa >>= (first_exponent - second_exponent)
        exponent = first_exponent
    else:
        first_mantissa >>= (second_exponent - first_exponent)
        exponent = second_exponent

    result_mantissa = first_mantissa + second_mantissa

    if result_mantissa & (1 << 24):
        result_mantissa >>= 1
        exponent += 1

    result_mantissa &= ~(1 << 23)

    if exponent >= 255:
        raise OverflowError("Exponent Overflow.")

    result_binary = f"{0:01b}{format(exponent, '08b')}{format(result_mantissa, '023b')}"
    result_float = ieee754_to_float(result_binary)

    return result_float, result_binary
