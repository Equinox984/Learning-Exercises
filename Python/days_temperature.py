"""Days Temperature"""

# Welcome Message
separator = "============================"
print(separator)
print("Hello! Welcome to Days Temperature Program!")
print(separator, "\n")

# Creating the List of Temperatures
temperatures = [22.5, 18.0, 25.5, 20.0, 28.5, 17.5, 21.0]
lowest_temperature = temperatures[0]

for temperature in temperatures:
    if temperature < lowest_temperature:
        lowest_temperature = temperature

print(f"The lowest temperature is: {lowest_temperature}")

print(temperatures[::2])
