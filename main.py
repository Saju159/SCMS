import os
import time



import viewer
import func
import userman
import choreman
import changeman


while True:
    func.clear()
    print("Welcome to SCMS (Saju's Chore Management System.)")
    print("Please enter a valid option: \n1. View Your Chores.\n2. Create or edit a chore.\n3. Create/edit users. \n9. View Change log. \n(1=Default).")
    option=input("Option: ")

    if option=="1":
        viewman.run()

    elif option=="2":
        choreman.validate()

    elif option=="3":
        userman.run()

    elif option=="9":
        changeman.run()

    else:
        print("Invalid option. Try again.")

    func.delay()