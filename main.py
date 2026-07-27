import os
import time



import viewer
import func


while True:
    func.clear()
    print("Welcome to SCMS (Saju's Chore Management System.)")
    print("Please enter a valid option: \n1. View Your Chores.\n2. Create a new chore. \n3. Edit Chores. \n9. View Change log. \n(1=Default).")
    option=input("Option: ")
    try:
        option=int(option)
    except Exception:
        print("Option is not a valid number.")
        if option=="":
            print("Using default value.")
            option=1
        else:
            print("Invalid option. Try again.")

    print(option)

    if option==1:
        viewer.run()

    time.sleep(1)