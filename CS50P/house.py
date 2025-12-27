name = str(input("What's your name? -> ").strip().title())
gryffindor = ["Harry", "Hermione", "Ron"]
slytherin = ["Draco"]

if name in gryffindor:
    print("Gryffindor")
elif name in slytherin:
    print("Slytherin")
else:
    print("Who?")
