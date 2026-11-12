"""
Lab 8 demonstration tests: association, aggregation, composition, LSP, polymorphism.

Run with:  python test_lab8.py
"""
from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order

def heading(text: str) -> None:
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def show_product_details(product: Product) -> None:
    """Works for ANY Product: no isinstance(), no subclass knowledge (LSP)."""
    product.display_information()
    print("Fulfilment:", product.get_fulfilment_info())


# Section 2
heading("2. ASSOCIATION: Supplier and Product")
supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
laptop = PhysicalProduct("P001", "Laptop", 3000.0, 10, supplier, 1.8)
app = DigitalProduct("D001", "Clip Studio Paint", 75.0, 999, supplier, 2120.0)

print("-- Supplier info through the physical product:")
laptop.get_supplier().display_information()
print("-- Supplier info through the digital product:")
app.get_supplier().display_information()

# PREDICT FIRST: what happens to the products after `del supplier`?
del supplier
print("-- After `del supplier`, through the products:")
laptop.get_supplier().display_information()
app.get_supplier().display_information()
assert laptop.get_supplier() is app.get_supplier()   # one shared Supplier object

# Section 3
heading("3. AGGREGATION: Inventory and Product")
mouse = PhysicalProduct("P002", "Mouse", 30.0, 50, laptop.get_supplier(), 0.1)  # exists first
inventory_a = Inventory()
inventory_b = Inventory()

inventory_a.add_product(mouse)
print("In A after add:", inventory_a.find_product("P002") is mouse)

# PREDICT FIRST: will `mouse` still work after removal from Inventory A?
removed = inventory_a.remove_product("P002")
print("Removed from A:", removed, "| still in A:", inventory_a.find_product("P002"))
mouse.display_row()                                   # product still usable
print("Mouse can still update stock:", mouse.update_stock(45), "->", mouse.get_stock())

inventory_b.add_product(mouse)
print("Same object now in B:", inventory_b.find_product("P002") is mouse)
assert inventory_a.find_product("P002") is None
assert inventory_b.find_product("P002") is mouse
assert inventory_a.remove_product("NOPE") is False

# Section 4
heading("4. COMPOSITION: Order and OrderLine")
order_1 = Order("O001")
order_2 = Order("O002")

# PREDICT FIRST: same Product in two Orders: how many OrderLines? how many Products?
order_1.add_order_line(laptop, 1)
order_1.add_order_line(app, 2)
order_2.add_order_line(laptop, 3)

order_1.display_information()
order_2.display_information()

line_1 = order_1.get_order_lines()[0]
line_2 = order_2.get_order_lines()[0]
print("Different OrderLine objects:", line_1 is not line_2)
print("Same Product object:", line_1.get_product() is line_2.get_product())
assert line_1 is not line_2
assert line_1.get_product() is line_2.get_product()
assert order_1.calculate_total() == 3000.0 + 2 * 75.0
assert order_2.calculate_total() == 3 * 3000.0

print("Remove laptop line from order_1:", order_1.remove_order_line("P001"))
print("Laptop (Product) still exists:", laptop.get_name())
assert len(order_1.get_order_lines()) == 1
assert order_1.remove_order_line("P001") is False

# Section 6
heading("6. LSP: Product can be substituted by either subclass")
for p in (laptop, app):
    show_product_details(p)
    print("-" * 40)

# update_stock keeps the same meaning in both subclasses
for p in (laptop, app):
    assert p.update_stock(7) is True and p.get_stock() == 7
    assert p.update_stock(-1) is False and p.get_stock() == 7
print("update_stock behaves the same for PhysicalProduct and DigitalProduct")

try:
    Product("X", "Abstract", 1.0, 1, laptop.get_supplier())   # type: ignore[abstract]
except TypeError as error:
    print("Product cannot be instantiated:", error)

# Section 7
heading("7. POLYMORPHISM: one loop, many behaviours")
inventory = Inventory()
inventory.add_product(laptop)
inventory.add_product(app)

# PREDICT FIRST: what will get_fulfilment_info() print for each product?
for product in inventory.get_products():
    product.display_information()
    print(product.get_fulfilment_info())
    print("-" * 40)

print("Physical shipping cost (1.8 kg):", laptop.calculate_shipping_cost())
print("DigitalProduct has shipping method:", hasattr(app, "calculate_shipping_cost"))
assert laptop.calculate_shipping_cost() == 5.00 + 2.50 * 1.8
assert not hasattr(app, "calculate_shipping_cost")

heading("ALL CHECKS PASSED")
