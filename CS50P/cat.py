"""i = 0
while i < 3:
    i += 1
    print("Meow")"""

"""for _ in range(3):
    print("Meow")"""

"""print("Meow\n" * 3, end="")"""


def main():
    number = get_number()
    meow(number)


def get_number():
    while True:
        try:
            n = int(input("What's n? "))
            if n > 0:
                return n
        except ValueError:
            print("Write a number dude!")


def meow(n):
    for _ in range(n):
        print("Meow")


main()
