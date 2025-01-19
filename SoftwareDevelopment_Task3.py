import tkinter as tk
from tkinter import ttk, messagebox
import json

CONTACTS_FILE = "contacts.json"

# Load contacts from file
def load_contacts():
    try:
        with open(CONTACTS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save contacts to file
def save_contacts():
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)

# Add a new contact
def add_contact():
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    email = entry_email.get().strip()

    if not name or not phone or not email:
        messagebox.showerror("Error", "All fields are required!")
        return

    if name in contacts:
        messagebox.showerror("Error", "Contact already exists!")
        return

    contacts[name] = {"phone": phone, "email": email}
    save_contacts()
    update_contact_list()
    clear_entries()
    messagebox.showinfo("Success", f"Contact '{name}' added!")

# Update the contact list
def update_contact_list():
    contact_list.delete(0, tk.END)
    for name in contacts:
        contact_list.insert(tk.END, name)

# View selected contact
def view_contact(event):
    try:
        selected_name = contact_list.get(contact_list.curselection())
        contact = contacts[selected_name]
        entry_name.delete(0, tk.END)
        entry_name.insert(0, selected_name)
        entry_phone.delete(0, tk.END)
        entry_phone.insert(0, contact["phone"])
        entry_email.delete(0, tk.END)
        entry_email.insert(0, contact["email"])
    except tk.TclError:
        pass

# Edit an existing contact
def edit_contact():
    selected_name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    email = entry_email.get().strip()

    if not selected_name or not phone or not email:
        messagebox.showerror("Error", "All fields are required!")
        return

    if selected_name not in contacts:
        messagebox.showerror("Error", "Contact does not exist!")
        return

    contacts[selected_name] = {"phone": phone, "email": email}
    save_contacts()
    update_contact_list()
    clear_entries()
    messagebox.showinfo("Success", f"Contact '{selected_name}' updated!")

# Delete a contact
def delete_contact():
    try:
        selected_name = contact_list.get(contact_list.curselection())
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete '{selected_name}'?"):
            del contacts[selected_name]
            save_contacts()
            update_contact_list()
            clear_entries()
            messagebox.showinfo("Success", f"Contact '{selected_name}' deleted!")
    except tk.TclError:
        messagebox.showerror("Error", "No contact selected!")

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)

# Initialize data
contacts = load_contacts()

root = tk.Tk()
root.title("Contact Manager")

# Input Frame
frame_input = ttk.Frame(root, padding="10")
frame_input.grid(row=0, column=0, padx=10, pady=10)

ttk.Label(frame_input, text="Name:").grid(row=0, column=0, padx=5, pady=5)
entry_name = ttk.Entry(frame_input, width=30)
entry_name.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_input, text="Phone:").grid(row=1, column=0, padx=5, pady=5)
entry_phone = ttk.Entry(frame_input, width=30)
entry_phone.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_input, text="Email:").grid(row=2, column=0, padx=5, pady=5)
entry_email = ttk.Entry(frame_input, width=30)
entry_email.grid(row=2, column=1, padx=5, pady=5)

frame_buttons = ttk.Frame(root, padding="10")
frame_buttons.grid(row=1, column=0, padx=10, pady=10)

ttk.Button(frame_buttons, text="Add Contact", command=add_contact).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(frame_buttons, text="Edit Contact", command=edit_contact).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(frame_buttons, text="Delete Contact", command=delete_contact).grid(row=0, column=2, padx=5, pady=5)
ttk.Button(frame_buttons, text="Clear", command=clear_entries).grid(row=0, column=3, padx=5, pady=5)

# Contact List Frame
frame_list = ttk.Frame(root, padding="10")
frame_list.grid(row=2, column=0, padx=10, pady=10)

ttk.Label(frame_list, text="Contact List:").grid(row=0, column=0, padx=5, pady=5)
contact_list = tk.Listbox(frame_list, height=10, width=50)
contact_list.grid(row=1, column=0, padx=5, pady=5)
contact_list.bind("<<ListboxSelect>>", view_contact)

update_contact_list()

root.mainloop()