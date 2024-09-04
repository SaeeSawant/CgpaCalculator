import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('student_marks1.db')
cursor = conn.cursor()

# Create a table to store student marks
cursor.execute('''
    CREATE TABLE IF NOT EXISTS student (
        sapid INTEGER PRIMARY KEY,
        subject1 INTEGER,
        subject2 INTEGER,
        subject3 INTEGER,
        subject4 INTEGER,
        subject5 INTEGER,
        credits1 INTEGER,
        credits2 INTEGER,
        credits3 INTEGER,
        credits4 INTEGER,
        credits5 INTEGER
    )
''')
conn.commit()

def map_marks_to_value(marks):
    if 80 < marks <= 90:
        return 9
    elif 90 < marks <= 100:
        return 10
    elif 70 < marks <=80:
        return 8
    elif 60 < marks <=70:
        return 7
    elif 50 < marks <=60:
        return 6
    elif 40 < marks <=50:
        return 5
    else:
        result_label.config(text="Student Failed in a Subject")

# Function to insert student marks into the database
def insert_marks(sapid, subj1, subj2, subj3, subj4, subj5, cred1, cred2, cred3, cred4, cred5):
    subj1 = map_marks_to_value(subj1)
    subj2 = map_marks_to_value(subj2)
    subj3 = map_marks_to_value(subj3)
    subj4 = map_marks_to_value(subj4)
    subj5 = map_marks_to_value(subj5)
    cursor.execute('''
        INSERT INTO student (sapid, subject1, subject2, subject3, subject4, subject5, 
                             credits1, credits2, credits3, credits4, credits5)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (sapid, subj1, subj2, subj3, subj4, subj5, cred1, cred2, cred3, cred4, cred5))
    conn.commit()

# Function to calculate SGPA based on marks and credits
def calculate_sgpa(sapid):
    cursor.execute('SELECT * FROM student WHERE sapid = ?', (sapid,))
    data = cursor.fetchone()

    if data:
        total_credits = data[6] + data[7] + data[8] + data[9] + data[10]
        total_points = (data[1]*data[6] + data[2]*data[7] + data[3]*data[8] + data[4]*data[9] + data[5]*data[10])

        sgpa = total_points / total_credits
        messagebox.showinfo('SGPA', f'SGPA for SAPID {sapid}: {sgpa:.2f}')
    else:
        messagebox.showerror('Error', 'SAPID not found in the database.')

# Function to delete data for a SAPID from the database
def delete_data(sapid):
    cursor.execute('DELETE FROM student WHERE sapid = ?', (sapid,))
    conn.commit()
    messagebox.showinfo('Success', f'Data for SAPID {sapid} deleted.')

# GUI
def submit():
    sapid = int(entry_sapid.get())
    subj1 = int(entry_subj1.get())
    subj2 = int(entry_subj2.get())
    subj3 = int(entry_subj3.get())
    subj4 = int(entry_subj4.get())
    subj5 = int(entry_subj5.get())
    cred1 = int(entry_cred1.get())
    cred2 = int(entry_cred2.get())
    cred3 = int(entry_cred3.get())
    cred4 = int(entry_cred4.get())
    cred5 = int(entry_cred5.get())

    insert_marks(sapid, subj1, subj2, subj3, subj4, subj5, cred1, cred2, cred3, cred4, cred5)
    messagebox.showinfo('Success', 'Marks inserted into the database.')

def fetch_sgpa():
    sapid = int(entry_sapid_sgpa.get())
    calculate_sgpa(sapid)

def delete_data_button():
    sapid = int(entry_sapid_delete.get())
    delete_data(sapid)

# Main GUI window
root = tk.Tk()
root.title('SGPA Calculator')

# Entry fields for inserting marks
label_sapid = tk.Label(root, text='SAP Identification No.:')
label_sapid.grid(row=0, column=1, padx=5, pady=5)
entry_sapid = tk.Entry(root)
entry_sapid.grid(row=0, column=2, padx=5, pady=5)

label_subj1 = tk.Label(root, text='MATHS:')
label_subj1.grid(row=1, column=0, padx=5,pady=5)
entry_subj1 = tk.Entry(root)
entry_subj1.grid(row=1, column=1, padx=5, pady=5)

# ... (similar entry fields for other subjects and credits)
label_subj2 = tk.Label(root, text='OS:')
label_subj2.grid(row=2, column=0, padx=5, pady=5)
entry_subj2 = tk.Entry(root)
entry_subj2.grid(row=2, column=1, padx=5, pady=5)

label_subj3 = tk.Label(root, text='DS:')
label_subj3.grid(row=3, column=0, padx=5, pady=5)
entry_subj3 = tk.Entry(root)
entry_subj3.grid(row=3, column=1, padx=5, pady=5)

label_subj4 = tk.Label(root, text='DBMS:')
label_subj4.grid(row=4, column=0, padx=5, pady=5)
entry_subj4 = tk.Entry(root)
entry_subj4.grid(row=4, column=1, padx=5, pady=5)

label_subj5 = tk.Label(root, text='PYTHON:')
label_subj5.grid(row=5, column=0, padx=5, pady=5)
entry_subj5 = tk.Entry(root)
entry_subj5.grid(row=5, column=1, padx=5, pady=5)

label_cred1 = tk.Label(root, text='MATHS CREDITS:')
label_cred1.grid(row=1, column=3, padx=5, pady=5)
entry_cred1 = tk.Entry(root)
entry_cred1.grid(row=1, column=4, padx=5, pady=5)

label_cred2 = tk.Label(root, text='OS CREDITS:')
label_cred2.grid(row=2, column=3, padx=5, pady=5)
entry_cred2 = tk.Entry(root)
entry_cred2.grid(row=2, column=4, padx=5, pady=5)

label_cred3 = tk.Label(root, text='DS CREDITS:')
label_cred3.grid(row=3, column=3, padx=5, pady=5)
entry_cred3 = tk.Entry(root)
entry_cred3.grid(row=3, column=4, padx=5, pady=5)

label_cred4 = tk.Label(root, text='DBMS CREDITS:')
label_cred4.grid(row=4, column=3, padx=5, pady=5)
entry_cred4 = tk.Entry(root)
entry_cred4.grid(row=4, column=4, padx=5, pady=5)

label_cred5 = tk.Label(root, text='PYTHON CREDITS:')
label_cred5.grid(row=5, column=3, padx=5, pady=5)
entry_cred5 = tk.Entry(root)
entry_cred5.grid(row=5, column=4, padx=5, pady=5)

# Button to delete data
label_sapid_delete = tk.Label(root, text='Enter SAPID to delete:')
label_sapid_delete.grid(row=10, column=1, padx=5, pady=5)
entry_sapid_delete = tk.Entry(root)

entry_sapid_delete.grid(row=10, column=2, padx=5, pady=5)
delete_button = tk.Button(root, text='Delete Data', command=delete_data_button)

delete_button.grid(row=11, column=2, padx=5, pady=5)

submit_button = tk.Button(root, text='Submit', command=submit)
submit_button.grid(row=7, column=2, padx=5, pady=5)

# Entry field for fetching SGPA
label_sapid_sgpa = tk.Label(root, text='Enter SAPID for SGPA:')
label_sapid_sgpa.grid(row=8, column=1, padx=5, pady=5)
entry_sapid_sgpa = tk.Entry(root)
entry_sapid_sgpa.grid(row=8, column=2, padx=5, pady=5)

fetch_sgpa_button = tk.Button(root, text='Fetch SGPA', command=fetch_sgpa)
fetch_sgpa_button.grid(row=9, column=2, padx=5, pady=5)

root.mainloop()

# Close the database connection when the program exits
conn.close()
