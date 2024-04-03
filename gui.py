import tkinter as tk
from tkinter import messagebox
import psycopg2
import os
import credentials as cred

def add_user():
    name = name_entry.get()
    email = email_entry.get()
    company = company_entry.get()
    dbname=cred.dbname
    user=cred.user
    password=cred.password

    try:
        connection = psycopg2.connect(
            dbname = dbname,
            user= user,
            password = password,
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()

        insert_query = "INSERT INTO hr_info (name, email, company) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (name, email, company))
        connection.commit()

        messagebox.showinfo("Success", "User added successfully")

    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Error adding user: {e}")

    finally:
        if connection:
            connection.close()
    clear_entries()

def clear_entries():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    company_entry.delete(0, tk.END)

# GUI setup
root = tk.Tk()
root.title("Add HR details")

# Labels
tk.Label(root, text="Name:").grid(row=0, column=0, padx=5, pady=5)
tk.Label(root, text="Email:").grid(row=1, column=0, padx=5, pady=5)
tk.Label(root, text="Company:").grid(row=2, column=0, padx=5, pady=5)

# Entry fields
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=5, pady=5)
email_entry = tk.Entry(root)
email_entry.grid(row=1, column=1, padx=5, pady=5)
company_entry = tk.Entry(root)
company_entry.grid(row=2, column=1, padx=5, pady=5)

# Add button
add_button = tk.Button(root, text="Add HR details", command=add_user)
add_button.grid(row=3, column=0, padx=5, pady=10)

add_new_button = tk.Button(root, text="Add New", command=clear_entries)
add_new_button.grid(row=3, column=1, padx=5, pady=10)


root.mainloop()
