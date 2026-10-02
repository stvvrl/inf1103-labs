def get_valid_input():
    user_input = input("Enter stock quantity (or 'quit' to finish): ")

    if user_input.lower() == "quit":
        return "quit"

    if not user_input.isdigit():
        print("Error: Please enter a non-negative integer.")
        return None

    return int(user_input)


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    print("\n--- Final Report ---")
    print(f"Total Units Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    inventory = 0
    failed_attempts = 0
    deliveries_processed = 0

    while True:
        value = get_valid_input()

        if value == "quit":
            generate_report(inventory, failed_attempts)
            break

        if value is None:
            failed_attempts += 1
            continue

        inventory = process_delivery(inventory, value)
        tax = calculate_tax(value)
        deliveries_processed += 1

        print(f"Delivery accepted: {value} units")
        print(f"Tax for this delivery: ${tax}")

        if inventory > 500:
            print("Overstock! Total inventory exceeds 500 units.")
            break


if __name__ == "__main__":
    main()