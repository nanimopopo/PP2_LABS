import psycopg2
import csv

conn = psycopg2.connect(
    dbname="phonebook_db",
    user="postgres",
    password="sheesh2006inet",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS phonebook (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE,
    phone VARCHAR(20)
)
""")
conn.commit()

cur.execute("""
CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT id, name, phone FROM phonebook
    WHERE name ILIKE '%' || pattern || '%' OR phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;
""")
conn.commit()

cur.execute("""
CREATE OR REPLACE PROCEDURE insert_or_update_user(user_name TEXT, user_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = user_name) THEN
        UPDATE phonebook SET phone = user_phone WHERE name = user_name;
    ELSE
        INSERT INTO phonebook (name, phone) VALUES (user_name, user_phone);
    END IF;
END;
$$
""")
conn.commit()

cur.execute("""
CREATE OR REPLACE PROCEDURE insert_many_users(names TEXT[], phones TEXT[])
LANGUAGE plpgsql
AS $$
DECLARE
    i INT := 1;
    wrong_data TEXT := '';
BEGIN
    WHILE i <= array_length(names, 1) LOOP
        BEGIN
            IF names[i] IS NULL OR phones[i] IS NULL OR length(phones[i]) < 5 THEN
                wrong_data := wrong_data || '(' || COALESCE(names[i], 'NULL') || ', ' || COALESCE(phones[i], 'NULL') || '), ';
            ELSE
                CALL insert_or_update_user(names[i], phones[i]);
            END IF;
        EXCEPTION
            WHEN OTHERS THEN
                wrong_data := wrong_data || '(' || COALESCE(names[i], 'NULL') || ', ' || COALESCE(phones[i], 'NULL') || '), ';
        END;
        i := i + 1;
    END LOOP;
    IF wrong_data != '' THEN
        RAISE NOTICE 'Incorrect data: %', wrong_data;
    END IF;
END;
$$
""")
conn.commit()

cur.execute("""
CREATE OR REPLACE FUNCTION get_contacts_paginated(limit_num INT, offset_num INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT id, name, phone FROM phonebook
    ORDER BY id
    LIMIT limit_num OFFSET offset_num;
END;
$$ LANGUAGE plpgsql;
""")
conn.commit()

cur.execute("""
CREATE OR REPLACE PROCEDURE delete_contact(value TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook WHERE name = value OR phone = value;
END;
$$
""")
conn.commit()

while True:
    print("\nMenu:")
    print("1. Add or update contact")
    print("2. Add multiple contacts by CSV")
    print("3. Redact contact")
    print("4. Find contact")
    print("5. Delete contact")
    print("6. Show all phonebook")
    print("7. Show paginated phonebook")
    print("0. Quit")

    choice = input("Choose the num: ")

    if choice == "1":
        name = input("Name: ")
        phone = input("Number: ")
        cur.execute("CALL insert_or_update_user(%s, %s)", (name, phone))
        conn.commit()
        print("Successful!")

    elif choice == "2":
        filename = input("CSV file name: ")
        try:
            names = []
            phones = []
            with open(filename, 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    names.append(row[0])
                    phones.append(row[1])
            cur.execute("CALL insert_many_users(%s, %s)", (names, phones))
            conn.commit()
            print("Successful!")
        except Exception as e:
            print("Error:", e)

    elif choice == "3":
        name = input("Name to change: ")
        new_phone = input("New number: ")
        cur.execute("CALL insert_or_update_user(%s, %s)", (name, new_phone))
        conn.commit()
        print("Successful!")

    elif choice == "4":
        keyword = input("Name or number to find: ")
        cur.execute("SELECT * FROM search_contacts(%s)", (keyword,))
        results = cur.fetchall()
        if results:
            for row in results:
                print(f"{row[1]}: {row[2]}")
        else:
            print("Nothing found")

    elif choice == "5":
        value = input("Name or number to delete: ")
        cur.execute("CALL delete_contact(%s)", (value,))
        conn.commit()
        print("Deleted")

    elif choice == "6":
        cur.execute("SELECT * FROM phonebook")
        contacts = cur.fetchall()
        if contacts:
            for row in contacts:
                print(f"{row[1]}: {row[2]}")
        else:
            print("Empty")

    elif choice == "7":
        limit = int(input("Limit: "))
        offset = int(input("Offset: "))
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
        contacts = cur.fetchall()
        if contacts:
            for row in contacts:
                print(f"{row[1]}: {row[2]}")
        else:
            print("No contacts at this page")

    elif choice == "0":
        print("Quit")
        break

    else:
        print("Choose again")

cur.close()
conn.close()
