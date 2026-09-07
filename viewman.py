import userman
import func
import sqlite3
from datetime import datetime, timedelta

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


def validatechore(chore):
    conn = sqlite3.connect(filepath)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Chores WHERE id = ?", (chore,))
    result = cursor.fetchone()
    conn.close()
    if result is not None:
        return True
    else:
        return False



def writelog():
    print("Write to table history")

def markdone(cid):
    conn = sqlite3.connect(filepath)
    cursor = conn.cursor()

    # 2. Fetch the date and the days to add
    cursor.execute("SELECT nexttime, repeatday, repeat FROM Chores WHERE id = ?", (cid,))
    row = cursor.fetchone()

    if row:
        choretime, advance, repeat = row

        if func.confirm(f"Are you sure you want to mark chore {cid} as done ?"):
            if repeat==1:
                func.delay()
                choretime = datetime.strptime(choretime, '%Y-%m-%d %H:%M:%S')
                new_date = choretime + timedelta(days=advance)
                newtime = new_date.strftime('%Y-%m-%d 00:00:00')

                cursor.execute("UPDATE Chores SET nexttime = ? WHERE id = ?", (newtime, cid))
                conn.commit()
                print("Chore completed!")
                print(f"Moved chore: {cid} to a new date: {newtime}.")
                func.delay()
                func.waituser()
                conn.close()

            else:
                func.delay()
                try:
                    with sqlite3.connect(filepath) as connection:
                        cursor = connection.cursor()
                        cursor.execute(
                            "DELETE FROM Chores WHERE id = ?",
                            (cid,)
                        )
                        connection.commit()
                        connection.close()
                    print(f"Removing chore {cid} was successfull.")
                    func.delay()
                    func.waituser()
                except Exception as e:
                    print(f"Failed removing chore {cid} from config: {e}")
                    func.waituser()
        else:
            func.delay()
            print("Exiting...")


    else:
        print("Error! Chore was not found from database.")
        func.waituser()



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
                    if validatechore(option):
                        markdone(option)
                        break

                    else:
                        print("Invalid Chore. Try again.")
                        func.delay()
