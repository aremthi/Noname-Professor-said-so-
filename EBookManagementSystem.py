from datetime import date, datetime
from enum import Enum
from typing import List


# Enums
class Genre(Enum):
    FICTION = "Fiction"
    NON_FICTION = "Non-Fiction"
    SCIENCE = "Science"
    FANTASY = "Fantasy"
    MYSTERY = "Mystery"
    BIOGRAPHY = "Biography"
    EDUCATION = "Education"


class OrderStatus(Enum):
    PENDING = "Pending"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELED = "Canceled"


# Item Class
class Item:
    """Base class representing a store item."""

    def __init__(self, item_id: int, price: float, description: str, stock_quantity: int):
        self._id = item_id
        self._price = price
        self._description = description
        self._stock_quantity = stock_quantity

    # Getters and Setters
    def getId(self):
        return self._id  # Fixed to use the correct attribute name

    def setId(self, item_id):
        self._id = item_id

    def getPrice(self):
        return self._price

    def setPrice(self, price):
        self._price = price

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    def getStockQuantity(self):
        return self._stock_quantity

    def setStockQuantity(self, stock_quantity):
        self._stock_quantity = stock_quantity

    def addStock(self, quantity: int):
        if quantity > 0:
            self._stock_quantity += quantity

    def removeStock(self, quantity: int) -> bool:
        if quantity <= self._stock_quantity:
            self._stock_quantity -= quantity
            return True
        return False

    def __str__(self):
        return f"Item(ID: {self._id}, Price: {self._price}, Stock: {self._stock_quantity})"


# EBook Class
class EBook(Item):
    """Class representing an electronic book.
       This class inherits from Item (inheritance relationship).
    """

    def __init__(self, book_id: int, title: str, author: str, pub_date: date, genre: Genre, price: float,
                 description: str, stock_quantity: int):
        super().__init__(book_id, price, description, stock_quantity)
        self._title = title
        self._author = author
        self._pub_date = pub_date
        self._genre = genre

    # Getters and Setters
    def getTitle(self):
        return self._title

    def setTitle(self, title):
        self._title = title

    def getAuthor(self):
        return self._author

    def setAuthor(self, author):
        self._author = author

    def getPubDate(self):
        return self._pub_date

    def setPubDate(self, pub_date):
        self._pub_date = pub_date

    def getGenre(self):
        return self._genre

    def setGenre(self, genre):
        self._genre = genre

    def __str__(self):
        return f"EBook(Title: {self._title}, Author: {self._author}, Genre: {self._genre.value})"


# Customer Class
class Customer:
    """Class representing a customer."""

    def __init__(self, customer_id: int, name: str, email: str):
        self._customer_id = customer_id
        self._name = name
        self._email = email
        self._is_loyalty_member = False

    # Getters and Setters
    def getCustomerId(self):
        return self._customer_id

    def setCustomerId(self, customer_id):
        self._customer_id = customer_id

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def getEmail(self):
        return self._email

    def setEmail(self, email):
        self._email = email

    def getIsLoyaltyMember(self):
        return self._is_loyalty_member

    def enableLoyalty(self):
        self._is_loyalty_member = True

    def updateAccount(self):
        pass

    def deleteAccount(self):
        pass

    def __str__(self):
        return f"Customer(ID: {self._customer_id}, Name: {self._name})"


# CartItem Class
class CartItem(Item):
    """Class representing an item in the shopping cart."""
    def __init__(self, ebook: EBook, quantity: int):
        super().__init__(ebook.getId(), ebook.getPrice(), ebook.getDescription(), ebook.getStockQuantity())
        self._ebook = ebook  # The associated eBook
        self._quantity = quantity
        self._date_added = date.today()  # Date the item was added to the cart
        self._is_available = ebook.getStockQuantity() >= quantity  # Availability based on stock

    # Getters and Setters
    def getEbook(self):
        return self._ebook

    def setEbook(self, ebook):
        self._ebook = ebook

    def getQuantity(self):
        return self._quantity

    def setQuantity(self, quantity):
        self._quantity = quantity
        self._is_available = self.getStockQuantity() >= quantity  # Update availability

    def getDateAdded(self):
        return self._date_added

    def isAvailable(self):
        return self._is_available

    def __str__(self):
        return (f"CartItem(EBook: {self._ebook.getTitle()}, Item: {self.getDescription()}, "
                f"Quantity: {self._quantity}, Date Added: {self._date_added}, "
                f"Available: {self._is_available})")

