import psycopg2
import csv

conn = psycopg2.connect(
    dbname="phonebook_db",
    user="postgres",
    password="ccffgc",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS phonebook (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20)
)
""")
conn.commit()

while True:
    print("\nMenu:")
    print("1. Add contact")
    print("2. Add contact by CSV")
    print("3. Redact contact")
    print("4. Find contact")
    print("5. Delete contact")
    print("6. Show all phonebook")
    print("0. Quit")

    choice = input("Chose the num: ")

    if choice == "1":
        name = input("Name: ")
        phone = input("Number: ")
        cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
        conn.commit()
        print("Succesful!")

    elif choice == "2":
        filename = input("CSV file name: ")
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (row[0], row[1]))
                conn.commit()
            print("Succesful!")
        except:
            print("Try again")

    elif choice == "3":
        name = input("Name to change: ")
        new_phone = input("New number: ")
        cur.execute("UPDATE phonebook SET phone = %s WHERE name = %s", (new_phone, name))
        conn.commit()
        print("Succesful!")

    elif choice == "4":
        keyword = input("Name to find: ")
        cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s", ('%' + keyword + '%',))
        results = cur.fetchall()
        if results:
            for row in results:
                print(f"{row[1]}: {row[2]}")
        else:
            print("Try again")

    elif choice == "5":
        value = input("Name or number to delete: ")
        cur.execute("DELETE FROM phonebook WHERE name = %s OR phone = %s", (value, value))
        conn.commit()
        print("Deleted")

    elif choice == "6":
        cur.execute("SELECT * FROM phonebook")
        contacts = cur.fetchall()
        if contacts:
            for row in contacts:
                print(f"{row[1]}: {row[2]}")
        else:
            print("Enmpty")

    elif choice == "0":
        print("Quit")
        break

    else:
        print("Chose again")
        
cur.close()
conn.close()