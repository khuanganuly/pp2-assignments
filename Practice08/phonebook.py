import csv
from connect import connect


def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE,
            phone TEXT
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


def create_functions():
    conn = connect()
    cur = conn.cursor()

    with open("functions.sql", "r", encoding="utf-8") as file:
        sql = file.read()
        cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()


def create_procedures():
    conn = connect()
    cur = conn.cursor()

    with open("procedures.sql", "r", encoding="utf-8") as file:
        sql = file.read()
        cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()


def setup_database():
    create_table()
    create_functions()
    create_procedures()
    print("Database is ready")




def insert_manual():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "CALL insert_or_update_user(%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact added or updated")


def insert_many():
    n = int(input("How many contacts: "))

    names = []
    phones = []

    for _ in range(n):
        name = input("Enter name: ")
        phone = input("Enter phone: ")
        names.append(name)
        phones.append(phone)

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "CALL insert_many_users(%s, %s)",
        (names, phones)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Many contacts processed")


def search_contacts():
    pattern = input("Enter pattern: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM search_by_pattern(%s)",
        (pattern,)
    )

    results = cur.fetchall()

    if results:
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("No results found")

    cur.close()
    conn.close()


def show_paginated():
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM get_contacts_paginated(%s, %s)",
        (limit, offset)
    )

    results = cur.fetchall()

    if results:
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("No results found")

    cur.close()
    conn.close()


def delete_contact():
    value = input("Enter name or phone to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "CALL delete_by_name_or_phone(%s)",
        (value,)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Deleted")



def menu():
    while True:
        print("\n--- PHONEBOOK ---")
        print("1. Insert manually")
        print("2. Insert many users")
        print("3. Search by pattern")
        print("4. Show paginated data")
        print("5. Delete")
        print("6. Show all")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            insert_manual()

        elif choice == "2":
            insert_many()

        elif choice == "3":
            search_contacts()

        elif choice == "4":
            show_paginated()

        elif choice == "5":
            delete_contact()

        elif choice == "6":
            show_all()

        elif choice == "0":
            break

        else:
            print("Invalid choice")


setup_database()
menu()