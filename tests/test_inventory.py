import unittest
import json
import os
import tempfile
from src.inventory import InventoryManager

class TestInventoryManager(unittest.TestCase):
    """Test cases for the InventoryManager class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        
        # Create sample inventory data
        self.inventory_data = {
            "1001": {"Name": "Test Product 1", "Price": 100, "Quantity": 10},
            "1002": {"Name": "Test Product 2", "Price": 200, "Quantity": 5}
        }
        
        # Create temporary inventory file
        self.inventory_file = os.path.join(self.test_dir, "test_inventory.json")
        with open(self.inventory_file, 'w') as f:
            json.dump(self.inventory_data, f)
            
        # Create temporary sales file
        self.sales_file = os.path.join(self.test_dir, "test_sales.txt")
        
        # Initialize inventory manager with test files
        self.manager = InventoryManager(
            inventory_file=self.inventory_file,
            sales_file=self.sales_file
        )
    
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        # Clean up temporary files
        if os.path.exists(self.inventory_file):
            os.remove(self.inventory_file)
        if os.path.exists(self.sales_file):
            os.remove(self.sales_file)
    
    def test_load_inventory(self):
        """Test loading inventory from file."""
        self.assertEqual(len(self.manager.record), 2)
        self.assertEqual(self.manager.record["1001"]["Name"], "Test Product 1")
        self.assertEqual(self.manager.record["1002"]["Price"], 200)
    
    def test_add_to_cart_valid(self):
        """Test adding valid product to cart."""
        result = self.manager.add_to_cart("1001", 2)
        self.assertTrue(result)
        self.assertEqual(len(self.manager.cart), 1)
        self.assertEqual(self.manager.cart[0]["name"], "Test Product 1")
        self.assertEqual(self.manager.cart[0]["quantity"], 2)
        self.assertEqual(self.manager.cart[0]["total"], 200)
        
        # Check inventory update in memory
        self.assertEqual(self.manager.record["1001"]["Quantity"], 8)
    
    def test_add_to_cart_invalid_product(self):
        """Test adding invalid product to cart."""
        result = self.manager.add_to_cart("9999", 1)
        self.assertFalse(result)
        self.assertEqual(len(self.manager.cart), 0)
    
    def test_add_to_cart_excess_quantity(self):
        """Test adding product with quantity exceeding inventory."""
        # Patching input function to simulate user declining purchase
        def mock_input(prompt):
            return "n"
        
        original_input = __builtins__["input"]
        __builtins__["input"] = mock_input
        
        try:
            result = self.manager.add_to_cart("1001", 20)
            self.assertFalse(result)
            self.assertEqual(len(self.manager.cart), 0)
        finally:
            __builtins__["input"] = original_input
    
    def test_generate_bill(self):
        """Test generating bill with items in cart."""
        # Add items to cart
        self.manager.add_to_cart("1001", 2)
        self.manager.add_to_cart("1002", 1)
        
        # Generate bill
        self.manager.generate_bill("Test User", "test@example.com", "1234567890")
        
        # Check if inventory file was updated
        with open(self.inventory_file, 'r') as f:
            updated_inventory = json.loads(f.read())
            self.assertEqual(updated_inventory["1001"]["Quantity"], 8)
            self.assertEqual(updated_inventory["1002"]["Quantity"], 4)
            
        # Check if sales file was created
        self.assertTrue(os.path.exists(self.sales_file))
        with open(self.sales_file, 'r') as f:
            sales_data = f.readlines()
            self.assertEqual(len(sales_data), 2)  # Two items in cart
            
            # Check first sales entry
            first_sale = sales_data[0].split(',')
            self.assertEqual(first_sale[1], "Test User")
            self.assertEqual(first_sale[2], "test@example.com")
            self.assertEqual(first_sale[4], "1001")
            self.assertEqual(int(first_sale[6]), 2)  # Quantity
            self.assertEqual(int(first_sale[8]), 200)  # Total

if __name__ == '__main__':
    unittest.main()