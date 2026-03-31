import csv
from connect import connect


def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name TEXT,
            phone TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("Table created")


def insert_from_csv():
    conn = connect()
    cur = conn.cursor()

    with open("contacts.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            name = row[0]
            phone = row[1]

            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (name, phone)
            )

    conn.commit()
    conn.close()
    print("Data added from CSV")



def insert_manual():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    conn.close()
    print("Contact added")



def update_contact():
    name = input("Enter name to update: ")
    print("1 - update number")
    print("2 - update name")

    choice = int(input("Choice: "))

    conn = connect()
    cur = conn.cursor()

    if choice == 1:
        new_phone = input("Enter new phone: ")

        cur.execute(
            "UPDATE phonebook SET phone = %s WHERE name = %s",
            (new_phone, name)
        )

        print("Contact number updated")


    elif choice == 2:
        new_name = input("Enter new name: ")

        cur.execute(
            "UPDATE phonebook SET name = %s WHERE name = %s",
            (new_name, name)
        )

        print("Contact name updated")

    
    conn.commit()
    cur.close()
    conn.close()


def search_contacts():
    print("1 - search by name")
    print("2 - search by phone prefix")

    choice = input("Choose: ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name: ")

        cur.execute(
            "SELECT * FROM phonebook WHERE name ILIKE %s",
            (f"%{name}%",)
        )

    elif choice == "2":
        prefix = input("Enter phone prefix: ")

        cur.execute(
            "SELECT * FROM phonebook WHERE phone LIKE %s",
            (f"{prefix}%",)
        )

    else:
        print("Wrong choice")
        return

    results = cur.fetchall()

    # вывод
    if results:
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("No results found")

    conn.close()



def delete_contact():
    value = input("Enter name or phone to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM phonebook WHERE name = %s OR phone = %s",
        (value, value)
    )

    conn.commit()
    conn.close()
    print("Deleted")



def menu():
    while True:
        print("\n--- PHONEBOOK ---")
        print("1. Create table")
        print("2. Insert from CSV")
        print("3. Insert manually")
        print("4. Update")
        print("5. Search")
        print("6. Delete")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            create_table()

        elif choice == "2":
            insert_from_csv()

        elif choice == "3":
            insert_manual()

        elif choice == "4":
            update_contact()

        elif choice == "5":
            search_contacts()

        elif choice == "6":
            delete_contact()

        elif choice == "0":
            break

        else:
            print("Invalid choice")


# запуск
menu()