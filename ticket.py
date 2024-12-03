# the ticket.py
class Ticket:
    #a base class for all ticket types and it demonstrates inheritance: (e.g., SingleDayPass, TwoDayPass) inherit from Ticket.
    def __init__(self, ticket_id, price, validity_period, ticket_type):
        self.ticket_id = ticket_id
        self.price = price
        self.validity_period = validity_period
        self.ticket_type = ticket_type

    def get_price(self):
        #returns the price of the ticket
        return self.price

    def get_validity_period(self):
        #returns the validity period of the ticket
        return self.validity_period

    def __str__(self):
        #Returns a string representation of the ticket
        return f"Ticket[ID: {self.ticket_id}, Type: {self.ticket_type}, Price: {self.price}]"


class SingleDayPass(Ticket):
    def __init__(self, ticket_id, price):
        #represents a single-day pass ticket
        super().__init__(ticket_id, price, "1 Day", "Single Day Pass")


class TwoDayPass(Ticket):
    def __init__(self, ticket_id, price, online_discount):
        #represents a two-day pass ticket with an online discount
        super().__init__(ticket_id, price, "2 Days", "Two Day Pass")
        self.online_discount = online_discount

    def apply_discount(self):
        #apply the online discount
        return self.price - (self.price * self.online_discount)


class AnnualMembership(Ticket):
    def __init__(self, ticket_id, price, renewal_discount):
        #represents an annual membership ticket with a renewal discount
        super().__init__(ticket_id, price, "1 Year", "Annual Membership")
        self.renewal_discount = renewal_discount

    def apply_renewal_discount(self):
        #applyies a renewal discount to the ticket price
        return self.price - (self.price * self.renewal_discount)


class ChildTicket(Ticket):
    def __init__(self, ticket_id, price, child_age_limit):
        #represents a child ticket with an age limit
        super().__init__(ticket_id, price, "1 Day", "Child Ticket")
        self.child_age_limit = child_age_limit

    def validate_age(self, age):
        #validate if the child's age is within the allowed limit
        return age <= self.child_age_limit


class GroupTicket(Ticket):
    def __init__(self, ticket_id, price_per_person, min_group_size, discount):
        #represents a group ticket with a minimum group size and a discount
        super().__init__(ticket_id, price_per_person, "1 Day", "Group Ticket")
        self.min_group_size = min_group_size
        self.discount = discount

    def calculate_group_price(self, group_size):
        #calculate the total price for the group
        if group_size >= self.min_group_size:
            total_price = (self.price * group_size) - (self.price * group_size * self.discount)
        else:
            total_price = self.price * group_size
        return total_price


class VIPExperiencePass(Ticket):
    def __init__(self, ticket_id, price, expedited_access=True):
        #represents a VIP experience pass with expedited access
        super().__init__(ticket_id, price, "1 Day", "VIP Experience Pass")
        self.expedited_access = expedited_access