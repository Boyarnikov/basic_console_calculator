import unittest
import calculator

import subprocess
import sys

class TestTokenizer(unittest.TestCase):
    def test_tokenizer_valid_expression_1(self):
        # given
        string_expression = "2 + 2"

        # when
        tokens = calculator.tokenize(string_expression)

        # then
        self.assertEqual(tokens, ["2", "+", "2"])


    def test_tokenizer_valid_expression_2(self):
        self.assertEqual(calculator.tokenize("2*2"), ["2", "*", "2"])


    def test_tokenizer_valid_expressions(self):
        test_cases = [
            ("6 * 7", ["6", "*", "7"]),
            ("7 + (3*6)", ["7", "+", "(", "3", "*", "6", ")"]),
            ("6000", ["6000"]),
        ]

        for expression, tokens in test_cases:
            with self.subTest(expression = expression):
                self.assertEqual(calculator.tokenize(expression), tokens)


    def test_tokenizer_invalid_expressions(self):
        test_cases = [
            "6 * 7 :",
            "!7 + (3*6)",
            "6000&",
            "6+$9",
        ]

        for expression in test_cases:
            with self.subTest(expression = expression):
                with self.assertRaises(ValueError) as cm:
                    calculator.tokenize(expression)


#calc_var
#calc_factor
#calc_expression
# ^^ HW


class TestCli(unittest.TestCase):
    def test_cli_valid_expressions(self):
        test_cases = [
            ("2+2", 4),
            ("6 + 6 * 2", 18),
            ("      2      +    ---2", 0),
            ("5 / (2 / 4)", 10),
            ("3*3+3", 12),
            ("9*9", 81)
        ]

        for expression, result in test_cases:
            with self.subTest(expression = expression):
                cli_result = subprocess.run([sys.executable, 'calculator.py', expression], capture_output=True, text=True)
                self.assertIn(f"Result: {float(result)}", cli_result.stdout)

    def test_cli_invalid_expressions(self):
        test_cases = [
            "2+",
            "* 2",
            "+2",
            "(2 / 4",
            "3^34"
        ]

        for expression in test_cases:
            with self.subTest(expression = expression):
                cli_result = subprocess.run([sys.executable, 'calculator.py', expression], capture_output=True, text=True)
                self.assertEqual(cli_result.returncode, 1)

    def test_cli_zero_division(self):
        test_cases = [
            "5/0",
        ]

        for expression in test_cases:
            with self.subTest(expression = expression):
                cli_result = subprocess.run([sys.executable, 'calculator.py', expression], capture_output=True, text=True)
                self.assertIn("Zero division", cli_result.stderr)
                self.assertEqual(cli_result.returncode, 1)