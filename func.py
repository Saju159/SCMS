
import sqlite3
import config
import os 
import time


masterpath=os.path.join(config.getBaseConfigDir(),"scms.db")
filepath=masterpath

def clear():
    os.system('cls' if os.name == 'nt' else "printf '\033c'")


def delay():
    time.sleep(1)

def delaylong():
    time.sleep(2)


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
        cursor.execute("PRAGMA table_info(Users)")
        columns = [row[1] for row in cursor.fetchall()]

        if "deftime" not in columns:
            cursor.execute("ALTER TABLE Users ADD COLUMN deftime TEXT")
            print("Added missing deftime column to table users.")

        if "discord" not in columns:
            cursor.execute("ALTER TABLE Users ADD COLUMN discord TEXT")
            print("Added missing discord column to table users.")

        connection.commit()


validate()