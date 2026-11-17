
import sqlite3
import config
import os 
import time
from datetime import datetime

import requests


masterpath=os.path.join(config.getBaseConfigDir(),"scms.db")
filepath=masterpath

def clear():
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

def delay():
    time.sleep(0.5)

def delaylong():
    time.sleep(3)

def waituser():
    input("Program stopped. Press ENTER to continue.")

def printbold(text):
    print(f"\033[1m{text}\033[0m")

def confirm(message):
    clear()
    print("Are you sure?")
    delay()
    print(message)
    while True:
        answer=input("YES(1),no(0), Default=1: ").lower()
        if answer=="":
            answer="1"
            break
        elif answer=="yes" or answer=="1":
            answer="1"
            break
        elif answer=="no" or answer=="0":
            answer="0"
            break
        else:
            print("Invalid input. Try again.")
            delay()
    if answer=="1":
        return True
    else:
        return False

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

def getusers():
    users=readconfig("Users")
    string=""
    for i in range(len(users)):
        if i==len(users)-1:
            string=string+users[i]
        else:
            string=string+users[i]+", "
    if len(users)==0:
        string="There are no users in the system."

    return string

def checkvaliduser(user):
    users=getusers()
    if user in str(users) and not user=="":
        return True
    else:
        return False

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
            values=values+(f"\n({id}). {name}")

        return values
  
    except Exception as e:
        print(f"Error while reading config: {e}")
        if "no such table" in str(e):
            createfile()
        waituser()

def validateid(cid):
    conn = sqlite3.connect(filepath)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Chores WHERE id = ?", (cid,))

    if cursor.fetchone():
        return True
    else:
        return False

def getchorename(cid):
    try:
        # Connect to database
        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()

        # Read one column
        cursor.execute("SELECT * FROM Chores WHERE id = ?", (cid,))

        values=[]

        data=cursor.fetchone()

        name = data[1]


    except Exception as e:
        raise
        print(f"Reading database failed: {e}")
        waituser()

    return name

def getchoreuser(id):
    try:
        # Connect to database
        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()

        # Read one column
        cursor.execute("SELECT * FROM Chores WHERE id = ?", (id,))

        values=[]

        data=cursor.fetchone()

        user = data[6]


    except Exception as e:
        print(f"Reading database failed: {e}")
        waituser()

    return user

def getdiscord(name):
    try:
        # Connect to database
        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()

        # Read one column
        cursor.execute("SELECT * FROM Users WHERE name = ?", (name,))

        values=[]

        data=cursor.fetchone()
        discord = data[2]

    except Exception as e:
        print(f"Reading database failed: {e}")
        waituser()

    return discord

def getwebhookurl():
    if checkvaliduser("log-bot"):
        url=getdiscord("log-bot")
        return url
    else:
        print("User 'log-bot' not found.")
        return None
    
