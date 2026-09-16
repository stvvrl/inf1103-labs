inventory = 0
rejected_entries = 0

while True:
    quantity = input("Stock quantity: ")

    if quantity == "quit":
        break

    if not quantity.isdigit():
        print("Invalid input")
        rejected_entries += 1
        continue

    quantity = int(quantity)
    inventory += quantity

    if inventory > 500:
        print("Overstock Alert!")
        break

print("Total Inventory:", inventory)
print("Number of Rejected Entries:", rejected_entries)