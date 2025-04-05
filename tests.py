import unittest
from io import StringIO
from contextlib import redirect_stdout
from table import Logicformula  # Предположим, твой код в файле main.py

class TestLogicFormula(unittest.TestCase):

    def test_isvlech(self):
        lf = Logicformula("A and B or not C")
        self.assertEqual(lf.variables, ['A', 'B', 'C', 'a', 'd', 'n', 'o', 'r', 't'])

    def test_eval_true(self):
        lf = Logicformula("A ∧ B")
        result = lf.evalu((1, 1))
        self.assertEqual(result, 1)

    def test_eval_false(self):
        lf = Logicformula("A ∧ B")
        result = lf.evalu((1, 0))
        self.assertEqual(result, 0)

    def test_truth_table_len(self):
        lf = Logicformula("A ∧ B")
        self.assertEqual(len(lf.table), 4)

    def test_sdnf_indices(self):
        lf = Logicformula("A ∨ B")
        output = StringIO()
        with redirect_stdout(output):
            lf.get_sdnf()
        result = output.getvalue()
        self.assertIn("(1, 2, 3) ∨", result)

    def test_sknf_indices(self):
        lf = Logicformula("A ∧ B")
        output = StringIO()
        with redirect_stdout(output):
            lf.get_sknf()
        result = output.getvalue()
        self.assertIn("(0, 1, 2)", result)

    def test_calc_expression(self):
        lf = Logicformula("A → B")
        result = lf.evalu((1, 0))
        self.assertEqual(result, 0)

    def test_binary_to_decimal(self):
        lf = Logicformula("A")
        self.assertEqual(lf.binary_to_decimal("1011"), 11)

if __name__ == "__main__":
    unittest.main()
