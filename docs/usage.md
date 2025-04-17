# Usage Guide

This document provides detailed instructions for using the Inventory Management System.

## Prerequisites

- Python 3.7 or higher
- JSON file with inventory data (see format below)

## Setting Up

1. Ensure your inventory data file (`Record.json`) is correctly formatted:

```json
{
  "1001": {
    "Name": "Dairy Milk-Silk",
    "Price": 175,
    "Quantity": 3973
  },
  "1002": {
    "Name": "Snickers",
    "Price": 30,
    "Quantity": 2384
  }
  // Add more products as needed
}
```

2. Place the inventory file in the `data` directory or specify a custom location when initializing the InventoryManager.

## Running the System

### Command-line Interface

Run the system using:

```bash
python src/inventory.py
```

### Process Flow

1. **Customer Information**: 
   - Enter customer name
   - Enter email address
   - Enter phone number

2. **Product Selection**:
   - View the menu of available products
   - Enter product ID to add to cart
   - Enter quantity
   - For products with insufficient quantity, you'll be offered the available amount
   - Enter '0' as product ID to finish shopping

3. **Bill Generation**:
   - View itemized bill with product details
   - See tax calculations (CGST and SGST)
   - Confirm total amount

4. **Records Update**:
   - Inventory is automatically updated
   - Sales records are saved to the sales file

## Using as an Imported Module

You can also use the system programmatically:

```python
from src.inventory import InventoryManager

# Initialize with custom file locations
manager = InventoryManager(
    inventory_file='path/to/inventory.json',
    sales_file='path/to/sales.txt'
)

# Display menu
manager.display_menu()

# Add items to cart
manager.add_to_cart("1001", 2)  # Add 2 units of product 1001

# Generate bill
manager.generate_bill("Customer Name", "email@example.com", "1234567890")
```

## Examples

### Basic Purchase Flow

```
---------------Customer Details-----------------
Enter your Name   : John Doe
Enter Mail ID     : john@example.com
Enter Ph No.      : 1234567890

------------------MENU----------------------
1001 : Dairy Milk-Silk 	| 175 	| 3973
1002 : Snickers 	| 30 	| 2384
...
--------------------------------------------
Enter Product ID (or 0 to finish): 1001
Enter the Quantity : 2
Added 2 Dairy Milk-Silk to cart
Enter Product ID (or 0 to finish): 0

-------------------------------------------
                  BILL                     

Customer Name     : John Doe
Email             : john@example.com
Phone             : 1234567890
-------------------------------------------
Products Purchased:

Name              : Dairy Milk-Silk
Quantity          : 2
Price             : 175 Rs
Item Total        : 350 Rs
-------------------------------------------
CGST              : 8.75 Rs
SGST              : 8.75 Rs
-------------------------------------------
Total Bill Amount : 367.50 Rs
-------------------------------------------
 Thanks for your order. Visit us again! 
-------------------------------------------
```

## Troubleshooting

- **File Not Found**: Ensure that the data directory exists and contains the required JSON file
- **Invalid JSON Format**: Check that your inventory file follows the required structure
- **Input Type Error**: Ensure you're entering numeric values for product IDs and quantities