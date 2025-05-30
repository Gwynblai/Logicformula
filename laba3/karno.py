import itertools

from sympy import SOPform, symbols



class LogicFormul:
    def __init__(self, formula):
        self.formula = formula
        self.variables = self.extract_variables(formula)
        self.table = self.generate_table()
        self.k_map = None

    def extract_variables(self, formula):
        return sorted(set(filter(str.isalpha, formula)))

    def calc(self, expr):
        precedence = {'not': 3, 'and': 2, 'or': 1, '==': 1, '<=': 1}
        output = []
        ops = []
        expr = expr.replace('(', ' ( ').replace(')', ' ) ')
        tokens = expr.split()

        for token in tokens:
            if token in ('0', '1'):
                output.append(int(token))
            elif token in precedence:
                while ops and ops[-1] != '(' and precedence.get(ops[-1], 0) >= precedence[token]:
                    output.append(ops.pop())
                ops.append(token)
            elif token == '(':
                ops.append(token)
            elif token == ')':
                while ops and ops[-1] != '(':
                    output.append(ops.pop())
                ops.pop()
            else:
                output.append(token)

        while ops:
            output.append(ops.pop())

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

    def evaluate(self, values):
        expr = self.formula
        env = {var: val for var, val in zip(self.variables, values)}
        expr = expr.replace('(', ' ( ').replace(')', ' ) ')
        expr = (expr.replace('!', ' not ')
                    .replace('¬', ' not ')
                    .replace('&', ' and ')
                    .replace('∧', ' and ')
                    .replace('^', ' and ')
                    .replace('|', ' or ')
                    .replace('∨', ' or ')
                    .replace('->', ' <= ')
                    .replace('→', ' <= ')
                    .replace('~', ' == '))
        tokens = expr.split()
        tokens = [str(env[token]) if token in env else token for token in tokens]
        expr = ' '.join(tokens)
        return self.calc(expr)

    def generate_table(self):
        return [(values, self.evaluate(values)) for values in itertools.product([0, 1], repeat=len(self.variables))]

    def display_table(self):
        header = " | ".join(self.variables) + " | Result"
        print("\nТаблица истинности:")
        print(header)
        print("-" * len(header))
        for values, result in self.table:
            row = " | ".join(map(str, values)) + " | " + str(result)
            print(row)




    def generate_karnaugh_map(self):
        n = len(self.variables)
        if n > 5:
            print("Карта Карно поддерживает до 5 переменных.")
            return

        def gray_code(bits):
            if bits == 1:
                return [0, 1]
            elif bits == 2:
                return [0, 1, 3, 2]
            elif bits == 3:
                return [0, 1, 3, 2, 6, 7, 5, 4]
            return []

        print(f"Переменные: {self.variables}")

        if n == 1:
            rows, cols = 1, 2
            row_vars, col_vars = 0, 1
        elif n == 2:
            rows, cols = 2, 2
            row_vars, col_vars = 1, 1
        elif n == 3:
            rows, cols = 2, 4
            row_vars, col_vars = 1, 2
        elif n == 4:
            rows, cols = 4, 4
            row_vars, col_vars = 2, 2
        elif n == 5:
            rows, cols = 4, 8
            row_vars, col_vars = 2, 3

        self.k_map = [[0 for _ in range(cols)] for _ in range(rows)]
        gray_rows = gray_code(row_vars)
        gray_cols = gray_code(col_vars)

        gray_to_idx = {g: i for i, g in enumerate(gray_cols)}

        for values, result in self.table:
            if n == 1:
                col = values[0]
                self.k_map[0][col] = result
            elif n == 2:
                row, col = values
                row_idx = gray_rows[row]
                col_idx = gray_cols[col]
                self.k_map[row_idx][col_idx] = result
            elif n == 3:
                a, b, c = values
                row_idx = gray_rows[a]
                col_idx = gray_cols[b * 2 + c]
                self.k_map[row_idx][col_idx] = result
            elif n == 4:
                a, b, c, d = values
                row_idx = gray_rows[a * 2 + b]
                col_idx = gray_cols[c * 2 + d]
                self.k_map[row_idx][col_idx] = result
            elif n == 5:
                a, b, c, d, e = values
                row_idx = gray_rows[a * 2 + b]
                raw_idx = c * 4 + d * 2 + e
                col_idx = gray_to_idx[raw_idx]
                print(f"Values: {values}, Row_idx: {row_idx}, Col_idx: {col_idx}, Result: {result}")
                self.k_map[row_idx][col_idx] = result

        print(f"\nКарта Карно ({n} переменных):")
        if n == 1:
            print("    " + "  ".join(f"{bin(g)[2:].zfill(1)}" for g in gray_cols))
            print(f"  | " + " | ".join(str(self.k_map[0][j]) for j in range(cols)))
        else:
            col_label = self.variables[2:n] if n == 5 else self.variables[n - row_vars:n]
            print(f"col_label: {col_label}")
            print(f"{''.join(self.variables[:row_vars])} \\ {''.join(col_label)}  " + "  ".join(
                f"{bin(g)[2:].zfill(col_vars)}" for g in gray_cols))
            for i in range(rows):
                label = bin(gray_rows[i])[2:].zfill(row_vars) if row_vars > 0 else ""
                row = f"{label}      " + "  ".join(str(self.k_map[i][j]) for j in range(cols))
                print(row)

    def find_sdnf(self):
        if self.k_map is None:
            self.generate_karnaugh_map()
        n = len(self.variables)
        if not (2 <= n <= 5):
            print("Минимизация СДНФ поддерживается только для 2–5 переменных.")
            return ""



        var_syms = symbols(self.variables)
        minterms = []

        row_vars = self.variables[:(n // 2)]
        col_vars = self.variables[(n // 2):]
        row_bits = len(row_vars)
        col_bits = len(col_vars)

        gray_rows = [0, 1, 3, 2] if row_bits == 2 else ([0, 1] if row_bits == 1 else [0, 1, 3, 2, 6, 7, 5, 4])
        gray_cols = [0, 1, 3, 2] if col_bits == 2 else ([0, 1] if col_bits == 1 else [0, 1, 3, 2, 6, 7, 5, 4])

        for i, gr in enumerate(gray_rows):
            for j, gc in enumerate(gray_cols):
                if self.k_map[i][j] == 1:
                    row_bits_vals = [(gr >> (row_bits - k - 1)) & 1 for k in range(row_bits)]
                    col_bits_vals = [(gc >> (col_bits - k - 1)) & 1 for k in range(col_bits)]
                    minterms.append(row_bits_vals + col_bits_vals)

        expr = SOPform(var_syms, minterms)
        result = str(expr).replace('~', '!')
        print("\nМинимизированная СДНФ:")
        print(result)
        return result




    def find_sknf(self):
        if self.k_map is None:
            self.generate_karnaugh_map()
        n = len(self.variables)
        if not (2 <= n <= 5):
            return ""

        rows, cols = len(self.k_map), len(self.k_map[0])
        gray_rows = [0, 1, 3, 2] if n >= 4 else ([0, 1] if n == 2 or n == 3 else [0])
        gray_cols = [0, 1, 3, 2, 6, 7, 5, 4] if n == 5 else ([0, 1, 3, 2] if n >= 3 else [0, 1])
        implicants = []

        # Поиск групп нулей (ограничиваем размер групп до 8 ячеек)
        for i in range(rows):
            for j in range(cols):
                if self.k_map[i][j] == 0:
                    for h in [1, 2, 4][:rows]:
                        for w in [1, 2, 4, 8][:cols]:
                            if h * w > 8:
                                continue
                            if h > rows or w > cols:
                                continue
                            valid = True
                            cells = []
                            for r in range(i, i + h):
                                for c in range(j, j + w):
                                    r_wrap = r % rows
                                    c_wrap = c % cols
                                    if self.k_map[r_wrap][c_wrap] != 0:
                                        valid = False
                                        break
                                    cells.append((r_wrap, c_wrap))
                                if not valid:
                                    break
                            if valid and cells:
                                implicants.append(cells)

        implicants = sorted([list(set(cells)) for cells in implicants], key=len, reverse=True)

        # Поиск основных импликант
        zeros = [(i, j) for i in range(rows) for j in range(cols) if self.k_map[i][j] == 0]
        essential_implicants = []
        covered = set()
        terms = []

        for cell in zeros:
            cell_implicants = [imp for imp in implicants if cell in imp]
            if len(cell_implicants) == 1:
                imp = cell_implicants[0]
                if imp not in essential_implicants:
                    essential_implicants.append(imp)
                    covered.update(imp)
                    row_indices = set(r for r, _ in imp)
                    col_indices = set(c for _, c in imp)
                    row_bits = [bin(gray_rows[r])[2:].zfill(len(self.variables[:(n // 2)])) for r in row_indices]
                    col_bits = [bin(gray_cols[c])[2:].zfill(len(self.variables[(n // 2):])) for c in col_indices]
                    bit_sets = [set(rb[i] for rb in row_bits) for i in range(len(row_bits[0]))] + \
                               [set(cb[i] for cb in col_bits) for i in range(len(col_bits[0]))]
                    term = []
                    for i, bits in enumerate(bit_sets):
                        if len(bits) == 1:
                            var = self.variables[i]
                            val = bits.pop()
                            term.append(f"!{var}" if val == '1' else var)
                    if term:
                        terms.append('(' + ' | '.join(term) + ')')

        # Фильтрация импликант с проверкой конфликтов
        filtered_implicants = essential_implicants[:]
        remaining_zeros = set(zeros) - covered
        used_variables = set(var for term in terms for var in term if var.startswith('!') or var.isalpha())

        while remaining_zeros:
            best_implicant = None
            max_coverage = 0
            best_score = 0
            best_term = None
            for imp in implicants:
                if imp not in filtered_implicants:
                    coverage = len(set(imp) & remaining_zeros)
                    row_indices = set(r for r, _ in imp)
                    col_indices = set(c for _, c in imp)
                    row_bits = [bin(gray_rows[r])[2:].zfill(len(self.variables[:(n // 2)])) for r in row_indices]
                    col_bits = [bin(gray_cols[c])[2:].zfill(len(self.variables[(n // 2):])) for c in col_indices]
                    bit_sets = [set(rb[i] for rb in row_bits) for i in range(len(row_bits[0]))] + \
                               [set(cb[i] for cb in col_bits) for i in range(len(col_bits[0]))]
                    num_vars = sum(1 for s in bit_sets if len(s) == 1)
                    term = []
                    term_vars = set()
                    for i, bits in enumerate(bit_sets):
                        if len(bits) == 1:
                            var = self.variables[i]
                            val = bits.pop()
                            term.append(f"!{var}" if val == '1' else var)
                            term_vars.add(var)
                    conflict = False
                    for var in term_vars:
                        if var in used_variables and any(f"!{var}" in t or var in t for t in terms):
                            conflict = True
                            break
                    score = coverage * 1000 - num_vars * 200
                    if coverage > 0 and not conflict and (
                            coverage > max_coverage or (coverage == max_coverage and score > best_score)):
                        max_coverage = coverage
                        best_implicant = imp
                        best_score = score
                        best_term = term

            if best_implicant and best_term:
                filtered_implicants.append(best_implicant)
                covered.update(best_implicant)
                remaining_zeros -= set(best_implicant)
                used_variables.update(var for var in best_term if var.startswith('!') or var.isalpha())
                terms.append('(' + ' | '.join(best_term) + ')')

        # Подготовка таблицы для minimize_sknf_quine_mccluskey
        table = []
        for i in range(rows):
            for j in range(cols):
                # Формируем значения переменных на основе gray_rows и gray_cols
                row_bits = bin(gray_rows[i])[2:].zfill(len(self.variables[:(n // 2)]))
                col_bits = bin(gray_cols[j])[2:].zfill(len(self.variables[(n // 2):]))
                vals = list(row_bits + col_bits)
                vals = [int(v) for v in vals]
                res = self.k_map[i][j]
                table.append((vals, res))

        # Вызов функции минимизации
        result = " & ".join(terms) if terms else "1"













