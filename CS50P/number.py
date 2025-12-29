try:
    x = float(input("What's x? "))
    print(f"x is {x}")
except ValueError:
    print("x isn't a number.")
