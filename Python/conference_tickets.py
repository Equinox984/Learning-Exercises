"""Equinox Conference Tickets"""

separator = "==============================="
print(separator)
print("Hello! Welcome to Equinox Conference Tickets!")
print(separator, "\n")

Registration_Type = int(
    input("Please select your registration type (1 - Early Bird / 2 - Regular): \n"))
Role = int(
    input("Please select your role (1 - Student / 2 - Developer / 3 - Speaker): \n"))

if Registration_Type == 1:
    if Role == 1:
        print("Your ticket costs 50$")
    elif Role == 2:
        print("Your ticket costs 350$")
    elif Role == 3:
        print("Your ticket is free!")
    else:
        print("Invalid role. Please try again.")

elif Registration_Type == 2:
    if Role == 1:
        print("Your ticket costs 75$")
    elif Role == 2:
        print("Your ticket costs 499$")
    elif Role == 3:
        print("Your ticket is free!")

else:
    print("Invalid registration type or role. Please try again.")
