# this program is responsible for adding extra chores to the history and showing chore history to the user.

import userman
import func


def writehistquarry():
    print(f"Current chores in the system: {func.getchores()}")


    print("Enter a chore ID to add, type cancel to cancel: ")
    cancelled=False
    while True:
        cid=input("Chore ID: ").lower()
        if cid=="cancel":
            print("Canceling...")
            func.delay()
            cancelled=True
            break
        else:
            if func.validateid(cid):
                break
            else:
                print("Invalid input. Try again.")

    if not cancelled:
        print("\nEnter a user for you want to add this chore for:")
        print(f"Users in the system are: {func.getusers()}")
        name=userman.userquarry()

        if not cancelled and not name.strip()=="" and func.confirm(f"You want to write chore ID: '{cid}' named: '{func.getchorename(cid)}' for user '{name}' to memory?"):
            func.writehistory(cid,name)
        else:
            print("Canceled...")
            func.delaylong()

def printhist():
    print("")


def run():
    func.clear()
    func.printbold("Chore History Manager")
    print("You can view chore history or add extra completed chores with this system.")
    print(f"Enter an option to continue.\n---------------\n1. Add history entry.\n2. View History.\n4. to exit.")
    selection=input("Option: ")

    if selection=="1":
        func.clear()
        func.delay()
        writehistquarry()

    elif selection=="2":
        func.clear()
        func.delay()
        printhist()

    elif selection=="4":
        print("Exiting...")
        func.delay()

    else:
        print("Invalid option. Try again.")
        run()