import os
import time



import viewman
import func
import userman
import choreman
import changeman
import chorehist


while True:
    func.clear()
    func.printbold("Main Menu")
    print("Welcome to SCMS (Saju's Chore Management System.)")
    print("Be ware of the Supervisor. ( ఠ ͟ʖ ఠ)")
    if False:
        print("------\nWARNING! The Supervisor has a message!\n------")
    print("Please enter a valid option: \n1. View/complete your Chores.\n2. Create, edit or view info of a chore.\n3. Create/edit users.\n4. Supervisor\n5. Chore Logger / History\n9. View Change log. \n(1=Default).")
    option=input("Option: ")

    if option=="1" or option.strip()=="":
        viewman.run()

    elif option=="2":
        choreman.validate()

    elif option=="3":
        userman.run()

    elif option=="4":
        print("Supervisor")

    elif option=="5":
        chorehist.run()

    elif option=="9":
        changeman.run()

    else:
        print("Invalid option. Try again.")

    func.delay()