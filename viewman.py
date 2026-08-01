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
    AND ABS(julianday(nexttime) - julianday('now')) = (
        SELECT MIN(ABS(julianday(nexttime) - julianday('now')))
        FROM Chores
        WHERE user = ?
    );
    """, (user, user))

    #rows = cursor.fetchall()
    #print(rows)

    data=[]
    for row in cursor.fetchall():
        time = row[5]
        time = datetime.strptime(time, "%Y-%m-%d 00:00:00")
        time = time.strftime("%d.%m.%y")
        name = row[1]
        usid=row[0]
        repeat=[2]

        data.append(f"{usid},{name},{repeat},{time}")

    return data



def run():
    print("Starting ViewMan...")
    func.delay()
    func.clear()
    print("---ViewMan--- Chore Viewer")
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
        else:
            print("Your upcoming chore(s): ")

            for i in range(len(data)):
                data2=data[i].split(",")
                chid=data2[0]
                name=data2[1]
                repeat=data2[2]
                time=data2[3]

                print("------------------------")
                print(f"({chid}). {name}")
                if repeat=="1":
                    print("Chore is repeating.")
                else:
                    print("Chore is not repeating.")
                print(f"The chore should be done: {time}")

        print("-------\nWhat do you want to do?")
        option=input("ENTER to exit or input the ID of the chore you want to mark done: ")
        if option=="":
            run()
        else:
            
    


    
