
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
                name TEXT

            );
            '''

            # Execute the SQL command
            cursor.execute(create_table_query)

            # Commit the changes
            connection.commit()

        print(f"Created users table to {filepath} successfully.")

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
                deftime TEXT,
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

    except Exception as e:
        print(f"Creating database failed: {e}")
        if not os.path.isfile(filepath):
            print("Config database is missing.")
