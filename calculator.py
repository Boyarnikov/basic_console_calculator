import argparse
import string
import sys

""" 
expression 1234 - (5 * 6) / 7 - 8 * (-9) 
term [ ] + [ ] - [ ] + [ ]
factor [ ] * [ ] / [ ] * [ ]
var (...), 135, -12


1234 - (5 * 6) / 7 - 8 * (-9) 

[12*34] - [(5 * 6) / 7] - [8 * -9]


23*45
"""

def calc_var(tokens) -> float:
    if not tokens:
        raise ValueError("Cannot calculate None")

    token = tokens.pop(0)

    if token == "(":
        result = calc_expression(tokens)
        if not tokens or not tokens[0] == ")":
            raise ValueError("Unmatched '('")
        tokens.pop(0)
        return result

    if token == "-":
        return -calc_expression(tokens)

    try:
        return float(token)
    except ValueError:
        raise ValueError(f"Expected number, got {token}")


def calc_factor(tokens) -> float:
    if not tokens:
        raise ValueError("Cannot calculate None")

    left = calc_var(tokens)

    while tokens and tokens[0] in ["*", "/"]:
        operation = tokens.pop(0)
        right = calc_var(tokens)
        if operation == "*":
            left *= right
        elif operation == "/":
            if right == 0:
                raise ZeroDivisionError(f"Zero division while calculating {left}/{right}")
            left /= right

    return left


def calc_expression(tokens) -> float:
    if not tokens:
        raise ValueError("Cannot calculate None")

    left = calc_factor(tokens)

    while tokens and tokens[0] in ["+", "-"]:
        operation = tokens.pop(0)
        right = calc_factor(tokens)
        if operation == "+":
            left += right
        elif operation == "-":
            left -= right

    return left


def tokenize(expression: str) -> list:
    tokens = []
    token = ''

    for c in expression:
        if c in "()+-*/":
            if token:
                tokens.append(token)
            tokens.append(c)
            token = ""
        elif c in string.digits:
            token+=c
        elif c.isspace():
            if token:
                tokens.append(token)
                token = ""
        else:
            raise ValueError(f"Unexpected character {c}")

    if token:
        tokens.append(token)
    return tokens


def main():
    parser = argparse.ArgumentParser(description="Basic CLI calculator")
    parser.add_argument("expression", type=str, help="expression string to be calculated")

    args = parser.parse_args()

    try:
        tokens = tokenize(args.expression)
        result = calc_expression(tokens)
        print(f"Result: {result}")
    except Exception as e:
        sys.stderr.write(f"Error while calculating: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()