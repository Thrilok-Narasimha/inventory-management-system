# Inventory Management System

A robust Python application for managing inventory, processing sales, and generating bills.

## Features

- **Product Management**: View available products with prices and quantities
- **Shopping Cart**: Add items to cart with quantity validation
- **Bill Generation**: Generate detailed bills with tax calculations
- **Sales Recording**: Maintain records of all sales transactions
- **Inventory Tracking**: Automatically update inventory after purchases

## Installation

Clone the repository and install the required packages:

```bash
git clone https://github.com/yourusername/inventory-management-system.git
cd inventory-management-system
pip install -r requirements.txt
```

## Usage

1. Prepare your inventory data in `data/Record.json`:

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
}
```

2. Run the program:

```bash
python src/inventory.py
```

3. Follow the prompts to:
   - Enter customer details
   - Select products by ID
   - Specify quantities
   - Complete purchase and view bill

For detailed usage instructions, see [usage documentation](docs/usage.md).

## Project Structure

```
inventory-management-system/
├── README.md           # Project overview and instructions
├── src/                # Source code
│   ├── __init__.py
│   ├── inventory.py    # Main inventory management module
├── data/               # Data files
│   ├── Record.json     # Inventory records
│   └── Sales.txt       # Sales history
├── docs/               # Documentation
│   └── usage.md        # Detailed usage guide
├── tests/              # Test suite
│   ├── __init__.py
│   └── test_inventory.py
├── .gitignore          # Git ignore file
├── requirements.txt    # Project dependencies
└── LICENSE             # License information
```

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.