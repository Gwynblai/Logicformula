import re

class BooleanMinimizer:
    @staticmethod
    def __evaluate(logic_expr, inputs):
        expr = re.sub(r'!([a-zA-Z]\d?)', lambda m: f'not {inputs.get(m.group(1), 0)}', logic_expr)
        expr = re.sub(r'\b([a-zA-Z]\d?)\b', lambda m: str(inputs.get(m.group(1), 0)), expr)
        expr = expr.replace('&', ' and ').replace('|', ' or ')
        try:
            return int(eval(expr))
        except Exception as ex:
            raise ValueError(f"Ошибка при обработке выражения: {expr}") from ex

    @staticmethod
    def __extract_values(term, connector):
        result = {}
        target = 0 if connector == '|' else 1
        parts = term.split(connector)
        for p in parts:
            p = p.strip()
            if p.startswith('!'):
                result[p[1:]] = not target
            else:
                result[p] = target
        return result

    @staticmethod
    def minimize_sdnf_by_table(formula):
        implicants = BooleanMinimizer.__table_simplify(formula, '&')
        return ' | '.join(f"({imp})" for imp in implicants)

    @staticmethod
    def minimize_sknf_by_table(formula):
        implicants = BooleanMinimizer.__table_simplify(formula, '|')
        return ' & '.join(f"({imp})" for imp in implicants)

    @staticmethod
    def minimize_sdnf(formula):
        implicants = BooleanMinimizer.__process_minimization(formula, '&')
        return ' | '.join(f"({imp})" for imp in implicants)

    @staticmethod
    def minimize_sknf(formula):
        implicants = BooleanMinimizer.__process_minimization(formula, '|')
        return ' & '.join(f"({imp})" for imp in implicants)

    @staticmethod
    def __process_minimization(formula, connector):
        terms = BooleanMinimizer.__split_terms(formula)
        if not terms:
            print("Ошибка: не удалось получить конституенты.")
            return

        reduced = terms.copy()
        while True:
            next_step = BooleanMinimizer.__combine_terms(
                connector.join(f"({t})" for t in reduced), connector)
            next_step = sorted(set(next_step))

            if set(next_step) == set(reduced):
                break
            reduced = next_step

        essential = []
        for term in reduced:
            input_values = BooleanMinimizer.__extract_values(term, connector)
            if (connector == '&' and BooleanMinimizer.__evaluate(formula, input_values) == 1) or \
               (connector == '|' and BooleanMinimizer.__evaluate(formula, input_values) == 0):
                essential.append(term)
        return essential

    @staticmethod
    def __table_simplify(formula, connector):
        terms = BooleanMinimizer.__split_terms(formula)
        if not terms:
            print("Ошибка: не удалось получить конституенты.")
            return

        print("Полученные конституенты:", terms)

        reduced = terms.copy()
        while True:
            glued = BooleanMinimizer.__combine_terms(connector.join(f"({t})" for t in reduced), connector)
            glued = sorted(set(glued))
            if set(glued) == set(reduced):
                break
            reduced = glued

        print("Импликанты после склейки:", reduced)

        imp_parts = {imp: set(x.strip() for x in imp.split(connector)) for imp in reduced}
        term_parts = {term: set(x.strip() for x in term.split(connector)) for term in terms}

        result = BooleanMinimizer.__build_coverage_table(reduced, imp_parts, term_parts)
        return result

    @staticmethod
    def __split_terms(expression):
        terms = []
        if BooleanMinimizer.__check_parentheses(expression):
            current = ''
            depth = 0
            for char in expression:
                if char == '(':
                    if depth > 0:
                        current += char
                    depth += 1
                elif char == ')':
                    depth -= 1
                    if depth == 0:
                        terms.append(current)
                        current = ''
                    else:
                        current += char
                else:
                    if depth > 0:
                        current += char
        else:
            print("Ошибка: неверная структура скобок")
        return terms

    @staticmethod
    def __check_parentheses(expression):
        depth = 0
        for char in expression:
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            if depth < 0:
                return False
        return depth == 0

    @staticmethod
    def __combine_terms(expression, connector):
        items = BooleanMinimizer.__split_terms(expression)
        result = []
        used_indices = set()

        for i in range(len(items)):
            for j in range(len(items)):
                if i == j:
                    continue

                lhs = [x.strip() for x in items[i].split(connector)]
                rhs = [x.strip() for x in items[j].split(connector)]

                common = set(lhs) & set(rhs)
                diff = set(lhs) ^ set(rhs)

                if len(common) == len(lhs) - 1 and len(diff) == 2:
                    d1, d2 = diff
                    if d1.lstrip('!') == d2.lstrip('!') and (d1.startswith('!') ^ d2.startswith('!')):
                        used_indices.update({i, j})
                        combined = connector.join(sorted(common))
                        if combined not in result and combined:
                            result.append(combined)

        for idx, original in enumerate(items):
            if idx not in used_indices:
                cleaned = connector.join(sorted([x.strip() for x in original.split(connector)]))
                if cleaned not in result and cleaned:
                    result.append(cleaned)

        return result

    @staticmethod
    def __build_coverage_table(implicants, imp_parts, term_parts):
        coverage = {imp: [] for imp in implicants}

        for imp, ilits in imp_parts.items():
            for term, tlits in term_parts.items():
                if ilits.issubset(tlits):
                    coverage[imp].append(term)

        print("\nТаблица покрытия:")
        header = [" " * 15] + list(term_parts.keys())
        print("".join(col.center(18) for col in header))
        for imp in implicants:
            row = [imp.ljust(15)]
            for term in term_parts:
                row.append("+" if term in coverage[imp] else " ")
            print("".join(cell.center(18) for cell in row))

        essential = []
        for imp, covered in coverage.items():
            other_covered = set()
            for other_imp, others in coverage.items():
                if other_imp != imp:
                    other_covered.update(others)
            if not set(covered).issubset(other_covered):
                essential.append(imp)

        return essential
