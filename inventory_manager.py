import json
import os

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory

DATA_FILE: str = "inventory.json"

def create_product_from_dict(item: dict, suppliers: dict[str, Supplier]) -> Product | None:
    supplier = suppliers.get(item.get("supplier_id"))
    if supplier is None:
        return None

    product_type = item.get("type")

    if product_type == "physical":
        return PhysicalProduct(item["id"], item["name"], item["price"], item["stock"],
                               supplier, item["weight"])
    elif product_type == "digital":
        return DigitalProduct(item["id"], item["name"], item["price"], item["stock"],
                              supplier, item["download_size"])
    return None


def load_inventory() -> Inventory:
    inventory = Inventory()

    if os.path.exists(DATA_FILE):
        file = open(DATA_FILE, "r")
        data = json.load(file)
        file.close()

        suppliers: dict[str, Supplier] = {}
        for s in data.get("suppliers", []):
            suppliers[s["id"]] = Supplier(s["id"], s["name"], s["contact_email"])

        for item in data.get("products", []):
            product = create_product_from_dict(item, suppliers)
            if product is None:
                print("Skipping product with unknown type or supplier:", item.get("id"))
            else:
                inventory.add_product(product)

        print("inventory.json found.")
        print("Inventory loaded successfully.")
    else:
        print("No inventory.json found. Starting with empty inventory.")

    return inventory


def save_inventory(inventory: Inventory) -> None:
    products_data: list[dict] = []
    suppliers_data: dict[str, dict] = {}

    for product in inventory.get_products():
        products_data.append(product.to_dict())
        supplier = product.get_supplier()
        suppliers_data[supplier.get_supplier_id()] = {
            "id": supplier.get_supplier_id(),
            "name": supplier.get_name(),
            "contact_email": supplier.get_contact_email()
        }

    data = {"suppliers": list(suppliers_data.values()), "products": products_data}

    file = open(DATA_FILE, "w")
    json.dump(data, file, indent=4)
    file.close()
    print("Inventory saved successfully to inventory.json.")


def find_supplier(inventory: Inventory, supplier_id: str) -> Supplier | None:
    for product in inventory.get_products():
        if product.get_supplier().get_supplier_id() == supplier_id:
            return product.get_supplier()
    return None


def ask_for_supplier(inventory: Inventory) -> Supplier | None:
    supplier_id = input("Supplier ID: ")
    supplier = find_supplier(inventory, supplier_id)

    if supplier is not None:
        print("Existing supplier found:", supplier.get_name())
        return supplier

    print("New supplier. Please enter details.")
    name = input("Supplier Name: ")
    email = input("Supplier Contact Email: ")
    if supplier_id == "" or name == "":
        print("Supplier ID and name cannot be empty.")
        return None
    return Supplier(supplier_id, name, email)


def add_product(inventory: Inventory) -> None:
    print("Add New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    product_type = input("Choose product type: ")

    if product_type != "1" and product_type != "2":
        print("Invalid product type. Please enter 1 or 2.")
        return

    product_id = input("Product ID: ")
    product_name = input("Product Name: ")
    price = input("Price: ")
    stock = input("Stock Quantity: ")

    if product_type == "1":
        extra = input("Weight (kg): ")
    else:
        extra = input("Download Size (MB): ")

    supplier = ask_for_supplier(inventory)
    if supplier is None:
        return

    try:
        price = float(price)
        stock = int(stock)
        extra = float(extra)

        if price < 0 or stock < 0 or extra < 0:
            print("Price, stock and weight/download size cannot be negative.")
        else:
            if product_type == "1":
                new_product: Product = PhysicalProduct(product_id, product_name, price, stock, supplier, extra)
            else:
                new_product = DigitalProduct(product_id, product_name, price, stock, supplier, extra)

            if inventory.add_product(new_product):
                print("Product added successfully!")
            else:
                print("Product ID already exists.")

    except ValueError:
        print("Please enter valid numbers for price, stock and weight/download size.")


def update_stock(inventory: Inventory) -> None:
    print("Update Stock")
    product_id = input("Enter Product ID: ")

    product = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
    else:
        print("Product Found:")
        print("Name:", product.get_name())
        print("Current Stock:", product.get_stock())

        new_stock = input("New Stock Quantity: ")

        try:
            if product.update_stock(int(new_stock)):
                print("Stock updated successfully!")
            else:
                print("Stock cannot be negative.")

        except ValueError:
            print("Please enter a valid whole number.")


def search_product(inventory: Inventory) -> None:
    print("Search Product")
    product_id = input("Enter Product ID: ")

    product = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
    else:
        print("Product Found")
        print("-" * 48)
        product.display_information()
        print("Fulfilment:", product.get_fulfilment_info())
        print("-" * 48)


def main() -> None:
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


if __name__ == "__main__":
    main()