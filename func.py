
import sqlite3
import config
import os 
import time


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
                user, TEXT


            );
            '''

            # Execute the SQL command
            cursor.execute(create_table_query)

            # Commit the changes
            connection.commit()

        print(f"Created chores table to {filepath} successfully.")
        delay()

    except Exception as e:
        print(f"Creating database failed: {e}")
        if not os.path.isfile(filepath):
            print("Config database is missing.")

def validate():
    if not os.path.isfile(filepath):
        print("Database file was not found. Creating...")
        createfile()
        func.delay()

    with sqlite3.connect(filepath) as connection:

            # Create a cursor object
        cursor = connection.cursor()

        cursor.execute(""" SELECT name FROM sqlite_master
        WHERE type='table' AND name='Users'
        """)

    if not cursor.fetchone():
        print("Table Users does not exist. Creating...")
        delay()
        createfile()

    with sqlite3.connect(filepath) as connection:

            # Create a cursor object
        cursor = connection.cursor()

        cursor.execute(""" SELECT name FROM sqlite_master
        WHERE type='table' AND name='Chores'
        """)

    if not cursor.fetchone():
        print("Table Chores does not exist. Creating...")
        delay()
        createfile()


    with sqlite3.connect(filepath) as connection:

            # Create a cursor object
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

            # Create a cursor object
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


validate()
