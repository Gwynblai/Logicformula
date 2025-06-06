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
    return sum(a != b for a, b in zip(term1, term2)) == 1

def combine_terms(term1, term2):
    return ''.join(a if a == b else '-' for a, b in zip(term1, term2))

def covers(implicant, term):
    return all(i == t or i == '-' for i, t in zip(implicant, term))

# === Группировка и объединение ===

def group_by_ones(terms):
    grouped = {}
    for term in terms:
        ones = count_ones(term)
        grouped.setdefault(ones, []).append(term)
    return grouped

def generate_combinations(group1, group2):
    for t1, t2 in itertools.product(group1, group2):
        if differ_by_one_bit(t1, t2):
            yield t1, t2, combine_terms(t1, t2)

def combine_groups(groups):
    new_groups = {}
    marked = set()
    keys = sorted(groups)

    for k1, k2 in zip(keys, keys[1:]):
        for t1, t2, combined in generate_combinations(groups[k1], groups[k2]):
            marked.update([t1, t2])
            ones = count_ones(combined.replace('-', '0'))
            new_groups.setdefault(ones, set()).add(combined)

    return new_groups, marked

def get_unmarked_terms(groups, marked):
    """Возвращает термы, которые не были объединены"""
    return {
        term
        for group in groups.values()
        for term in group
        if term not in marked
    }

def build_next_groups(groups):
    """Строит новые группы и отмечает объединённые термы"""
    new_groups, marked = combine_groups(groups)
    unmarked = get_unmarked_terms(groups, marked)
    return new_groups, unmarked

# === Получение всех простых импликант ===

def extract_prime_implicants(minterms):
    groups = group_by_ones(minterms)
    prime_implicants = set()

    while groups:
        groups, unmarked = build_next_groups(groups)
        prime_implicants.update(unmarked)
        groups = {k: list(v) for k, v in groups.items()}

    return prime_implicants

# === Поиск эссенциальных импликант ===

def build_coverage_table(prime_implicants, minterms):
    coverage = {m: set() for m in minterms}
    for implicant in prime_implicants:
        for m in minterms:
            if covers(implicant, m):
                coverage[m].add(implicant)
    return coverage

def select_essential_implicants(prime_implicants, minterms):
    coverage = build_coverage_table(prime_implicants, minterms)
    essential = set()

    while coverage:
        single_covered = [(m, imps) for m, imps in coverage.items() if len(imps) == 1]
        if single_covered:
            m, imps = single_covered[0]
            imp = next(iter(imps))
            essential.add(imp)
            coverage = {k: v for k, v in coverage.items() if not covers(imp, k)}
        else:
            best = max(prime_implicants, key=lambda imp: sum(1 for m in coverage if covers(imp, m)), default=None)
            if not best:
                break
            essential.add(best)
            coverage = {k: v for k, v in coverage.items() if not covers(best, k)}

    return essential

# === Преобразование в выражение ===

def sknf_term_to_expr(term, variables):
    return '(' + ' ∨ '.join(
        f'¬{variables[i]}' if bit == '1' else variables[i]
        for i, bit in enumerate(term) if bit != '-'
    ) + ')'

def sdnf_term_to_expr(term, variables):
    return ' ∧ '.join(
        variables[i] if bit == '1' else f'¬{variables[i]}'
        for i, bit in enumerate(term) if bit != '-'
    )

# === Минимизация СКНФ ===

def minimize_sknf_quine_mccluskey(table, variables):
    minterms = [''.join(map(str, vals)) for vals, res in table if res == 0]
    if not minterms:
        return "1"

    prime_implicants = extract_prime_implicants(minterms)
    essential_implicants = select_essential_implicants(prime_implicants, minterms)

    expressions = [sknf_term_to_expr(term, variables) for term in sorted(essential_implicants)]
    return ' ∧ '.join(expressions) if expressions else "1"

# === Минимизация СДНФ ===

def minimize_sdnf_quine_mccluskey(table, variables):
    minterms = [''.join(map(str, vals)) for vals, res in table if res == 1]
    if not minterms:
        return "0"

    prime_implicants = extract_prime_implicants(minterms)
    expressions = [sdnf_term_to_expr(term, variables) for term in sorted(prime_implicants)]
    return ' ∨ '.join(expr for expr in expressions if expr) or "1"










