import json
import time
import os

class InventoryManager:
    """
    A class to manage inventory operations including product display, 
    cart management, and sales recording.
    """
    def __init__(self, inventory_file='data/Record.json', sales_file='data/Sales.txt'):
        """Initialize the InventoryManager with file paths."""
        self.inventory_file = inventory_file
        self.sales_file = sales_file
        self.cart = []
        self.total_bill = 0
        self.record = self._load_inventory()
        
    def _load_inventory(self):
        """Load inventory from JSON file."""
        try:
            with open(self.inventory_file, 'r') as fd:
                return json.loads(fd.read())
        except FileNotFoundError:
            print(f"Error: Inventory file {self.inventory_file} not found.")
            return {}
            
    def display_menu(self):
        """Display available products in inventory."""
        print("\n------------------MENU----------------------")
        for i in self.record.keys():
            print(i, ":", self.record[i]["Name"], "\t|", 
                  self.record[i]["Price"], "\t|", 
                  self.record[i]["Quantity"])
        print("--------------------------------------------")
        
    def add_to_cart(self, product_id, requested_quantity):
        """
        Add a product to cart if available in requested quantity.
        
        Args:
            product_id (str): The product ID to add
            requested_quantity (int): The quantity requested
            
        Returns:
            bool: True if added to cart, False otherwise
        """
        if product_id not in self.record:
            print("Invalid Product ID! Please try again.")
            return False
            
        available_quantity = self.record[product_id]['Quantity']
        
        if available_quantity >= requested_quantity:
            # Add to cart with requested quantity
            self._process_cart_addition(product_id, requested_quantity)
            return True
        else:
            # Not enough quantity
            print(f"\nSorry, we don't have enough quantity in our Inventory")
            print(f"We only have {available_quantity} quantity")
            print("Would you like to purchase it?")
            
            ch = input("Press Y/y to purchase: ")
            if ch.lower() == 'y':
                # Add to cart with available quantity
                self._process_cart_addition(product_id, available_quantity)
                return True
            return False
    
    def _process_cart_addition(self, product_id, quantity):
        """Process adding an item to cart and update inventory."""
        item_total = quantity * self.record[product_id]["Price"]
        self.cart.append({
            "product_id": product_id,
            "name": self.record[product_id]["Name"],
            "quantity": quantity,
            "price": self.record[product_id]["Price"],
            "total": item_total
        })
        
        # Update inventory
        self.record[product_id]['Quantity'] -= quantity
        self.total_bill += item_total
        
        print(f"Added {quantity} {self.record[product_id]['Name']} to cart")
        
    def generate_bill(self, customer_name, customer_email, customer_phone):
        """Generate bill for the items in cart."""
        if not self.cart:
            print("\nNo items purchased. Thank you for visiting!")
            return
        
        total_sum = sum(item['total'] for item in self.cart)
        cgst = sgst = 0.025 * total_sum
        final_total = total_sum + cgst + sgst
        
        print("\n-------------------------------------------")
        print("                  BILL                     \n")
        print(f"Customer Name     : {customer_name}")
        print(f"Email             : {customer_email}")
        print(f"Phone             : {customer_phone}")
        print("-------------------------------------------")
        print("Products Purchased:")
        
        for item in self.cart:
            print(f"\nName              : {item['name']}")
            print(f"Quantity          : {item['quantity']}")
            print(f"Price             : {item['price']} Rs")
            print(f"Item Total        : {item['total']} Rs")
            
        print("-------------------------------------------")
        print(f"CGST              : {cgst:.2f} Rs")
        print(f"SGST              : {sgst:.2f} Rs")
        print("-------------------------------------------")
        print(f"Total Bill Amount : {final_total:.2f} Rs")
        print("-------------------------------------------")
        print(" Thanks for your order. Visit us again! ")
        print("-------------------------------------------")
        
        # Save sales record
        self._save_sales_records(customer_name, customer_email, customer_phone)
        # Update inventory file
        self._update_inventory()
        
    def _save_sales_records(self, customer_name, customer_email, customer_phone):
        """Save sales records to file."""
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.sales_file), exist_ok=True)
        
        with open(self.sales_file, 'a') as fd:
            for item in self.cart:
                sales_entry = (
                    f"1,{customer_name},{customer_email},{customer_phone},"
                    f"{item['product_id']},{item['name']},{item['quantity']},"
                    f"{item['price']},{item['total']},{time.ctime()}\n"
                )
                fd.write(sales_entry)
                
    def _update_inventory(self):
        """Update inventory file with the latest quantities."""
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.inventory_file), exist_ok=True)
        
        with open(self.inventory_file, 'w') as fd:
            json.dump(self.record, fd, indent=4)

def main():
    """Main function to run the inventory management system."""
    inventory_manager = InventoryManager()
    
    # Taking User Details First
    print("---------------Customer Details-----------------")
    customer_name = input("Enter your Name   : ")
    customer_email = input("Enter Mail ID     : ")
    customer_phone = input("Enter Ph No.      : ")
    
    # Display available products
    inventory_manager.display_menu()
    
    # Shopping loop
    while True:
        product_id = input("Enter Product ID (or 0 to finish): ")
        
        if product_id == '0':
            break
            
        quantity = int(input("Enter the Quantity : "))
        inventory_manager.add_to_cart(product_id, quantity)
        
    # Generate bill
    inventory_manager.generate_bill(customer_name, customer_email, customer_phone)

if __name__ == "__main__":
    main()