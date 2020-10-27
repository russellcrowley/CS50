height = 0
# loop to ensure input between 1 nd 8
while (height < 1) or (height > 8):
    try:
        height = int(input("Height: "))
    except ValueError:
        print("Input must be a whole number between 1 and 8")
    # construct the pyramid, row by row
for i in range(1, height + 1):
    print((" " * (height - i)) + ("#" * i) + "  " + ("#" * i))

