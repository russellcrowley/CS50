# Get a positive float as input
amount = 0
while amount <= 0:
    try:
        amount = float(input("Change owed: "))
    except ValueError:
        continue
# convert amount to cents
amount = round(amount, 2) * 100
coin_count = 0
# Try and subtract coins from amount, largest first
while amount > 0:
    # quarter
    if amount >= 25:
        amount -= 25
        coin_count += 1
    # nickel
    elif amount >= 10:
        amount -= 10
        coin_count += 1
    # dime
    elif amount >= 5:
        amount -= 5
        coin_count += 1
    # last must be cent
    else:
        amount -= 1
        coin_count += 1

print(coin_count)