# ShoppingCart Class
class ShoppingCart:
    """Class representing a shopping cart."""
    def __init__(self, cart_id: int, cart_owner: Customer):
        self._cart_id = cart_id
        self._cart_owner = cart_owner
        self._items: List[CartItem] = []
        self._created_date = date.today()
        self._last_updated = date.today()
        self._total_quantity = 0
        self._total_price = 0.0

    # Getters and Setters
    def getCartId(self):
        return self._cart_id

    def setCartId(self, cart_id):
        self._cart_id = cart_id

    def getCartOwner(self):
        return self._cart_owner

    def setCartOwner(self, cart_owner):
        self._cart_owner = cart_owner

    def getItems(self):
        return self._items

    def getTotalQuantity(self):
        return self._total_quantity

    def getTotalPrice(self):
        return self._total_price

    def addItem(self, ebook: EBook, quantity: int):
        """Creates CartItem internally and adds to cart."""
        if ebook.removeStock(quantity):
            cart_item = CartItem(ebook, quantity)
            self._items.append(cart_item)
            self._updateCart(quantity, ebook.getPrice() * quantity)
            self._last_updated = date.today()

    def _updateCart(self, quantity: int, price: float):
        self._total_quantity += quantity
        self._total_price += price

    def __str__(self):
        return (f"ShoppingCart(ID: {self._cart_id}, Owner: {self._cart_owner.getName()}, "
                f"Total Items: {self._total_quantity}, Total Price: {self._total_price:.2f})")

# Order Class
class Order:
    """Class representing an order..
    """
    VAT_RATE = 0.08

    def __init__(self, order_id: int, customer: Customer, cart: ShoppingCart):
        self._order_id = order_id
        self._customer = customer
        self._cart = cart
        self._status = OrderStatus.PENDING
        self._total_amount = self.calculateTotal()
        self._invoices: List[Invoice] = self.createInvoices()  # Composition with Invoice

    # Getters and Setters
    def getOrderId(self):
        return self._order_id

    def setOrderId(self, order_id):
        self._order_id = order_id

    def getCustomer(self):
        return self._customer

    def setCustomer(self, customer):
        self._customer = customer

    def getTotalAmount(self):
        return self._total_amount

    def calculateTotal(self):
        total = sum(item.getPrice() * item.getQuantity() for item in self._cart.getItems())
        if self._customer.getIsLoyaltyMember():
            total *= 0.9
        if len(self._cart.getItems()) >= 5:
            total *= 0.8
        return total * (1 + self.VAT_RATE)

    def createInvoices(self):
        """Creates a list of Invoice objects internally (composition relationship)."""
        invoices = []
        invoice = Invoice(invoice_id=1, order=self)  # Pass the Order instance itself
        invoices.append(invoice)
        return invoices

    def getInvoices(self):
        return self._invoices

    def __str__(self):
        invoice_details = "\n".join(str(invoice) for invoice in self._invoices)
        return (f"Order(ID: {self._order_id}, Total: {self._total_amount:.2f})\n"
                f"Invoices:\n{invoice_details}")


# Invoice Class
class Invoice:
    """Class representing an invoice.
       Has a composition relationship with Order.
    """

    def __init__(self, invoice_id: int, order: Order):
        self._invoice_id = invoice_id
        self._order = order  # Composition: Invoice contains and depends on Order
        self._sub_total = order.getTotalAmount()  # Initial order total before discounts and VAT
        self._discount_amount = self.calculateDiscountAmount()  # Calculate discount based on order
        self._vat_amount = self.calculateVatAmount()  # Calculate VAT on the discounted total
        self._final_total = self.calculateFinalTotal()  # Calculate final total after discount and VAT

    # Getters and Setters
    def getInvoiceId(self):
        return self._invoice_id

    def setInvoiceId(self, invoice_id):
        self._invoice_id = invoice_id

    def getOrder(self):
        return self._order

    def setOrder(self, order):
        self._order = order
        self._sub_total = order.calculateTotal()
        self._discount_amount = self.calculateDiscountAmount()
        self._vat_amount = self.calculateVatAmount()
        self._final_total = self.calculateFinalTotal()

    def getSubTotal(self):
        return self._sub_total

    def getDiscountAmount(self):
        return self._discount_amount

    def getVatAmount(self):
        return self._vat_amount

    def getFinalTotal(self):
        return self._final_total

    def calculateDiscountAmount(self):
        """Calculate discount based on loyalty status and bulk purchase in order."""
        if self._order.getCustomer().getIsLoyaltyMember():
            discount = self._sub_total * 0.10  # 10% loyalty discount
        else:
            discount = 0.0
        if len(self._order._cart.getItems()) >= 5:  # Access items via the cart
            discount += self._sub_total * 0.20  # Additional 20% bulk discount for 5+ items
        return discount

    def calculateVatAmount(self):
        """Calculate VAT on the discounted total."""
        return (self._sub_total - self._discount_amount) * Order.VAT_RATE

    def calculateFinalTotal(self):
        """Calculate final total after applying discount and VAT."""
        return self._sub_total - self._discount_amount + self._vat_amount

    def __str__(self):
        return (f"Invoice(ID: {self._invoice_id}, Subtotal: {self._sub_total:.2f}, "
                f"Discount: {self._discount_amount:.2f}, VAT: {self._vat_amount:.2f}, "
                f"Final Total: {self._final_total:.2f})")