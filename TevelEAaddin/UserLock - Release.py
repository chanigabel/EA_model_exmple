import tkinter as tk
from tkinter import messagebox
import win32com.client
import xml.etree.ElementTree as ET

def load_locked_elements(listbox_locked_elements, repository):
    listbox_locked_elements.delete(0, tk.END)
    locked_elements = get_locked_elements(repository)
    for element in locked_elements:
        listbox_locked_elements.insert(tk.END, element)

def get_locked_elements(repository):
    locked_elements = []
    query = "SELECT t_secuser.FirstName, t_secuser.Surname, t_seclocks.EntityID, t_seclocks.EntityType " \
            "FROM t_secuser INNER JOIN t_seclocks ON t_secuser.UserID = t_seclocks.UserID"

    result = repository.SQLQuery(query)
    if result:
        root = ET.fromstring(result)
        for child in root.findall('.//EntityID'):
            locked_elements.append(child.text.strip())
    return locked_elements

def select_all(listbox_locked_elements):
    listbox_locked_elements.select_set(0, tk.END)

def clear_all(listbox_locked_elements):
    listbox_locked_elements.selection_clear(0, tk.END)

def release_lock(listbox_locked_elements, repository):
    selected_items = listbox_locked_elements.curselection()
    if not selected_items:
        messagebox.showwarning("No Elements Selected", "Please select elements to release the locks.")
        return

    if messagebox.askyesno("Confirm Release", "Are you sure you want to release the locks for the selected elements?"):
        for index in selected_items:
            element_id = listbox_locked_elements.get(index)
            query = f"DELETE FROM t_seclocks WHERE EntityID = '{element_id}'"
            repository.Execute(query)

        load_locked_elements(listbox_locked_elements, repository)
        messagebox.showinfo("Locks Released", "User locks released successfully.")

def release_user_lock(repository):
    root = tk.Tk()
    root.title("Release User Lock")
    root.geometry("500x400")

    listbox_locked_elements = tk.Listbox(root, selectmode=tk.MULTIPLE)
    listbox_locked_elements.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    btn_select_all = tk.Button(root, text="Select All", command=lambda: select_all(listbox_locked_elements))
    btn_select_all.pack()

    btn_clear_all = tk.Button(root, text="Clear All", command=lambda: clear_all(listbox_locked_elements))
    btn_clear_all.pack()

    btn_release = tk.Button(root, text="Release User Lock", command=lambda: release_lock(listbox_locked_elements, repository))
    btn_release.pack()

    load_locked_elements(listbox_locked_elements, repository)

    root.mainloop()

def main():
    ea = win32com.client.Dispatch("EA.App")
    repository = ea.Repository

    dialog_result = messagebox.askyesno("Release User Lock", 
        "This option opens the Release User Lock dialog box which enables releasing User Locks that EA could not release by itself.\n\nWould you like to proceed?")

    if dialog_result:
        release_user_lock(repository)

if __name__ == "__main__":
    main()
