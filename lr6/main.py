
from ex import *
from Log1 import *

def main():
    matrix = None
    while True:


        print("1. Вывести матрицу")
        print("2. Прочитать слово по номеру столбца")
        print("3. Применить логическую функцию к словам")
        print("4. Выполнить арифметическую операцию (сложение Aj и Bj)")
        print("5. Отсортировать матрицу")
        print("6. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            matrix = create_random_matrix(16)

            print("Исходная матрица:")
            print_matrix(matrix)



        elif choice == "2":

            col_index = int(input("Введите номер столбца (0-15): "))

            word = read_word_by_index(matrix, col_index)

            print(f"Слово, прочитанное из столбца с индексом {col_index} с циклическим сдвигом:")
            print(' '.join(str(bit) for bit in word))

        elif choice == "3":
            if matrix is None:
                print("Матрица не создана. Сначала создайте матрицу.")
            else:
                print("Доступные логические функции:")
                print("6: !x1 * x2 + x1 * !x2 (f6)")
                print("9: x1 * x2 + !x1 * !x2 (f9)")
                print("4: !x1 * x2 (f4)")
                print("11: x1 + !x2 (f11)")
                func_choice = input("Выберите функцию (6, 9, 4, 11): ")
                func_map = {"6": f6, "9": f9, "4": f4, "11": f11}
                if func_choice in func_map:
                    word1_col = int(input("Введите номер первого столбца (0-15): "))
                    word2_col = int(input("Введите номер второго столбца (0-15): "))
                    result_col = int(input("Введите номер столбца для записи результата (0-15): "))

                    apply_logical_function_to_word(matrix, func_map[func_choice], word1_col, word2_col, result_col)
                    print("Результат записан в матрицу.")
                    print_matrix(matrix)

                else:
                    print("Некорректный выбор функции.")

        elif choice == "4":
            if matrix is None:
                print("Матрица не создана. Сначала создайте матрицу.")
            else:
                key = input("Введите ключ V (3 бита, например '111'): ")

                add_fields_in_rows(matrix, key)

                print(f"Матрица после сложения A+B → S, где V == {key}:")
                print_matrix(matrix)

        elif choice == "5":
            if matrix is None:
                print("Матрица не создана. Сначала создайте матрицу.")
            else:
                sorted_matrix = sort_matrix_rows(matrix)

                print("Отсортированная матрица (по строкам по возрастанию):")
                print_matrix(sorted_matrix)

        elif choice == "6":
            print("Выход из программы.")
            break

        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()