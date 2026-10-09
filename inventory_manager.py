import json
import os


def load_inventory():
    if os.path.exists("inventory.json"):
        file = open("inventory.json", "r")
        inventory = json.load(file)
        file.close()
        print("inventory.json found.")
        print("Inventory loaded successfully.")
        return inventory
    else:
        print("No inventory.json found. Starting with empty inventory.")
        return []


def save_inventory(inventory):
    file = open("inventory.json", "w")
    json.dump(inventory, file, indent=4)
    file.close()
    print("Inventory saved successfully to inventory.json.")


def display_all(inventory):
    if len(inventory) == 0:
        print("No products in inventory.")
    else:
        print("Current Inventory")
        print("-" * 48)

        for product in inventory:
            print("ID:", product["id"],
                  "| Name:", product["name"],
                  "| Price: $" + format(product["price"], ".2f"),
                  "| Stock:", product["stock"])

        print("-" * 48)


def add_product(inventory):
    print("Add New Product")

    product_id = input("Product ID: ")
    product_name = input("Product Name: ")

    price = input("Price: ")
    stock = input("Stock Quantity: ")

    try:
        price = float(price)
        stock = int(stock)

        if price < 0 or stock < 0:
            print("Price and stock cannot be negative.")
        else:
            found = False

            for product in inventory:
                if product["id"] == product_id:
                    found = True

            if found:
                print("Product ID already exists.")
            else:
                new_product = {
                    "id": product_id,
                    "name": product_name,
                    "price": price,
                    "stock": stock
                }

                inventory.append(new_product)
                print("Product added successfully!")

    except ValueError:
        print("Please enter a valid price and stock quantity.")


def update_stock(inventory):
    print("Update Stock")
    product_id = input("Enter Product ID: ")

    found = False

    for product in inventory:
        if product["id"] == product_id:
            found = True
            print("Product Found:")
            print("Name:", product["name"])
            print("Current Stock:", product["stock"])

            new_stock = input("New Stock Quantity: ")

            try:
                new_stock = int(new_stock)

                if new_stock < 0:
                    print("Stock cannot be negative.")
                else:
                    product["stock"] = new_stock
                    print("Stock updated successfully!")

            except ValueError:
                print("Please enter a valid whole number.")

    if not found:
        print("Product not found.")


def search_product(inventory):
    print("Search Product")
    product_id = input("Enter Product ID: ")

    found = False

    for product in inventory:
        if product["id"] == product_id:
            found = True
            print("Product Found")
            print("-" * 48)
            print("ID:", product["id"])
            print("Name:", product["name"])
            print("Price: $" + format(product["price"], ".2f"))
            print("Stock:", product["stock"])
            print("-" * 48)

    if not found:
        print("Product not found.")


inventory = load_inventory()

while True:
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")

    option = input("Enter option: ")

    if option == "1":
        display_all(inventory)

    elif option == "2":
        add_product(inventory)

    elif option == "3":
        update_stock(inventory)

    elif option == "4":
        search_product(inventory)

    elif option == "5":
        print("Saving inventory...")
        save_inventory(inventory)

    elif option == "6":
        print("Saving inventory before exit...")
        save_inventory(inventory)
        print("Thank you for using Inventory Management System.")
        print("Program terminated.")
        break

    else:
        print("Invalid option. Please enter 1 to 6.")