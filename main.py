from table import *

def main():
    formula = input("Введите логическое выражение: ")

    logic_formula = Logicformula(formula)

    print("\nПеременные:", logic_formula.variables)

    print("\nТаблица истинности:")
    logic_formula.display_table()

    logic_formula.get_sdnf()
    logic_formula.get_sknf()

if __name__ == "__main__":
    main()
