from datetime import date
from EBookManagementSystem import EBook, Genre, Customer, ShoppingCart, Order, Invoice

# Test Cases for EBook Creation
print("Testing EBook Creation...")
ebook1 = EBook(1, "Programming Fundamentals", "Afshan Parkar", date(2021, 1, 1), Genre.EDUCATION, 29.99, "A comprehensive guide to Programming Fundamentals.", 10)
ebook2 = EBook(2, "Diary of a Wimpy Kid", "Jeff Kinney", date(2022, 2, 2), Genre.FICTION, 39.99, "A fun read", 5)
ebook3 = EBook(3, "Data Science Essentials", "Mary Brown", date(2020, 6, 15), Genre.SCIENCE, 45.50, "Data Science basics.", 0)  # Out of stock
print(ebook1)
print(ebook2)
print(ebook3)

# Test Case for Customer Creation
print("\nTesting Customer Creation...")
customer1 = Customer(1001, "Abdulla Alremeithi", "abdulla@example.com")
customer2 = Customer(1002, "Fatima Almansoori", "fatima@example.com")
customer1.enableLoyalty() # Enable loyalty for customer1
print(customer1)
print(customer2)

# Test Cases for ShoppingCart and adding items
print("\nTesting ShoppingCart and Adding Items...")
cart1 = ShoppingCart(1, customer1)
cart2 = ShoppingCart(2, customer2)

# Adding available items to cart1
print("Adding items to cart1...")
cart1.addItem(ebook1, 2)  # Added ebook1 as the second argument 'item'
cart1.addItem(ebook2, 1)  # Added ebook2 as the second argument 'item'
print(cart1)

# Trying to add out-of-stock item to cart2
print("Adding items to cart2...")
cart2.addItem(ebook3, 1)  # Should fail (out of stock)
cart2.addItem(ebook1, 12)  # Should fail (not enough stock)
cart2.addItem(ebook1, 3)  # Should succeed
print(cart2)

# Test Cases for Order Creation
print("\nTesting Order Creation...")
order1 = Order(2001, customer1, cart1)  # With loyalty member, multiple items
order2 = Order(2002, customer2, cart2)  # Without loyalty member, single item
print(order1)
print(order2)

# Test Cases for Invoice Generation
print("\nTesting Invoice Generation...")
invoice1 = Invoice(3001, order1)
invoice2 = Invoice(3002, order2)
print(invoice1)
print(invoice2)

# Testing various edge cases
print("\nEdge Case Testing...")

# Case 1: Customer without loyalty program, single item in cart
print("Case 1: Customer without loyalty, single item")
cart3 = ShoppingCart(3, customer2)
cart3.addItem(ebook2, 1)  # Only one item
order3 = Order(2003, customer2, cart3)
invoice3 = Invoice(3003, order3)
print(order3)
print(invoice3)

# Case 2: Customer with loyalty program, multiple items for discount
print("\nCase 2: Customer with loyalty, multiple items for bulk discount")
cart4 = ShoppingCart(4, customer1)
cart4.addItem(ebook1, 3)
cart4.addItem(ebook2, 3)  # Total 6 items, should get bulk discount
order4 = Order(2004, customer1, cart4)
invoice4 = Invoice(3004, order4)
print(order4)
print(invoice4)

# Case 3: Attempt to add more quantity than available in stock
print("\nCase 3: Adding more than available stock")
cart5 = ShoppingCart(5, customer2)
result = cart5.addItem(ebook1, 15)  # Should fail, as stock is 5 after previous transactions
print("Add item result:", result)
print(cart5)

# Case 4: Creating an empty cart and generating an order
print("\nCase 4: Empty cart")
cart6 = ShoppingCart(6, customer2)
order6 = Order(2005, customer2, cart6)  # Should result in total amount = 0
invoice6 = Invoice(3005, order6)
print(order6)
print(invoice6)

# Case 5: Update stock and re-add items to cart
print("\nCase 5: Updating stock and re-adding items")
ebook3.addStock(10)  # Restock the previously out-of-stock ebook3
cart7 = ShoppingCart(7, customer2)
cart7.addItem(ebook3, 5)  # Should succeed after restocking
order7 = Order(2006, customer2, cart7)
invoice7 = Invoice(3006, order7)
print(order7)
print(invoice7)

# Case 6: Check if VAT and discount are calculated correctly
print("\nCase 6: VAT and Discount Verification")
cart8 = ShoppingCart(8, customer2)
cart8.addItem(ebook1, 1)  # One item with no discounts applied (non-loyalty customer)
order8 = Order(2007, customer2, cart8)
invoice8 = Invoice(3007, order8)
print(order8)
print(invoice8)

print("\nAll cases tested successfully.")