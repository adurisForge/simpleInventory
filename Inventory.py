import csv
import os

# File where inventory data will be stored
FILE_NAME = "inventory.csv"
# Column headers for CSV file
FIELDNAMES = ["Item ID", "Name", "Quantity", "Price"]

# Load inventory data from CSV file (if it exists)
def load_inventory():
    inventory = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="r", newline="") as f:
            reader = csv.DictReader(f)
            inventory = list(reader)
    return inventory

# Save inventory data back to the CSV file
def save_inventory(inventory):
    with open(FILE_NAME, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(inventory)

# Prompt user to enter a valid number (integer or float)
def input_valid_number(prompt):
    while True:
        value = input(prompt)
        if value.replace('.', '', 1).isdigit():
            return float(value)
        else:
            print("❌ Invalid number. Try again.")

# Check if an item with the same ID already exists
def item_exists(inventory, item_id):
    return any(item["Item ID"] == item_id for item in inventory)

# Add a new item to the inventory
def add_item(inventory):
    item_id = input("Enter Item ID: ").strip()
    if item_exists(inventory, item_id):
        print("❌ Item ID already exists!")
        return
    name = input("Enter Item Name: ").strip()
    quantity = input_valid_number("Enter Quantity: ")
    price = input_valid_number("Enter Price: ")

    # Add item as dictionary
    inventory.append({
        "Item ID": item_id,
        "Name": name,
        "Quantity": str(int(quantity)),
        "Price": f"{price:.2f}"
    })
    print("✅ Item added!")

# Display all items in the inventory in a table format
def view_items(inventory):
    if not inventory:
        print("⚠️ No items found.")
        return
    print("\n📦 Inventory Items:")
    print(f"{'ID':<10}{'Name':<20}{'Qty':<10}{'Price':<10}")
    print("-" * 50)
    for item in inventory:
        print(f"{item['Item ID']:<10}{item['Name']:<20}{item['Quantity']:<10}{item['Price']:<10}")
    print()

# Update quantity and price of an existing item
def update_item(inventory):
    item_id = input("Enter Item ID to update: ").strip()
    for item in inventory:
        if item["Item ID"] == item_id:
            item["Quantity"] = str(int(input_valid_number("Enter new Quantity: ")))
            item["Price"] = f"{input_valid_number('Enter new Price: '):.2f}"
            print("✅ Item updated!")
            return
    print("❌ Item not found.")

# Remove an item from the inventory
def delete_item(inventory):
    item_id = input("Enter Item ID to delete: ").strip()
    for i, item in enumerate(inventory):
        if item["Item ID"] == item_id:
            del inventory[i]
            print("✅ Item deleted!")
            return
    print("❌ Item not found.")

# Search for items by ID or name (case-insensitive)
def search_items(inventory):
    query = input("Enter Item ID or Name to search: ").strip().lower()
    found = [
        item for item in inventory
        if query in item["Item ID"].lower() or query in item["Name"].lower()
    ]
    if found:
        view_items(found)
    else:
        print("❌ No matching items found.")

# Main menu loop
def main():
    inventory = load_inventory()
    while True:
        print("\n===== Inventory Manager =====")
        print("1. Add Item")
        print("2. View Items")
        print("3. Update Item")
        print("4. Delete Item")
        print("5. Search Item")
        print("6. Exit")

        choice = input("Select an option: ").strip()
        if choice == '1':
            add_item(inventory)
        elif choice == '2':
            view_items(inventory)
        elif choice == '3':
            update_item(inventory)
        elif choice == '4':
            delete_item(inventory)
        elif choice == '5':
            search_items(inventory)
        elif choice == '6':
            save_inventory(inventory)
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Try again.")

# Run the program
if __name__ == "__main__":
    main()
