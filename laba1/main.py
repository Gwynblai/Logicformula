from work import *


# Блок тестирования
if __name__ == "__main__":
    while True:
        print("\nВыберите операцию:")
        print("1. Сложение чисел с плавающей запятой")
        print("2. Вычитание положительных чисел")
        print("3. Умножение двоичных чисел")
        print("4. Деление двоичных чисел")
        print("5. Преобразование числа в двоичный формат")
        print("6. Преобразование двоичного числа в десятичное")
        print("7. Инвертирование битов и получение дополнительного кода")
        print("8. Сложение с использованием sum_dop")
        print("9. Выход")

        choice = input("Введите номер операции: ")

        if choice == '1':
            first_float = float(input("Введите первое число: "))
            second_float = float(input("Введите второе число: "))
            result_float, result_binary = sum_floats_ieee754(first_float, second_float)
            print(f"Сложение {first_float} и {second_float}:")
            print(f"Результат: {result_float} (в двоичном: {result_binary})")

        elif choice == '2':
            minuend = input("Введите уменьшаемое (в двоичном формате): ")
            subtrahend = input("Введите вычитаемое (в двоичном формате): ")
            result = subtract_positive_numbers(minuend, subtrahend)
            print(f"Результат вычитания: {result[0]} (в десятичном: {result[1]})")


        elif choice == '3':

            num1 = int(input("Введите первое число (в десятичном формате): "))

            num2 = int(input("Введите второе число (в десятичном формате): "))

            bin1 = to_binary(num1)

            bin2 = to_binary(num2)

            result = multiply_binary_strings(bin1, bin2)

            print(f"Произведение {bin1} и {bin2} равно: {result} (в десятичном: {binary_to_decimal(result)})")


        elif choice == '4':

            num1 = int(input("Введите делимое (в десятичном формате): "))

            num2 = int(input("Введите делитель (в десятичном формате): "))

            bin1 = to_binary(num1)

            bin2 = to_binary(num2)

            binary_result, decimal_result = divide_binary_strings(bin1, bin2)

            print(f"Результат деления {bin1} на {bin2} в двоичном формате: {binary_result}")

            print(f"Результат деления {bin1} на {bin2} в десятичном формате: {decimal_result}")

        elif choice == '5':
            number = int(input("Введите число для преобразования в двоичный формат: "))
            binary_representation = to_binary(number)
            print(f"Двоичное представление {number}: {binary_representation}")

        elif choice == '6':
            bin_str = input("Введите двоичное число для преобразования в десятичное: ")
            decimal_value = binary_to_decimal(bin_str)
            print(f"Десятичное представление {bin_str}: {decimal_value}")

        elif choice == '7':
            number = int(input("Введите число для преобразования: "))
            binary_representation = to_binary(number)
            print(f"Двоичное представление: {binary_representation}")

            inverted_binary = to_invert(binary_representation)
            print(f"Инвертированное представление: {inverted_binary}")

            twos_complement = to_dop(binary_representation)
            print(f"Дополнительный код: {twos_complement} ")


        elif choice == '8':

            num1 = int(input("Введите первое число (в десятичном формате): "))

            num2 = int(input("Введите второе число (в десятичном формате): "))

            bin1 = to_binary(num1)

            bin2 = to_binary(num2)
            if num1 < 0:
                bin1 = to_dop(to_binary(num1))
            else:
                bin1 = to_binary(num1)

            if num2 < 0:
                bin2 = to_dop(to_binary(num2))
            else:
                bin2 = to_binary(num2)

                # Теперь выполняем сложение
            result_binary, result_decimal = sum_dop(bin1, bin2)

            print(f"Результат сложения: {result_binary} (в десятичном: {result_decimal})")

        elif choice == '9':
            print("Выход из программы.")
            break

        else:
            print("Некорректный ввод. Пожалуйста, выберите снова.")
