import argparse

operations = {
    "add": lambda x, y: x+y,
    "sub": lambda x, y: x-y,
    'mult': lambda x, y: x*y,
    "div": lambda x, y: x/y,
}


# main.py add 5 2 -> 7
# main.py sub 20 50 -> -30


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Basic calculator"
    )

    parser.add_argument("operation", type=str, choices=operations.keys())
    parser.add_argument("num1", type=float)
    parser.add_argument("num2", type=float)

    #args = parser.parse_args()

    args = parser.parse_args(["div", "40", "10"])

    try:
        function = operations[args.operation]
        result = function(args.num1, args.num2)
        print(result)
    except ValueError as e:
        print(f"Error: {e}")
    except ZeroDivisionError:
        print("Error: zero devision detected")
