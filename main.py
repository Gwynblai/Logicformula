from tabl import *

def main():
    formula_input = input("Введите логическое выражение: ")
    logic_formula = LogicFormula(formula_input)
    logic_formula.display_truth_table()
    logic_formula.get_sdnf()
    logic_formula.get_sknf()

if __name__ == "__main__":
    main()
