#the user.py
from datetime import datetime

class UserAccount:
    # Represents a user account in the system
    # Demonstrates Aggregation: Contains multiple Order objects
    def __init__(self, username, email, phone_number, password, role="user"):
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.password = password  # Store the password
        self.role = role  # Add role to differentiate between admin and regular users
        self.order_history = []  # Aggregation: Contains a collection of Orders

    def add_order(self, order):
        # Add an order to the user's history
        self.order_history.append(order)

    def __str__(self):
        # Return a string representation of the user
        return f"User[Username: {self.username}, Email: {self.email}, Role: {self.role}]"


class Order:
    # Represents an order containing one or more tickets
    # Demonstrates Aggregation: Contains a collection of Ticket objects
    def __init__(self, order_id, tickets):
        self.order_id = order_id
        self.tickets = tickets  # Aggregation: Order contains multiple Ticket objects
        self.total_amount = sum(ticket.get_price() for ticket in tickets)
        self.order_date = datetime.now()

    def __str__(self):
        # Return a string representation of the order
        return f"Order[ID: {self.order_id}, Date: {self.order_date.strftime('%Y-%m-%d %H:%M:%S')}, Total: {self.total_amount}]"
