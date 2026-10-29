import json
import os

from product import Product
from inventory import Inventory


def load_inventory():
    inventory = Inventory()

    if os.path.exists("inventory.json"):
        file = open("inventory.json", "r")
        data = json.load(file)
        file.close()

        for item in data:
            product = Product(item["id"], item["name"], item["price"], item["stock"])
            inventory.add_product(product)

        print("inventory.json found.")
        print("Inventory loaded successfully.")
    else:
        print("No inventory.json found. Starting with empty inventory.")

    return inventory


def save_inventory(inventory):
    data = []

    for product in inventory.get_products():
        data.append(product.to_dict())

    file = open("inventory.json", "w")
    json.dump(data, file, indent=4)
    file.close()
    print("Inventory saved successfully to inventory.json.")


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
            new_product = Product(product_id, product_name, price, stock)

            if inventory.add_product(new_product):
                print("Product added successfully!")
            else:
                print("Product ID already exists.")

    except ValueError:
        print("Please enter a valid price and stock quantity.")


def update_stock(inventory):
    print("Update Stock")
    product_id = input("Enter Product ID: ")

    product = inventory.search_product(product_id)

    if product == None:
        print("Product not found.")
    else:
        print("Product Found:")
        print("Name:", product.get_name())
        print("Current Stock:", product.get_stock())

        new_stock = input("New Stock Quantity: ")

        try:
            new_stock = int(new_stock)

            if product.update_stock(new_stock):
                print("Stock updated successfully!")
            else:
                print("Stock cannot be negative.")

        except ValueError:
            print("Please enter a valid whole number.")


def search_product(inventory):
    print("Search Product")
    product_id = input("Enter Product ID: ")

    product = inventory.search_product(product_id)

    if product == None:
        print("Product not found.")
    else:
        print("Product Found")
        print("-" * 48)
        product.display_information()
        print("-" * 48)


inventory = load_inventory()

while True:
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")

    option = input("Enter option: ")

    if option == "1":
        inventory.display_all()

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