import itertools

class LogicFormula:
    def __init__(self, formula):
        self.formula = formula
        self.variables = self._extract_variables()
        self.truth_table = self._generate_truth_table()

    def _extract_variables(self):
        return sorted({char for char in self.formula if char.isalpha()})

    def _calculate_expression(self, expression):
        print(f"Обработка выражения в calculate: {expression}")
        precedence = {'not': 3, 'and': 2, 'or': 1, '==': 1, '<=': 1}
        output, operators = [], []
        tokens = expression.replace('(', ' ( ').replace(')', ' ) ').split()

        for token in tokens:
            if token in ('0', '1'):
                output.append(int(token))
            elif token in precedence:
                while (operators and operators[-1] != '(' and
                       precedence[operators[-1]] >= precedence[token]):
                    output.append(operators.pop())
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                operators.pop()  # Удаляем '('

        while operators:
            output.append(operators.pop())

        return self._evaluate_postfix(output)

    def _evaluate_postfix(self, output):
        stack = []
        for token in output:
            if isinstance(token, int):
                stack.append(token)
            elif token == 'not':
                stack.append(1 - stack.pop())
            else:
                b = stack.pop()
                a = stack.pop()
                stack.append(self._apply_operator(token, a, b))
        return stack[0] if stack else None

    def _apply_operator(self, operator, a, b):
        if operator == 'and':
            return a & b
        elif operator == 'or':
            return a | b
        elif operator == '==':
            return int(a == b)
        elif operator == '<=':
            return int(not a or b)

    def _evaluate(self, values):
        expression = self.formula
        for var, val in zip(self.variables, values):
            expression = expression.replace(var, str(val))

        expression = (expression.replace('!', ' not ')
                       .replace('¬', ' not ')
                       .replace('&', ' and ')
                       .replace('∧', ' and ')
                       .replace('^', ' and ')
                       .replace('|', ' or ')
                       .replace('∨', ' or ')
                       .replace('->', ' <= ')
                       .replace('→', ' <= ')
                       .replace('~', ' == '))
        print(f"Подставленное выражение: {expression}")  # отладка
        return self._calculate_expression(expression)

    def _generate_truth_table(self):
        return [(values, self._evaluate(values))
                for values in itertools.product([0, 1], repeat=len(self.variables))]

    def display_truth_table(self):
        header = " | ".join(self.variables) + " | Result"
        print(header)
        print("-" * len(header))

        for values, result in self.truth_table:
            row = " | ".join(map(str, values)) + " | " + str(result)
            print(row)

    def _binary_to_decimal(self, binary_str):
        return int(binary_str, 2)

    def get_sdnf(self):
        terms, indexes, result_vector = [], [], ""

        for i, (vals, res) in enumerate(self.truth_table):
            result_vector += str(res)
            if res == 1:
                term = [var if val else f'¬{var}' for var, val in zip(self.variables, vals)]
                terms.append("(" + " ∧ ".join(term) + ")")
                indexes.append(i)

        print("\nСДНФ (строковая):", " ∨ ".join(terms) if terms else "0")
        print("СДНФ (числовая):", f"({', '.join(map(str, indexes))}) ∨" if indexes else "0")
        print("Индексная форма функции (вектор значений):", f'"{result_vector} - {self._binary_to_decimal(result_vector)}"')

    def get_sknf(self):
        terms, indexes, result_vector = [], [], ""

        for i, (vals, res) in enumerate(self.truth_table):
            result_vector += str(res)
            if res == 0:
                term = [f'¬{var}' if val else var for var, val in zip(self.variables, vals)]
                terms.append("(" + " ∨ ".join(term) + ")")
                indexes.append(i)

        print("\nСКНФ (строковая):", " ∧ ".join(terms) if terms else "1")
        print("СКНФ (числовая):", f"({', '.join(map(str, indexes))}) ∧" if indexes else "1")
        print("Индексная форма функции (вектор значений):", f'"{result_vector}"')