#create and remove users


import os
import sqlite3
import config
import time
import func

filepath=func.masterpath


def clear():
    os.system('cls' if os.name == 'nt' else "printf '\033c'")



def readconfig(value):
    try:
        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()

        # Read one column
        cursor.execute(f"SELECT name FROM {value}")

        values=[]

        for row in cursor.fetchall():
            name = row[0]
            values.append(name)
            
        return values

    except Exception as e:
        print(f"Error while reading config: {e}")
        if "no such table" in str(e):
            func.createfile()

def getusers():
    users=readconfig("Users")
    string=""
    for i in range(len(users)):
        if i==len(users)-1:
            string=string+users[i]
        else:
            string=string+users[i]+", "


    return string



def writeconfig(user):
    try:
        with sqlite3.connect(filepath) as connection:
            cursor = connection.cursor()

            # Insert a record into the Students table
            insert_query = '''
            INSERT INTO Users (name)
            VALUES (?);
            '''

            data = (user,)

            cursor.execute(insert_query, data)
            # Commit the changes automatically
            connection.commit()
        print(f"Adding user {user} to the config was successfull.")
    except Exception as e:
        print(f"Failed writing config: {e}")

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

def userquarry():
    func.delay()
    name=input("Enter a username. Type cancel to cancel: ").lower()
    if name=="cancel":
        print("Canceling...")
        func.delay()
        clear()
        return ""
    else:
        return name

def run():
    clear()
    if not os.path.isfile(filepath):
        print("Database file was not found. Creating...")
        func.createfile()

    if os.path.isfile(filepath):
        print("Database file found. Starting wizard...")

    print(f"Current users are: {getusers()}")
    print("Select option: \n1. Add new user.\n2. Remove current user.\n3. Exit")
    option=input("Option: ")


    if option=="1":
        clear()
        print("Adding new user...")
        user=userquarry()
        if not user=="":
            writeconfig(user)
        func.delay()
        run()
   
        

    elif option=="2":
        clear()
        print("Removing user...")
        print(f"Current users are: {getusers()}")
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




