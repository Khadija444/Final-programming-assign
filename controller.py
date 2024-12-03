from storage_layer import StorageLayer
from user import UserAccount, Order
from ticket import SingleDayPass, TwoDayPass, AnnualMembership, ChildTicket, GroupTicket, VIPExperiencePass


class Controller:
    # It manages the interaction between the business model and storage layer
    def __init__(self):
        self.users = {}  # Dictionary of username to UserAccount
        self.tickets = []  # List of available tickets
        self.sales_report = {}  # Tracks ticket sales

        # Load existing data
        self.load_data()

        # Initialize default tickets if needed
        self.initialize_tickets()

        # Ensure there is at least one admin user
        if "admin" not in self.users:
            self.users["admin"] = UserAccount(
                username="admin",
                email="admin@example.com",
                phone_number="0000000000",
                password="admin123",
                role="admin"
            )
            self.save_data()

    def initialize_tickets(self):
        # Initialize default tickets if the list is empty
        if not self.tickets:
            self.tickets.append(SingleDayPass(1, "Single Day Pass", 275))
            self.tickets.append(TwoDayPass(2, "Two Day Pass", 480))
            self.tickets.append(AnnualMembership(3, "Annual Membership", 1840))
            self.tickets.append(ChildTicket(4, "Child Ticket", 185))
            self.tickets.append(GroupTicket(5, "Group Ticket", 220))
            self.tickets.append(VIPExperiencePass(6, "VIP Experience Pass", 550))
            self.save_data()

    def create_user(self, username, email, phone_number, password, role="user"):
        # Creates a new user account
        if username in self.users:
            raise Exception("User already exists!")
        self.users[username] = UserAccount(username, email, phone_number, password, role)
        self.save_data()

    def add_ticket(self, ticket):
        # Adds a new ticket to the system
        self.tickets.append(ticket)
        self.save_data()

    def login(self, username, password):
        # Handles user login by validating credentials
        if username in self.users:
            user = self.users[username]
            if user.password == password:  # Validate the stored password
                return user
            else:
                raise Exception("Invalid password")
        else:
            raise Exception("User not found")

    def book_tickets(self, username, ticket_ids):
        # Books tickets for a user
        if username not in self.users:
            raise Exception("User not found!")
        user = self.users[username]
        selected_tickets = [ticket for ticket in self.tickets if ticket.ticket_id in ticket_ids]
        if not selected_tickets:
            raise Exception("No valid tickets found!")
        order = Order(len(user.order_history) + 1, selected_tickets)
        user.add_order(order)

        # Update sales report
        for ticket in selected_tickets:
            ticket_type = ticket.ticket_type
            if ticket_type in self.sales_report:
                self.sales_report[ticket_type] += 1
            else:
                self.sales_report[ticket_type] = 1

        self.save_data()

    def get_all_tickets(self):
        # Returns all available tickets
        return self.tickets

    def get_sales_report(self):
        # Returns the ticket sales report
        return self.sales_report

    def modify_discounts(self, ticket_type, new_price):
        # Modifies the price of a specific ticket type
        found = False
        for ticket in self.tickets:
            if ticket.ticket_type.strip().lower() == ticket_type.strip().lower():
                ticket.price = new_price
                found = True
        if not found:
            raise Exception("Ticket type not found.")
        self.save_data()

    def save_data(self):
        # Saves all users, tickets, and sales data to storage
        StorageLayer.save_data("users.pkl", self.users)
        StorageLayer.save_data("tickets.pkl", self.tickets)
        StorageLayer.save_data("sales_report.pkl", self.sales_report)

    def load_data(self):
        # Loads all user, ticket, and sales data from storage
        self.users = StorageLayer.load_data("users.pkl") or {}
        self.tickets = StorageLayer.load_data("tickets.pkl") or []
        self.sales_report = StorageLayer.load_data("sales_report.pkl") or {}

    def get_customers(self):
        # Returns a list of all customers
        return list(self.users.values())

    def delete_customer(self, username):
        # Deletes a customer by username
        if username in self.users:
            del self.users[username]
            self.save_data()
            return True
        return False

    def modify_customer(self, username, new_email=None, new_phone=None):
        # Modifies customer details
        if username in self.users:
            if new_email:
                self.users[username].email = new_email
            if new_phone:
                self.users[username].phone_number = new_phone
            self.save_data()
            return True
        return False
