while True:
    try:
        x = float(input("What's x? "))
        y = float(input("What's y? "))

    except ValueError:
        print("Write a number dude!")

    else:
        if x != y:
            print("x is not equal to y")
        else:
            print("x is equal to y")
        break
