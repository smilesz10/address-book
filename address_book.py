import sqlite3
from tkinter import *
from tkinter import messagebox

# Connect to the database (or create a new one if it doesn't exist)
conn = sqlite3.connect('contacts_book.db')
# Create a cursor object to interact with the database
cursor = conn.cursor()


# Define a function to create the table (called once)
def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                    name text,
                    phone_number text,
                    address text
                    )''')
    conn.commit()


create_table()  # Call the function to create the table (if needed)


# initializing window
window = Tk()
window.geometry('750x600')
window.config(bg="lightblue")
window.title("contact book")

Name = StringVar()
Number = StringVar()
Address = StringVar()
SearchTerm = StringVar()

# creating frame
frame = Frame(window)
frame.pack(side=RIGHT)

scroll = Scrollbar(frame, orient=VERTICAL)
select = Listbox(frame, yscrollcommand=scroll.set, font=("Times new roman", 16),
                 bg="#f0fffc", width=20, height=20, borderwidth=3, relief="groove")
scroll.config(command=select.yview)
scroll.pack(side=RIGHT, fill=Y)
select.pack(side=LEFT, fill=BOTH, expand=1)


# function to select
def Selected():
    if len(select.curselection()) == 0:
        messagebox.showerror("Error", "Please select the name")
        return None  # Indicate no selection made (optional)
    else:
        return int(select.curselection()[0])


# adding contact and editing
def Addcontact():
    if Name.get() != "" and Number.get() != "" and Address.get() != "":
        # Insert data into the table
        cursor.execute('INSERT INTO contacts VALUES (?, ?, ?)', (Name.get(), Number.get(), Address.get()))
        conn.commit()
        Select_set()
        # Use showinfo for success messages
        messagebox.showinfo("Confirmation", "Successfully Added New Contact")
    else:
        messagebox.showerror("Error", "Please fill the information")


def UpdateDetail():
    if Name.get() and Number.get():
        selected_index = Selected()
        if selected_index is not None:
            cursor.execute("UPDATE contacts SET name = ?, phone_number = ?, address = ? WHERE rowid = ?",
                           (Name.get(), Number.get(), Address.get(), selected_index + 1))
            conn.commit()
            messagebox.showinfo("Confirmation", "Successfully Updated Contact")
            EntryReset()
            Select_set()
        else:
            messagebox.showerror("Error", "Please select a contact to update")
    else:
        messagebox.showerror("Error", "Please fill the information")


def Delete_Entry():
    selected_index = Selected()
    if selected_index is not None:
        result = messagebox.askyesno('confirmation', 'You want to delete contact which you select')
        if True == result:
            # Delete data from the table based on selected contact
            cursor.execute("DELETE FROM contacts WHERE rowid = ?", (selected_index + 1,))
            conn.commit()
            Select_set()
    else:
        messagebox.showerror("Error", "Please select contact")


def VIEW():
    selected_index = Selected()
    if selected_index is not None:
        # Fetch data from the table based on selected contact
        cursor.execute("SELECT * FROM contacts WHERE rowid = ?", (selected_index + 1,))
        row = cursor.fetchone()
        if row:
            NAME, PHONE, ADDRESS = row
            Name.set(NAME)
            Number.set(PHONE)
            Address.set(ADDRESS)
        else:
            messagebox.showerror("Error", "No contact found")
    else:
        messagebox.showerror("Error", "Please select a contact to view")


def SearchContact():
    search_term = SearchTerm.get()
    Select_set(search_term)  # Call Select_set with search term


# EXITING THE GAME WINDOW
def EXIT():
    window.destroy()


def Select_set(search_term=None):
    # Clear the listbox for a new search
    select.delete(0, END)

    # If a search term is provided, use it to filter the results
    if search_term:
        search_terms = search_term.split()  # Split the search term into separate words
        search_query = " OR ".join(["name LIKE ?"] * len(search_terms))  # Create OR conditions

        # Prepare placeholders and search terms
        placeholders = ["%" + term for term in search_terms]
        cursor.execute(f"SELECT * FROM contacts WHERE {search_query}", placeholders)
    else:
        cursor.execute("SELECT * FROM contacts")

    for row in cursor.fetchall():
        name, phone_number, address = row
        select.insert(END, name)  # Directly update the listbox


Select_set()


def EntryReset():

    Name.set("")
    Number.set("")
    Address.set("")


# buttons
Label(window, text='Name', font=("Times new roman", 22, "bold"), bg='SlateGray3').place(x=30, y=20)
Entry(window, textvariable=Name, width=30).place(x=200, y=30)
Label(window, text='Contact no:', font=("Times new roman", 20, "bold"), bg='SlateGray3').place(x=30, y=70)
Entry(window, textvariable=Number, width=30).place(x=200, y=80)
Label(window, text='Address:', font=("Times new roman", 20, "bold"), bg='SlateGray3').place(x=30, y=120)
Entry(window, textvariable=Address, width=30).place(x=200, y=130)
search_label = Label(window, text="Search:", font=("Times new roman", 12))
search_label.place(x=30, y=510)
search_entry = Entry(window, textvariable=SearchTerm, width=20)
search_entry.place(x=100, y=510)


Button(window, text="ADD", font='Helvetica 18 bold', bg='yellow', command=Addcontact, padx=20).place(x=50, y=190)
Button(window, text="EDIT", font='Helvetica 18 bold', bg='yellow', command=UpdateDetail, padx=20).place(x=50, y=260)
Button(window, text="DELETE", font='Helvetica 18 bold', bg='yellow', command=Delete_Entry, padx=20).place(x=50, y=320)
Button(window, text="VIEW", font='Helvetica 18 bold', bg='yellow', command=VIEW).place(x=50, y=385)
Button(window, text="RESET", font='Helvetica 18 bold', bg='yellow', command=EntryReset).place(x=50, y=450)
Button(window, text="EXIT", font='Helvetica 18 bold', bg='tomato', command=EXIT).place(x=250, y=540)
search_button = Button(window, text="Search", font='Helvetica 10 bold', bg='lightblue', command=SearchContact)
search_button.place(x=230, y=510)

window.mainloop()
