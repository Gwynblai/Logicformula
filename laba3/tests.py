
from table import *  # Предположим, твой код в файле main.py

import unittest

class TestLogicFormula(unittest.TestCase):

    def test_isvlech(self):
        lf = Logicformula("a & b | !c")
        self.assertEqual(lf.variables, ['a', 'b', 'c'])

    def test_evalu(self):
        lf = Logicformula("a & !b")
        self.assertEqual(lf.evalu([1, 0]), 1)
        self.assertEqual(lf.evalu([1, 1]), 0)

    def test_gener_table(self):
        lf = Logicformula("a & b")
        table = lf.gener_table()
        expected = [
            ((0, 0), 0),
            ((0, 1), 0),
            ((1, 0), 0),
            ((1, 1), 1),
        ]
        self.assertEqual(table, expected)

    def test_get_sdnf(self):
        lf = Logicformula("a & b")
        sdnf = lf.get_sdnf()
        self.assertEqual(sdnf, "(a & b)")

    def test_get_sknf(self):
        lf = Logicformula("a & b")
        sknf = lf.get_sknf()
        expected = "(a | b) & (a | !b) & (!a | b)"
        self.assertIn("(a | b)", sknf)
        self.assertIn("(!a | b)", sknf)
        self.assertIn("(a | !b)", sknf)

    def test_minimize_sdnf_quine_mccluskey(self):
        lf = Logicformula("a & b")
        result = minimize_sdnf_quine_mccluskey(lf.table, lf.variables)
        self.assertIn("a", result)
        self.assertIn("b", result)

    def test_minimize_sknf_quine_mccluskey(self):
        lf = Logicformula("a & b")
        result = minimize_sknf_quine_mccluskey(lf.table, lf.variables)
        self.assertIn("a", result)
        self.assertIn("b", result)


    def test_sdnf_constant_true(self):
        lf = Logicformula("1")
        result = minimize_sdnf_quine_mccluskey(lf.table, lf.variables)
        self.assertEqual(result, "1")

    def test_sdnf_single_variable(self):
        lf = Logicformula("a")
        result = minimize_sdnf_quine_mccluskey(lf.table, lf.variables)
        self.assertEqual(result, "a")

    def test_sdnf_negation(self):
        lf = Logicformula("!a")
        result = minimize_sdnf_quine_mccluskey(lf.table, lf.variables)
        self.assertEqual(result, "¬a")

    def test_sdnf_simple_and(self):
        lf = Logicformula("a & b")
        result = minimize_sdnf_quine_mccluskey(lf.table, lf.variables)
        # возможны разные порядки
        expected = {"a ∧ b", "b ∧ a"}
        self.assertIn(result, expected)

    def test_sdnf_complex_formula(self):
        lf = Logicformula("(a & b) | c")
        result = minimize_sdnf_quine_mccluskey(lf.table, lf.variables)
        self.assertTrue("c" in result or "a ∧ b" in result)



if __name__ == "__main__":
    unittest.main()

