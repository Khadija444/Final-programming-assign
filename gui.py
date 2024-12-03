import tkinter as tk
from tkinter import messagebox
from controller import Controller  # Import the backend logic from controller.py


class TicketBookingApp:
    # GUI for the Adventure Land Ticket Booking System
    def __init__(self, root):
        self.root = root
        self.controller = Controller()  # Connect to the backend Controller
        self.root.title("Adventure Land Ticket Booking System")  # Set the title of the window
        self.root.geometry("800x600")  # Set the size of the window
        self.show_login_screen()  # Show the login screen initially

    def show_login_screen(self):
        # Displays the login screen for users and admins
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Login", font=("Arial", 24)).pack(pady=20)
        tk.Label(self.root, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Register", command=self.show_register_screen).pack(pady=10)

    def show_register_screen(self):
        # Displays the registration screen for new users
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Register", font=("Arial", 24)).pack(pady=20)

        tk.Label(self.root, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Email").pack(pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Phone Number").pack(pady=5)
        self.phone_entry = tk.Entry(self.root)
        self.phone_entry.pack(pady=5)

        tk.Label(self.root, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Register", command=self.register_user).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_login_screen).pack(pady=5)

    def login(self):
        # Handles user login
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            user = self.controller.login(username, password)
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            if hasattr(user, "role") and user.role == "admin":
                self.show_admin_dashboard()
            else:
                self.show_user_dashboard(user)
        except Exception as e:
            messagebox.showerror("Login Failed", str(e))

    def register_user(self):
        # Handles user registration
        username = self.username_entry.get()
        email = self.email_entry.get()
        phone_number = self.phone_entry.get()
        password = self.password_entry.get()

        try:
            self.controller.create_user(username, email, phone_number, password)
            messagebox.showinfo("Success", "Account created successfully!")
            self.show_login_screen()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_user_dashboard(self, user):
        # Displays the user dashboard
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Welcome, {user.username}", font=("Arial", 24)).pack(pady=20)
        tk.Button(self.root, text="View Tickets", command=self.view_tickets).pack(pady=10)
        tk.Button(self.root, text="Purchase Tickets", command=lambda: self.purchase_tickets(user)).pack(pady=10)
        tk.Button(self.root, text="View Purchase History", command=lambda: self.view_purchase_history(user)).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.show_login_screen).pack(pady=10)

    def view_tickets(self):
        # Displays available tickets
        tickets = self.controller.get_all_tickets()
        ticket_window = tk.Toplevel(self.root)
        ticket_window.title("Available Tickets")

        for ticket in tickets:
            tk.Label(ticket_window, text=f"{ticket.ticket_type} - {ticket.price} AED").pack()

    def purchase_tickets(self, user):
        # Allows the user to select and purchase tickets
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Purchase Tickets", font=("Arial", 24)).pack(pady=20)

        tk.Label(self.root, text="Enter Ticket IDs (comma-separated):").pack(pady=5)
        self.ticket_ids_entry = tk.Entry(self.root)
        self.ticket_ids_entry.pack(pady=5)

        tk.Button(self.root, text="Confirm Purchase", command=lambda: self.confirm_purchase(user)).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.show_user_dashboard(user)).pack(pady=5)

    def confirm_purchase(self, user):
        # Confirms the ticket purchase
        ticket_ids = self.ticket_ids_entry.get().split(",")
        ticket_ids = [int(tid.strip()) for tid in ticket_ids if tid.strip().isdigit()]

        try:
            self.controller.book_tickets(user.username, ticket_ids)
            messagebox.showinfo("Success", "Tickets purchased successfully!")
            self.show_user_dashboard(user)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_purchase_history(self, user):
        # Displays the user's purchase history
        history_window = tk.Toplevel(self.root)
        history_window.title("Purchase History")

        if not user.order_history:
            tk.Label(history_window, text="No purchase history found.").pack()
            return

        for order in user.order_history:
            tk.Label(history_window, text=str(order)).pack()

    def show_admin_dashboard(self):
        # Displays the admin dashboard
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Admin Dashboard", font=("Arial", 24)).pack(pady=20)
        tk.Button(self.root, text="View Sales Report", command=self.view_sales_report).pack(pady=10)
        tk.Button(self.root, text="Modify Discounts", command=self.modify_discounts).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.show_login_screen).pack(pady=10)

    def view_sales_report(self):
        # Displays the sales report
        report_window = tk.Toplevel(self.root)
        report_window.title("Sales Report")

        sales_report = self.controller.get_sales_report()
        if not sales_report:
            tk.Label(report_window, text="No sales data available.").pack()
        else:
            for ticket_type, sales in sales_report.items():
                tk.Label(report_window, text=f"{ticket_type}: {sales} tickets sold").pack()

    def modify_discounts(self):
        # Displays the modify discounts interface
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Modify Discounts", font=("Arial", 24)).pack(pady=20)
        tk.Label(self.root, text="Ticket Type").pack(pady=5)
        self.ticket_type_entry = tk.Entry(self.root)
        self.ticket_type_entry.pack(pady=5)

        tk.Label(self.root, text="New Price").pack(pady=5)
        self.new_price_entry = tk.Entry(self.root)
        self.new_price_entry.pack(pady=5)

        tk.Button(self.root, text="Update", command=self.update_discount).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_admin_dashboard).pack(pady=5)

    def update_discount(self):
        # Updates the price of a specific ticket
        ticket_type = self.ticket_type_entry.get()
        new_price = self.new_price_entry.get()

        try:
            new_price = float(new_price)
            self.controller.modify_discounts(ticket_type, new_price)
            messagebox.showinfo("Success", f"{ticket_type} price updated to {new_price} AED!")
            self.show_admin_dashboard()
        except ValueError:
            messagebox.showerror("Error", "Invalid price entered.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = TicketBookingApp(root)
    root.mainloop()
