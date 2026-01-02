def main():
    x = get_int("What's x? ")
    print(f"x is {x}\n")


def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            pass  # We catch the error but we don't do anything about it.
            # We just stay in the loop


main()
