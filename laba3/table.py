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
        preced = {'not': 3, 'and': 2, 'or': 1, '==': 1, '<=': 1}
        output = []
        operand = []
        express = express.replace('(', ' ( ').replace(')', ' ) ')
        tokens = express.split()

        for token in tokens:
            if token in ('0', '1'):
                output.append(int(token))
            elif token in preced:
                while operand and operand[-1] != '(' and preced.get(operand[-1], 0) >= preced[token]:
                    output.append(operand.pop())
                operand.append(token)
            elif token == '(':
                operand.append(token)
            elif token == ')':
                while operand and operand[-1] != '(':
                    output.append(operand.pop())
                operand.pop()

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
                    stack.append(1 if a == b else 0)
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
                   .replace('~', ' == '))  # Замена стрелки на логическое равенство
        return self.calc(express)

    def gener_table(self):
        table = []
        for value in itertools.product([0, 1], repeat=len(self.variables)):
            res = self.evalu(value)
            table.append((value, res))
        return table

    def display_table(self):
        header = " | ".join(self.variables) + " | Result"
        print("\nТаблица истинности:")
        print(header)
        print("-" * len(header))
        for values, result in self.table:
            row = " | ".join(map(str, values)) + " | " + str(result)
            print(row)

    def get_sknf(self):
        terms = []
        indexes = []
        result_vector = ""
        for i, (vals, res) in enumerate(self.table):
            result_vector += str(res)
            if res == 0:
                term = []
                for var, val in zip(self.variables, vals):
                    term.append(f'!{var}' if val else var)
                terms.append("(" + " | ".join(term) + ")")
                indexes.append(i)
        return " & ".join(terms) if terms else "1"
        #print("\nСКНФ (строковая):", " ∧ ".join(terms) if terms else "1")
        #print("СКНФ (числовая):", f"({', '.join(map(str, indexes))}) ∧" if indexes else "1")
        #print("Индексная форма функции (вектор значений):", f'"{result_vector}"')

    def get_sdnf(self):
        terms = []
        indexes = []
        result_vector = ""
        for i, (vals, res) in enumerate(self.table):
            result_vector += str(res)
            if res == 1:
                term = []
                for var, val in zip(self.variables, vals):
                    term.append(f'{var}' if val else f'!{var}')
                term_str = " & ".join(term)
                terms.append(f"({term_str})")
                indexes.append(i)

        return " | ".join(terms) if terms else "0"
        #print("\nСДНФ (строковая):", " ∨ ".join(terms) if terms else "0")
        #print("СДНФ (числовая):", f"({', '.join(map(str, indexes))}) ∨" if indexes else "0")
        #print("Индексная форма функции (вектор значений):", f'"{result_vector}"')




# ====================
# Минимизация СКНФ
# ====================

def count_ones(term):
    return term.count('1')

def differ_by_one_bit(term1, term2):
    diff = 0
    for a, b in zip(term1, term2):
        if a != b:
            diff += 1
        if diff > 1:
            return False
    return diff == 1

def combine_terms(term1, term2):
    return ''.join([a if a == b else '-' for a, b in zip(term1, term2)])

def covers_minterm(implicant, minterm):
    return all(i == m or i == '-' for i, m in zip(implicant, minterm))

