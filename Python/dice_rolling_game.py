"""Dice Rolling Game"""
import random
# Welcome Message
separator = "==========================="
print(separator, "\n")
print("Hello! Welcome to my Dice Rolling Game!\n")
print(separator, "\n")

list = ("0", "1", "3", "4", "5", "6", "7", "8", "9")
list_two = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
random_value = random.choice(list)
random_value_two = random.choice(list_two)

# Asking the User Input
choice = str(input("Roll the Dice? (Y/N) -> ").strip().upper())

# Process
if choice == "Y":
    print("[" + random_value + "," + random_value_two + "]\n")
elif choice == "N":
    exit()
else:
    print("ERROR: Write Y or N!!!")
    


