import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os

FILE_NAME = "inventory.csv"
FIELDS = ["Item ID", "Name", "Quantity", "Price"]

def load_data():
    data = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, newline='') as f:
            reader = csv.DictReader(f)
            data = list(reader)
    return data

def save_data(data):
    with open(FILE_NAME, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(data)

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Manager")
        self.data = load_data()
        self.create_widgets()
        self.load_table()

    def create_widgets(self):
        # Input Fields
        form = tk.Frame(self.root)
        form.pack(pady=10)

        tk.Label(form, text="Item ID").grid(row=0, column=0)
        tk.Label(form, text="Name").grid(row=0, column=1)
        tk.Label(form, text="Quantity").grid(row=0, column=2)
        tk.Label(form, text="Price").grid(row=0, column=3)

        self.id_entry = tk.Entry(form, width=10)
        self.name_entry = tk.Entry(form, width=20)
        self.qty_entry = tk.Entry(form, width=10)
        self.price_entry = tk.Entry(form, width=10)

        self.id_entry.grid(row=1, column=0)
        self.name_entry.grid(row=1, column=1)
        self.qty_entry.grid(row=1, column=2)
        self.price_entry.grid(row=1, column=3)

        tk.Button(form, text="Add Item", command=self.add_item).grid(row=1, column=4, padx=10)
        tk.Button(form, text="Update", command=self.update_item).grid(row=1, column=5)
        tk.Button(form, text="Delete", command=self.delete_item).grid(row=1, column=6)

        # Search
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Search by ID or Name:").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT)
        tk.Button(search_frame, text="Search", command=self.search_item).pack(side=tk.LEFT)
        tk.Button(search_frame, text="Show All", command=self.load_table).pack(side=tk.LEFT)

        # Table
        self.tree = ttk.Treeview(self.root, columns=FIELDS, show="headings")
        for col in FIELDS:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=100)
        self.tree.pack(pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def load_table(self, data=None):
        for i in self.tree.get_children():
            self.tree.delete(i)
        data = data if data is not None else self.data
        for item in data:
            self.tree.insert("", tk.END, values=(item["Item ID"], item["Name"], item["Quantity"], item["Price"]))

    def add_item(self):
        item_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        quantity = self.qty_entry.get().strip()
        price = self.price_entry.get().strip()

        if not item_id or not name or not quantity or not price:
            messagebox.showerror("Error", "All fields are required.")
            return

        if any(d["Item ID"] == item_id for d in self.data):
            messagebox.showerror("Error", "Duplicate Item ID.")
            return

        if not quantity.isdigit() or not self.is_valid_number(price):
            messagebox.showerror("Error", "Quantity must be integer, Price must be number.")
            return

        item = {"Item ID": item_id, "Name": name, "Quantity": quantity, "Price": f"{float(price):.2f}"}
        self.data.append(item)
        save_data(self.data)
        self.load_table()
        self.clear_entries()

    def update_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select an item to update.")
            return

        index = self.tree.index(selected[0])
        quantity = self.qty_entry.get().strip()
        price = self.price_entry.get().strip()

        if not quantity.isdigit() or not self.is_valid_number(price):
            messagebox.showerror("Error", "Quantity must be integer, Price must be number.")
            return

        self.data[index]["Quantity"] = quantity
        self.data[index]["Price"] = f"{float(price):.2f}"
        save_data(self.data)
        self.load_table()
        self.clear_entries()

    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select an item to delete.")
            return

        index = self.tree.index(selected[0])
        del self.data[index]
        save_data(self.data)
        self.load_table()
        self.clear_entries()

    def search_item(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            self.load_table()
            return
        result = [
            item for item in self.data
            if query in item["Item ID"].lower() or query in item["Name"].lower()
        ]
        self.load_table(result)

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])["values"]
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, values[0])
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[1])
            self.qty_entry.delete(0, tk.END)
            self.qty_entry.insert(0, values[2])
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, values[3])

    def clear_entries(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.qty_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

    def is_valid_number(self, val):
        try:
            float(val)
            return True
        except ValueError:
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
