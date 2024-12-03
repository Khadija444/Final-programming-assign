# main_page.py
from controller import Controller
from ticket import SingleDayPass, TwoDayPass, AnnualMembership, ChildTicket, GroupTicket, VIPExperiencePass

def main():
    controller = Controller()
    #add tickets
    controller.add_ticket(SingleDayPass(1, 275))
    controller.add_ticket(TwoDayPass(2, 480, 0.1))
    controller.add_ticket(AnnualMembership(3, 1840, 0.15))
    controller.add_ticket(ChildTicket(4, 185, 12))
    controller.add_ticket(GroupTicket(5, 220, 10, 0.2))
    controller.add_ticket(VIPExperiencePass(6, 550))
    #add user and book tickets
    controller.create_user("maryam", "maryam@gmail.com", "123456789")
    controller.book_tickets("maryam", [1, 2, 4])
    #display user data and orders
    user = controller.users["maryam"]
    print(user)
    for order in user.order_history:
        print(order)
if __name__ == "__main__":
    main()
