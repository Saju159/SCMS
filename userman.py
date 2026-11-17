#create and remove users


import os
import sqlite3
import config
import time
import func
from datetime import datetime

filepath=func.masterpath


def clear():
    os.system('cls' if os.name == 'nt' else "printf '\033c'")



def writeconfig(user):
    while True:
        deftime=input("When should the chore be done by default? (HH:MM): ")
        try:
            defaulttime = datetime.strptime(deftime, "%H:%M")
            break
        except Exception:
            if deftime.lower()=="cancel":
                print("Canceling...")
                run()
            else:
                print("Invalid input. Try again.")
    while True:
        discord=input("Enter the Discord username of the user: ")
        if discord=="":
            print("Username cannot be empty.")
        else:
            break

    while True:
        hidden=input("Should the user be hidden? TRUE=1/false=0: ")
        if hidden.strip()=="":
            hidden=0
        if hidden!="0" and hidden!="1":
            print("Username cannot be empty.")
        else:
            hidden=int(hidden)
            break


    try:
        with sqlite3.connect(filepath) as connection:
            cursor = connection.cursor()

            # Insert a record into the Students table
            insert_query = '''
            INSERT INTO Users (name, deftime, discord, hidden)
            VALUES (?,?,?);
            '''

            data = (user,defaulttime,discord,hidden)

            cursor.execute(insert_query, data)
            # Commit the changes automatically
            connection.commit()
        print(f"Adding user {user} to the config was successfull.")
    except Exception as e:
        print(f"Failed writing config: {e}")
        func.delaylong()
        func.waituser()

def removeconfig(user):
    try:
        with sqlite3.connect(filepath) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM Users WHERE name = ?",
                (user,)
            )
            connection.commit()
        print(f"Removing user {user} was successfull.")
    except Exception as e:
        print(f"Failed removing from config: {e}")
        func.waituser()

def userquarry():
    func.delay()
    while True:
        name=input("Enter a username. Type cancel to cancel: ").lower()
        if name=="cancel":
            print("Canceling...")
            func.delay()
            clear()
            return ""
        else:
            if func.checkvaliduser(name):
                return name
            else:
                print("Invalid username, try again.")
                func.delay()

def newuserquarry():
    func.delay()
    while True:
        name=input("Enter a username. Type cancel to cancel: ").lower()
        if name=="cancel":
            print("Canceling...")
            func.delay()
            clear()
            return ""
        elif name.strip()=="":
            print("Username cannot be empty")
        else:
            return name

def run():
    clear()
    if not os.path.isfile(filepath):
        print("Database file was not found. Creating...")
        func.createfile()

    if os.path.isfile(filepath):
        print("Database file found. Starting wizard...")

    func.validate()

    func.delay()
    func.clear()

    func.printbold("UserMan User Manager")
    userlist=func.readusers(True)
    string=""

    for i in userlist:
        string=f"{string}\n{i}"

    print(f"Current users are: {string}")
    print("Select option: \n1. Add new user.\n2. Remove current user.\n3. Exit")
    option=input("Option: ")


    if option=="1":
        clear()
        print("Adding new user...")
        user=newuserquarry()
        if not user=="":
            writeconfig(user)
        func.delay()
        run()
   
        

    elif option=="2":
        clear()
        print("Removing user...")
        print(f"Current users are: {func.getusers()}")
        user=userquarry()
        if not user=="":
            removeconfig(user)
        func.delay()
        run()



    elif option=="3":
        clear()
        print("Exiting...")
        func.delay()


    else:
        print("Invalid option. Try Again.")
        func.delaylong()
        clear()
        run()




