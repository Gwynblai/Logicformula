import itertools
class Logicformula:
    def __init__(self, formula):
        self.formula = formula
        self.variables = self.isvlech(formula)
        self.table = self.gener_table()

    def isvlech(self, formula):
        variables = set()
        for char in formula:
            if char.isalpha():
                variables.add(char)
        return sorted(variables)

    def calc(self, express):
        print(f"Обработка выражения в calc: {express}")
        preced = {'not': 3, 'and': 2, 'or': 1, '==': 1, '<=': 1}
        output = []
        operand = []
        express = express.replace('(', ' ( ').replace(')', ' ) ')
        tokens = express.split()

        for token in tokens:
            if token in ('0', '1'):
                output.append(int(token))
            elif token in preced:
                while (operand and operand[-1] != '(' and
                       preced.get(operand[-1], 0) >= preced[token]):
                    output.append(operand.pop())
                operand.append(token)
            elif token == '(':
                operand.append(token)
            elif token == ')':
                while operand and operand[-1] != '(':
                    output.append(operand.pop())
                operand.pop()  # Удаляем '('

        while operand:
            output.append(operand.pop())

        stack = []
        for token in output:
            if isinstance(token, int):
                stack.append(token)
            elif token == 'not':
                stack.append(1 - stack.pop())
            else:
                b = stack.pop()
                a = stack.pop()
                if token == 'and':
                    stack.append(a & b)
                elif token == 'or':
                    stack.append(a | b)
                elif token == '==':
                    a, b = stack.pop(), stack.pop()
                    operationResult = 1 if a == b else 0
                    stack.append(operationResult)
                elif token == '<=':
                    stack.append(int(not a or b))
        return stack[0]

    def evalu(self, value):
        express = self.formula
        for var, val in zip(self.variables, value):
            express = express.replace(var, str(val))

        express = (express.replace('!', ' not ')
                   .replace('¬', ' not ')
                   .replace('&', ' and ')
                   .replace('∧', ' and ')
                   .replace('^', ' and ')
                   .replace('|', ' or ')
                   .replace('∨', ' or ')
                   .replace('->', ' <= ')
                   .replace('→', ' <= ')
                   .replace('~', ' == '))
        print(f"Подставленное выражение: {express}")  # отладка
        return self.calc(express)

    def gener_table(self):
        table = []
        for value in itertools.product([0, 1], repeat=len(self.variables)):
            res = self.evalu(value)
            table.append((value, res))
        return table

    def display_table(self):
        # Заголовок таблицы
        header = " | ".join(self.variables) + " | Result"
        print(header)
        print("-" * len(header))

        # Вывод строк таблицы
        for values, result in self.table:
            row = " | ".join(map(str, values)) + " | " + str(result)
            print(row)

    def binary_to_decimal(sekf,bin_str):

        return int(bin_str, 2)

    def get_sdnf(self):
        terms = []
        indexes = []
        result_vector = ""

        for i, (vals, res) in enumerate(self.table):
            result_vector += str(res)
            if res == 1:
                term = []
                for var, val in zip(self.variables, vals):
                    term.append(var if val else f'¬{var}')
                terms.append("(" + " ∧ ".join(term) + ")")
                indexes.append(i)

        print("\nСДНФ (строковая):", " ∨ ".join(terms) if terms else "0")
        print("СДНФ (числовая):", f"({', '.join(map(str, indexes))}) ∨" if indexes else "0")
        print("Индексная форма функции (вектор значений):", f'"{result_vector} - {self.binary_to_decimal(result_vector)}"')

    def get_sknf(self):
        terms = []
        indexes = []
        result_vector = ""

        for i, (vals, res) in enumerate(self.table):
            result_vector += str(res)
            if res == 0:
                term = []
                for var, val in zip(self.variables, vals):
                    term.append(f'¬{var}' if val else var)
                terms.append("(" + " ∨ ".join(term) + ")")
                indexes.append(i)

        print("\nСКНФ (строковая):", " ∧ ".join(terms) if terms else "1")
        print("СКНФ (числовая):", f"({', '.join(map(str, indexes))}) ∧" if indexes else "1")
        print("Индексная форма функции (вектор значений):", f'"{result_vector}"')


# Пример использования