def minimize_sknf_quine_mccluskey(table, variables):
    # Собираем минтермы, где функция равна 0
    minterms = [''.join(map(str, vals)) for vals, res in table if res == 0]
    if not minterms:
        print("\nМинимизированная СКНФ: 1")
        return

    # Шаг 1: Группировка термов по количеству единиц
    groups = {}
    for term in minterms:
        ones = count_ones(term)
        groups.setdefault(ones, []).append(term)

    # Шаг 2: Формирование простых импликант
    prime_implicants = set()
    while groups:
        new_groups = {}
        marked = set()

        keys = sorted(groups.keys())
        for i in range(len(keys) - 1):
            g1 = groups[keys[i]]
            g2 = groups[keys[i + 1]]
            for term1 in g1:
                for term2 in g2:
                    if differ_by_one_bit(term1, term2):
                        combined = combine_terms(term1, term2)
                        marked.add(term1)
                        marked.add(term2)
                        ones = count_ones(combined.replace('-', '0'))
                        new_groups.setdefault(ones, set()).add(combined)

        # Добавляем немаркированные термы в простые импликанты
        for group in groups.values():
            for term in group:
                if term not in marked:
                    prime_implicants.add(term)

        groups = {k: list(v) for k, v in new_groups.items()}

    # Отладочный вывод
    print("Простые импликанты:", prime_implicants)

    # Шаг 3: Выбор эссенциальных импликант
    essential_implicants = set()
    minterm_coverage = {m: set() for m in minterms}

    # Находим, какие минтермы покрывает каждый импликант
    for implicant in prime_implicants:
        for minterm in minterms:
            if covers_minterm(implicant, minterm):
                minterm_coverage[minterm].add(implicant)

    # Выбираем эссенциальные импликанты
    while minterm_coverage:
        for minterm, implicants in list(minterm_coverage.items()):
            if len(implicants) == 1:  # Эссенциальный импликант
                implicant = next(iter(implicants))
                essential_implicants.add(implicant)
                # Удаляем покрытые минтермы
                for m in minterms:
                    if covers_minterm(implicant, m):
                        minterm_coverage.pop(m, None)
                break
        else:
            # Выбираем импликант, покрывающий наибольшее число минтермов
            max_coverage = 0
            best_implicant = None
            for implicant in prime_implicants:
                # Предпочитаем импликанты с меньшим числом '-' для большей специфичности
                count = sum(1 for m in minterms if covers_minterm(implicant, m) and m in minterm_coverage)
                # Добавляем небольшой бонус за импликанты, включающие 'a' (переменная с индексом 0)
                if implicant[0] in '01':
                    count += 0.1
                if count > max_coverage:
                    max_coverage = count
                    best_implicant = implicant
            if best_implicant:
                essential_implicants.add(best_implicant)
                for m in minterms:
                    if covers_minterm(best_implicant, m):
                        minterm_coverage.pop(m, None)
            else:
                break

    # Шаг 4: Преобразование импликант в выражение
    def term_to_expression(term):
        parts = []
        for i, ch in enumerate(term):
            if ch == '1':
                parts.append(f'¬{variables[i]}')
            elif ch == '0':
                parts.append(f'{variables[i]}')
        return '(' + ' ∨ '.join(parts) + ')' if parts else None

    expressions = [term_to_expression(t) for t in sorted(essential_implicants)]
    expressions = [expr for expr in expressions if expr]  # Удаляем None


    return ' ∧ '.join(expressions) if expressions else "1"


# ====================
# Минимизация СДНФ
# ====================

def minimize_sdnf_quine_mccluskey(table, variables):
    minterms = [''.join(map(str, vals)) for vals, res in table if res == 1]
    if not minterms:
        print("\nМинимизированная СДНФ: 0")
        return

    groups = {}
    for term in minterms:
        ones = term.count('1')
        groups.setdefault(ones, []).append(term)

    prime_implicants = set()
    checked = set()

    while True:
        new_groups = {}
        marked = set()

        keys = sorted(groups.keys())
        for i in range(len(keys) - 1):
            group1 = groups[keys[i]]
            group2 = groups[keys[i + 1]]
            for term1 in group1:
                for term2 in group2:
                    diff = sum(a != b for a, b in zip(term1, term2))
                    if diff == 1:
                        combined = ''.join('-' if a != b else a for a, b in zip(term1, term2))
                        marked.add(term1)
                        marked.add(term2)
                        ones = combined.count('1')
                        new_groups.setdefault(ones, set()).add(combined)

        for group in groups.values():
            for term in group:
                if term not in marked:
                    prime_implicants.add(term)

        if not new_groups:
            break
        else:
            groups = {k: list(v) for k, v in new_groups.items()}

    def term_to_expression(term):
        parts = []
        for i, ch in enumerate(term):
            if ch == '1':
                parts.append(f'{variables[i]}')
            elif ch == '0':
                parts.append(f'¬{variables[i]}')
        return ' ∧ '.join(parts)  # без лишних скобок

    expressions = [term_to_expression(term) for term in sorted(prime_implicants) if '-' not in term or term.strip('-')]

    return ' ∨ '.join(expr for expr in expressions if expr) or "1"









