import userman
import func
import sqlite3
from datetime import datetime

filepath=func.masterpath

def getchore(user):
    conn = sqlite3.connect(filepath)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM Chores
    WHERE user = ?
    ORDER BY ABS(julianday(nexttime) - julianday('now')) ASC
    LIMIT 3;
    """, (user,))

    #rows = cursor.fetchall()
    #print(rows)

    data=[]
    data2=cursor.fetchall()

    return data2

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
        func.waituser()

def getchores():
    chores=readconfig("Chores")
    string=""
    for i in range(len(chores)):
        if i==len(chores)-1:
            string=string+chores[i]
        else:
            string=string+chores[i]+", "
    if len(chores)==0:
        string="There are no chores in the system."

    return string


def validatechore(chore):
    chores=getchores()
    if chore in str(chores) and not chore=="":
        return True
    else:
        return False


def run():
    print("Starting ViewMan...")
    func.delay()
    func.clear() 
    func.printbold("ViewMan Chore Viewer")
    print("View your chores here. Press ENTER without typing anything to exit.")
    exiter=False
    

    while True:
        users=userman.getusers()
        print(f"Valid options are: {users}")
        user=input("Enter User: ").lower()
        if userman.checkvaliduser(user):
            break
        elif user=="":
            print("Exiting...")
            exiter=True
            break
        else:
            print("Invalid user name. Try again.")


    if not exiter:
        data=getchore(user)
        
        func.delay()
        func.clear()

        if len(data)==0:
            print("You do not have upcoming chores.")

            input("Press ENTER to continue")
        else:
            print("Your 3 closest chores: ")

            for i in range(len(data)):
                #data2=data[i].split(",")
                chid=data[i][0]
                name=data[i][1]
                repeat=data[i][2]
                time=data[i][5]
                time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                time = time.strftime("%d.%m.%Y")


                print("------------------------")
                print(f"({chid}). {name}")
                if repeat==1:
                    print("Chore is repeating.")
                else:
                    print("Chore is not repeating.")
                print(f"The chore should be done: {time}")

            print("-------\nWhat do you want to do?")
            while True:
                option=input("ENTER to exit or input the ID of the chore you want to mark done: ")
                if option=="":
                    break
                    run()
                else:
                    if validatechore(chore):
                        break
                    else:
                        print("Invalid Chore. Try again.")
                        func.delay()
