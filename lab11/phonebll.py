import psycopg2
import csv
from tabulate import tabulate 

conn = psycopg2.connect(host="localhost", dbname="lab10", user="postgres",
                        password="zhazok07", port=5432)

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS phonebook (
      user_id SERIAL PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      surname VARCHAR(255) NOT NULL, 
      phone VARCHAR(255) NOT NULL
)
""")


def all_records():
        n = input("Input 'name' to search by name, or anything else to search by number: ")
        with conn.cursor() as cursor:
            if n.lower() == "name":
                name=input("input the name: ")
                cursor.execute(f"SELECT * FROM phonebook WHERE name like'{name}%'")
                for row in cursor.fetchall():
                    print(row)
            elif n.lower() == "surname":
                surname=input("input the surname: ")
                cursor.execute(f"SELECT * FROM phonebook WHERE surname like'{name}%'")
                for row in cursor.fetchall():
                    print(row)
            else:
                number = input("Input the number: ")
                cursor.execute(f"SELECT * FROM phonebook WHERE number like'{number}%'")
                for row in cursor.fetchall():
                    print(row)

def call_insert():
    num = int(input("How many users do you want to add? "))
    for i in range(num):
        print(f"\nUser {i+1}:")
        name = input("name: ")
        surname = input("surname: ")
        phone = input("phone: ")
        

        cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", (name, surname, phone))
        conn.commit()
        print("Inserted successfully.")

def query_pagination():
    try:
        page_size = int(input("Enter how many records per page (limit): "))
        page_number = int(input("Enter page number: "))

        offset = (page_number - 1) * page_size

        cur.execute("SELECT * FROM phonebook ORDER BY user_id LIMIT %s OFFSET %s", (page_size, offset))
        rows = cur.fetchall()

        if rows:
            print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt="grid"))
        else:
            print("Not found on this page.")
    except ValueError:
        print("Please enter valid integers for page size and number.")


def insert_data():
    print('Type "csv" or "con" to choose option between uploading csv file or typing from console: ')
    method = input().lower()
    if method == "con":
        name = input("Name: ")
        surname = input("Surname: ")
        phone = input("Phone: ")
        cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", (name, surname, phone))
    elif method == "csv":
        filepath = input("Enter a file path with proper extension: ")
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            for row in reader:
                cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", tuple(row))

def update_data():
    column = input('Type the name of the column that you want to change: ')
    value = input(f"Enter {column} that you want to change: ")
    new_value = input(f"Enter the new {column}: ")
    cur.execute(f"UPDATE phonebook SET {column} = %s WHERE {column} = %s", (new_value, value))
    conn.commit()

def delete_data():
    phone = input('Type phone number which you want to delete: ')
    cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    conn.commit()
    
def query_data():
    column = input("Type the name of the column which will be used for searching data: ")
    value = input(f"Type {column} of the user: ")
    cur.execute(f"SELECT * FROM phonebook WHERE {column} = %s", (value,))
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"]))

def display_data():
    cur.execute("SELECT * from phonebook;")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt='fancy_grid'))

while True:
    print("""
    List of the commands:
    1. Type "i" or "I" in order to INSERT data to the table.
    2. Type "u" or "U" in order to UPDATE data in the table.
    3. Type "q" or "Q" in order to make specific QUERY in the table.
    4. Type "d" or "D" in order to DELETE data from the table.
    5. Type "s" or "S" in order to see the values in the table.
    6. Type "f" or "F" in order to close the program.
    7. Type "8" in order to see all informations about person.
    8. Type "9" in order to add many users by one running code.
    9. Type "p" in order to query with pagination.
    """)

    command = input().lower()

    if command == "i":
        insert_data()
    elif command == "u":
        update_data()
    elif command == "8":
        all_records()
    elif command == "9":
        call_insert()
    elif command == "d":
        delete_data()
    elif command == "q":
        query_data()
    elif command == "s":
        display_data()
    elif command == "p":
        query_pagination()
    elif command == "f":
        break

conn.commit()
cur.close()
conn.close()