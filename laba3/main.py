from table import *
from ex2 import *
from karno import *

def main():
    print("Программа для работы с логическими формулами")
    formula = input("Введите логическую формулу (например, (!a & b & !c & d) | (a & !b & c & d) | (a & b & c & d)): ")
    try:
        lf = Logicformula(formula)
        logic = LogicFormul(formula)
    except Exception as e:
        print(f"Ошибка в формуле: {e}")
        return

    while True:
        print("\nВыберите действие:")
        print("1. Минимизировать (расчетный)")
        print("2. Минимизировать (карно)")
        print("3. Минимизировать (расчетно-табличный метод)")

        print("4. Выйти")

        choice = input("Введите номер действия (1-4): ")

        if choice == '1':
            m=minimize_sknf_quine_mccluskey(lf.table,lf.variables)
            print(m)
            u=minimize_sdnf_quine_mccluskey(lf.table,lf.variables)
            print(u)
        elif choice == '2':
            logic.generate_karnaugh_map()
            sdnf_result = logic.find_sdnf()
            print("\nМинимизированная СДНФ:", sdnf_result)
            e=minimize_sknf_quine_mccluskey(logic.table, logic.variables)
            print(e)

        elif choice == '3':
            nom =lf.get_sknf()
            mon = lf.get_sdnf()
            BooleanMinimizer.minimize_sdnf_by_table(mon)
            BooleanMinimizer.minimize_sknf_by_table(nom)
            r=minimize_sknf_quine_mccluskey(lf.table, lf.variables)
            print(r)
            o = minimize_sdnf_quine_mccluskey(logic.table, logic.variables)
            print(o)
        elif choice == '4':
            print("Программа завершена.")
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 4.")

if __name__ == "__main__":
    main()