def writehistory(chore_id,user):
    validate()
    name=getchorename(chore_id)
    try:
        with sqlite3.connect(filepath) as connection:
            cursor = connection.cursor()

            insert_query = '''
            INSERT INTO History (chore_id, name, description, user, completed)
            VALUES (?, ?, ?, ?, ?);
            '''
            data = (chore_id,name,"Description",user,datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

            cursor.execute(insert_query, data)

            # Commit the changes automatically
            connection.commit()
        print("Chore was written to history successfully.")

        data = {"content": f"User '{user}' completed chore: '({chore_id}). {name}'. @everyone."}
        url=getwebhookurl()
        if url:
            response = requests.post(url, json=data)

            if response.status_code == 204:
                print("Discord log sent successfully!")
            else:
                print(f"Failed to send discord log: {response.status_code}")
                print(f"With URL: '{url}'")
                waituser()
        else:
            print("Could not get Discord bot URL.")
            waituser()

        delaylong()
    except Exception as e:
        if "no such table" in str(e):
            createfile()
        if "no column named" in str(e):
            createfile()
        print(f"An error occured when writing to the database: {e}")
        waituser()

def createfile():
    print("Creating file...")
    try:
        with sqlite3.connect(filepath) as connection:

            # Create a cursor object
            cursor = connection.cursor()

            # Write the SQL command to create the table
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS Users (
                name TEXT,
                deftime TEXT,
                discord TEXT

            );
            '''

            # Execute the SQL command
            cursor.execute(create_table_query)

            # Commit the changes
            connection.commit()

        print(f"Created users table to {filepath} successfully.")
        delay()


        with sqlite3.connect(filepath) as connection:

            # Create a cursor object
            cursor = connection.cursor()

            # Write the SQL command to create the table
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS Chores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                repeat INTEGER,
                repeatday INTEGER,
                usrchan INTEGER,
                nexttime TEXT,
                user TEXT


            );
            '''

            # Execute the SQL command
            cursor.execute(create_table_query)

            # Commit the changes
            connection.commit()

        print(f"Created chores table to {filepath} successfully.")
        delay()

        with sqlite3.connect(filepath) as connection:

            # Create a cursor object
            cursor = connection.cursor()

            # Write the SQL command to create the table
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS History (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chore_id INTEGER,
                name TEXT,
                description TEXT,
                user TEXT,
                completed TEXT


            );
            '''

            # Execute the SQL command
            cursor.execute(create_table_query)

            # Commit the changes
            connection.commit()

        print(f"Created history table to {filepath} successfully.")
        delay()

    except Exception as e:
        print(f"Creating database failed: {e}")
        if not os.path.isfile(filepath):
            print("Config database is missing.")

def validate():
    if not os.path.isfile(filepath):
        print("Database file was not found. Creating...")
        createfile()
        delay()



    with sqlite3.connect(filepath) as connection:
        cursor = connection.cursor()
        cursor.execute(""" SELECT name FROM sqlite_master
        WHERE type='table' AND name='Users'
        """)
    if not cursor.fetchone():
        print("Table Users does not exist. Creating...")
        delay()
        createfile()



    with sqlite3.connect(filepath) as connection:
        cursor = connection.cursor()
        cursor.execute(""" SELECT name FROM sqlite_master
        WHERE type='table' AND name='Chores'
        """)
    if not cursor.fetchone():
        print("Table Chores does not exist. Creating...")
        delay()
        createfile()


    with sqlite3.connect(filepath) as connection:
        cursor = connection.cursor()
        cursor.execute(""" SELECT name FROM sqlite_master
        WHERE type='table' AND name='History'
        """)
    if not cursor.fetchone():
        print("Table History does not exist. Creating...")
        delay()
        createfile()



    with sqlite3.connect(filepath) as connection:
        cursor = connection.cursor()
        cursor.execute("PRAGMA table_info(Users)")
        columns = [row[1] for row in cursor.fetchall()]
        if "deftime" not in columns:
            cursor.execute("ALTER TABLE Users ADD COLUMN deftime TEXT")
            print("Added missing deftime column to table users.")
        if "discord" not in columns:
            cursor.execute("ALTER TABLE Users ADD COLUMN discord TEXT")
            print("Added missing discord column to table users.")
        connection.commit()



    with sqlite3.connect(filepath) as connection:
        cursor = connection.cursor()
        cursor.execute("PRAGMA table_info(Chores)")
        columns = [row[1] for row in cursor.fetchall()]

        if "id" not in columns:
            cursor.execute("ALTER TABLE Chores ADD COLUMN id TEXT")
            print("Added missing id column to table Chores.")
            delay()

        if "name" not in columns:
            cursor.execute("ALTER TABLE Chores ADD COLUMN name TEXT")
            print("Added missing name column to table Chores.")
            delay()

        if "repeat" not in columns:
            cursor.execute("ALTER TABLE Chores ADD COLUMN repeat TEXT")
            print("Added missing repeat column to table Chores.")
            delay()
        if "repeatday" not in columns:
            cursor.execute("ALTER TABLE Chores ADD COLUMN repeatday TEXT")
            print("Added missing repeatday column to table Chores.")
            delay()
        if "usrchan" not in columns:
            cursor.execute("ALTER TABLE Chores ADD COLUMN usrchan TEXT")
            print("Added missing usrchan column to table Chores.")
            delay()
        if "nexttime" not in columns:
            cursor.execute("ALTER TABLE Chores ADD COLUMN nexttime TEXT")
            print("Added missing nexttime column to table Chores.")
            delay()
        if "user" not in columns:
            cursor.execute("ALTER TABLE Chores ADD COLUMN user TEXT")
            print("Added missing user column to table Chores.")
            delay()
        connection.commit()

    with sqlite3.connect(filepath) as connection:
        cursor = connection.cursor()
        cursor.execute("PRAGMA table_info(History)")
        columns = [row[1] for row in cursor.fetchall()]

        if "id" not in columns:
            cursor.execute("ALTER TABLE History ADD COLUMN id INTEGER PRIMARY KEY AUTOINCREMENT")
            print("Added missing id column to table History.")
            delay()

        if "chore_id" not in columns:
            cursor.execute("ALTER TABLE History ADD COLUMN chore_id INTEGER")
            print("Added missing chore_id column to table History.")
            delay()

        if "name" not in columns:
            cursor.execute("ALTER TABLE History ADD COLUMN name TEXT")
            print("Added missing name column to table History.")
            delay()

        if "description" not in columns:
            cursor.execute("ALTER TABLE History ADD COLUMN description TEXT")
            print("Added missing description column to table History.")
            delay()

        if "user" not in columns:
            cursor.execute("ALTER TABLE History ADD COLUMN user TEXT")
            print("Added missing user column to table History.")
            delay()

        if "completed" not in columns:
            cursor.execute("ALTER TABLE History ADD COLUMN user TEXT")
            print("Added missing completed column to table History.")
            delay()
        connection.commit()


validate()
