import tkinter as tk
from tkinter import messagebox
import os
import json

CONTACTS_FILE = "contacts.json"

def load_contacts():
    if not os.path.exists(CONTACTS_FILE):
        return []
    with open(CONTACTS_FILE, "r") as file:
        return json.load(file)

def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)

def find_real_index(contact):
    return next(
        (i for i, c in enumerate(contacts)
         if c["name"] == contact["name"]
         and c["phone"] == contact["phone"]
         and c["email"] == contact["email"]),
        None
    )

def refresh_contacts():
    save_contacts(contacts)
    search_var.set("")
    global filtered_contacts
    filtered_contacts = contacts.copy()
    update_listbox()

def add_contact():
    global filtered_contacts
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()
    if name and phone:
        contacts.append({"name": name, "phone": phone, "email": email})
        refresh_contacts()
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter at least Name and Phone.")

def update_contact():
    global filtered_contacts
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        contact_to_update = filtered_contacts[index]

        real_index = find_real_index(contact_to_update)

        if real_index is not None:
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            email = email_entry.get().strip()
            if name and phone:
                contacts[real_index]["name"] = name
                contacts[real_index]["phone"] = phone
                contacts[real_index]["email"] = email
                refresh_contacts()
            else:
                messagebox.showwarning("Input Error", "Please enter at least Name and Phone.")
        else:
            messagebox.showerror("Error", "Could not find contact in main list.")
    else:
        messagebox.showwarning("Selection Error", "Select a contact to update.")

def delete_contact():
    global filtered_contacts
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        contact_to_delete = filtered_contacts[index]

        real_index = find_real_index(contact_to_delete)
        if real_index is not None:
            contacts.pop(real_index)
            refresh_contacts()
        else:
            messagebox.showerror("Error", "Could not find contact in main list.")
    else:
        messagebox.showwarning("Selection Error", "Select a contact to delete.")

def on_select(event):
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        contact = filtered_contacts[index]
        name_entry.delete(0, tk.END)
        name_entry.insert(0, contact["name"])
        phone_entry.delete(0, tk.END)
        phone_entry.insert(0, contact["phone"])
        email_entry.delete(0, tk.END)
        email_entry.insert(0, contact["email"])

def search_contacts(*args):
    global filtered_contacts
    search_term = search_var.get().lower()
    filtered_contacts = [
        contact for contact in contacts
        if search_term in contact["name"].lower()
        or search_term in contact["phone"]
        or search_term in contact["email"].lower()
    ]
    update_listbox()

def update_listbox():
    listbox.delete(0, tk.END)
    for contact in filtered_contacts:
        listbox.insert(tk.END, f"{contact['name']} | {contact['phone']} | {contact['email']}")

# --------------------------
# GUI SETUP
# --------------------------

contacts = load_contacts()
filtered_contacts = contacts.copy()

root = tk.Tk()
root.title("Contact Book")

root.configure(bg="#f0f0f0")
font1 = ("Arial", 11)

tk.Label(root, text="Search:", bg="#f0f0f0", font=font1).grid(row=0, column=0, padx=5, pady=5, sticky="e")
search_var = tk.StringVar()
search_var.trace_add("write", search_contacts)
search_entry = tk.Entry(root, textvariable=search_var, width=30)
search_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2)

tk.Label(root, text="Name:", bg="#f0f0f0", font=font1).grid(row=1, column=0, padx=5, pady=5, sticky="e")
name_entry = tk.Entry(root, width=30)
name_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2)

tk.Label(root, text="Phone:", bg="#f0f0f0", font=font1).grid(row=2, column=0, padx=5, pady=5, sticky="e")
phone_entry = tk.Entry(root, width=30)
phone_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=2)

tk.Label(root, text="Email:", bg="#f0f0f0", font=font1).grid(row=3, column=0, padx=5, pady=5, sticky="e")
email_entry = tk.Entry(root, width=30)
email_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=2)

btn_add = tk.Button(root, text="Add", command=add_contact, width=10, bg="#4CAF50", fg="white")
btn_add.grid(row=4, column=0, padx=5, pady=10)

btn_update = tk.Button(root, text="Update", command=update_contact, width=10, bg="#2196F3", fg="white")
btn_update.grid(row=4, column=1, padx=5, pady=10)

btn_delete = tk.Button(root, text="Delete", command=delete_contact, width=10, bg="#f44336", fg="white")
btn_delete.grid(row=4, column=2, padx=5, pady=10)

listbox = tk.Listbox(root, width=60, font=font1)
listbox.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
listbox.bind('<<ListboxSelect>>', on_select)

update_listbox()

root.mainloop()
