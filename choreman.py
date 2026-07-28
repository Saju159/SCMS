# manages creating and editing of chores
import func
import os
import sqlite3
from datetime import datetime

filepath=func.masterpath

def getchores():
    try:
        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()

        # Read one column
        cursor.execute(f"SELECT id, name FROM Chores")

        values=""

        for row in cursor.fetchall():
            id = row[0]
            name = row[1]
            values=values+(f"{id}, {name}\n")
  
            

    except Exception as e:
        print(f"Error while reading config: {e}")
        if "no such table" in str(e):
            func.createfile()

def remove():
    print("Chore remover")
    print(f"Current chores in the system: {getchores()}")
    print("Enter a chore ID to remove: ")
    while True:
        try:
            id=int(input("Chore ID: "))
            break
        except Exception:
            print("Invalid input. Try again.")
        
    try:
        with sqlite3.connect(filepath) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM Chores WHERE id = ?",
                (id,)
            )
            connection.commit()
        print(f"Removing chore {id} was successfull.")
    except Exception as e:
        print(f"Failed removing chore {id} from config: {e}")

def new():
    print("You can write 'cancel' any time to stop the process.")
    name=input("Enter a name for the Chore: ")
    if name.lower()=="cancel":
        print("Canceling...")
        run()
    while True:
        repeat=input("Repeat this chore automatically. TRUE(1)/false(0): ").lower()
        if repeat.lower()=="cancel":
            print("Canceling...")
            break
            run()
        elif repeat=="true" or repeat=="1":
            repeatfinal=1
            break

        elif repeat == "false" or repeat == "0":
            repeatfinal=0
            break
        elif repeat=="":
            repeatfinal=1
            break
        else:
            print("Invalid option. Try again.")
    if repeatfinal==1:
        while True:
            days=input("How ofter should the chore be run (days): ")
            try:
                finaldays=int(days)
                break
            except Exception:
                if days.lower()=="cancel":
                    print("Canceling...")
                    run()
                else:
                    print("Invalid input. Try again.")

        
        while True:
            usrcha=input("Change users after every completion. TRUE(1)/false(0): ").lower()
            if usrcha=="cancel":
                print("Canceling...")
                break
                run()
            elif usrcha=="true" or usrcha=="1":
                usrchafinal=1
                break

            elif usrcha == "false" or usrcha == "0":
                usrchafinal=0
                break

            elif usrcha=="":
                usrchafinal=1
                break
            else:
                print("Invalid option. Try again.")

    else:
        finaldays=0
        usrchafinal=0
        finaltime=0

    while True:
        nextime=input("When should the chore be done? (dd.mm.yy.HH:MM): ")
        try:
            nextimefinal = datetime.strptime(nextime, "%d.%m.%y.%H:%M")
            break
        except Exception:
            if nextime.lower()=="cancel":
                print("Canceling...")
                run()
            else:
                print("Invalid input. Try again.")

    func.delay()
    func.clear()
    print("Chore information: ")
    print(name)
    if repeatfinal==0:
        print("Automatic repeat is disabled.")
    else:
        print("Automatic repeat enabled.")
        print(f"Chore is repeated every: {finaldays} day(s).")
        print(f"Chore is run at {finaltime.strftime("%H:%M")} by default.")
    if usrchafinal==0:
        print("Automatic user change is disabled.")
    else:
        print("Automatic user change is enabled.")
    print(f"This chore will be run for the next time: {nextimefinal}")

    while True:
        print("\nDo you want to save this chore?")
        confirmation=input("TRUE(1)/false(0): ").lower()
        if confirmation=="true" or confirmation == "1":
            write=True
            break

        elif confirmation == "false" or confirmation == "0":
            write=False
            break
        elif confirmation == "":
            write=True
            break
        else:
            print("Invalid option. Try again.")
    
    if write==True:
        try:
            with sqlite3.connect(filepath) as connection:
                cursor = connection.cursor()

                insert_query = '''
                INSERT INTO Chores (name, repeat, repeatday, usrchan, nexttime, user)
                VALUES (?, ?, ?, ?, ?, ?);
                '''

                data = (name,repeatfinal,finaldays,usrchafinal,nextimefinal,username)
                print(data)

                cursor.execute(insert_query, data)

                # Commit the changes automatically
                connection.commit()
            print("Chore was written to memory successfully.")
            func.delaylong()
            run()
        except Exception as e:
            if "no such table" in str(e):
                func.createfile()
            if "no column named" in str(e):
                func.createfile()
            print(f"An error occured when writing to the database: {e}")

        


def validate():
    print("Starting ChoreMan...")
    print("Validating database...")
    func.createfile()
    func.validate()

    if os.path.isfile(filepath):
        print("Database file found. Starting ChoreMan...")

    func.delay()
    run()

def run():
    func.clear()
    print(f"---ChoreMan-- \nEnter an option to continue.\nCurrent chores in the system: {getchores()} \n1. Create a new chore.\n2. Edit a chore. \n3. Remove a chore. \n4. View chore information.")
    selection=input("Option: ")

    if selection=="1":
        func.clear()
        func.delay()
        print("Chore wizard")
        new()

    elif selection=="3":
        unc.clear()
        func.delay()
        remove()
        









#validate()