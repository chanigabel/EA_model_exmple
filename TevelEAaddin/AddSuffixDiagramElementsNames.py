#The script, written by Chany Jacobs, 
#This script opens the Add/Remove Suffix dialog box which enables to add/remove 
#suffix to/from element names of the selected diagram which are not locked.

import win32com.client
import tkinter as tk
from tkinter import messagebox

def delete_suffix(selected_diagram, repository, suffix):
    num_locked_elements = 0
    num_add_update_elements = 0

    for cur_object in selected_diagram.DiagramObjects:
        cur_element = repository.GetElementByID(cur_object.ElementID)
        if cur_element.Type.strip() in ["Class", "Interface"]:
            if repository.IsSecurityEnabled:
                if cur_element.Locked:
                    num_locked_elements += 1
                else:
                    cur_element.ApplyUserLock()
                    if cur_element.Name.endswith(suffix):
                        cur_element.Name = cur_element.Name[:-len(suffix)]
                    cur_element.Update()
                    num_add_update_elements += 1
            else:
                if cur_element.Name.endswith(suffix):
                    cur_element.Name = cur_element.Name[:-len(suffix)]
                cur_element.Update()

    if repository.IsSecurityEnabled:
        messagebox.showinfo("Info", f"{num_locked_elements} elements were locked before. {num_add_update_elements} elements were locked and affected by you.")
    else:
        messagebox.showinfo("Info", "Elements updated successfully!")

def add_suffix(selected_diagram, repository, suffix):
    num_locked_elements = 0
    num_add_update_elements = 0

    for cur_object in selected_diagram.DiagramObjects:
        cur_element = repository.GetElementByID(cur_object.ElementID)
        if cur_element.Type.strip() in ["Class", "Interface"]:
            if repository.IsSecurityEnabled:
                if cur_element.Locked:
                    num_locked_elements += 1
                else:
                    cur_element.ApplyUserLock()
                    cur_element.Name += suffix
                    cur_element.Update()
                    num_add_update_elements += 1
            else:
                cur_element.Name += suffix
                cur_element.Update()

    if repository.IsSecurityEnabled:
        messagebox.showinfo("Info", f"{num_locked_elements} elements were locked before. {num_add_update_elements} elements were locked and affected by you.")
    else:
        messagebox.showinfo("Info", "Elements updated successfully!")

def on_update_suffix_click(selected_diagram, txt_suffix, root, repository, flag):
    suffix = txt_suffix.get().strip()
    if flag == "0":
        add_suffix(selected_diagram, repository, suffix)
    else:
        delete_suffix(selected_diagram, repository, suffix)
    root.destroy()

def suffix_form(selected_diagram, repository, flag):
    root = tk.Tk()
    root.title("Suffix")

    label = tk.Label(root, text="Enter the suffix to be added to/removed from the class names:")
    label.grid(row=0, column=0, padx=10, pady=10)

    txt_suffix = tk.Entry(root)
    txt_suffix.grid(row=1, column=0, padx=10, pady=5)

    btn_update_suffix = tk.Button(root, text="Update suffix", command=lambda: on_update_suffix_click(selected_diagram, txt_suffix, root, repository, flag))
    btn_update_suffix.grid(row=2, column=0, padx=10, pady=10)

    root.mainloop()

def get_selected_diagram(ea_repos):
    selected_diagram = ea_repos.GetTreeSelectedObject()
    if selected_diagram is None:
        messagebox.showwarning("Warning", "Please select a diagram")
    return selected_diagram

def suffix_dialog(rep, flag):
    if rep.IsSecurityEnabled:
        dialog_result = messagebox.askyesno(
            "Tevel EA Addin: Add/Remove Suffix to/from element names",
            "This option opens the Add/Remove Suffix dialog box which enables to add/remove suffix to/from element names of the selected diagram which are not locked.\n\nWould you like to proceed?",
            icon="warning"
        )
    else:
        dialog_result = messagebox.askyesno(
            "Tevel EA Addin: Add/Remove Suffix to/from element names",
            "This option opens the Add/Remove Suffix dialog box which enables to add/remove suffix to/from element names of the selected diagram.\n\nWould you like to proceed?",
            icon="warning"
        )

    if not dialog_result:
        return  # Exit if the user chooses not to proceed

    sel_diagram = get_selected_diagram(rep)
    if sel_diagram:
        suffix_form(sel_diagram, rep, flag)

def main():
    ea = win32com.client.Dispatch("EA.App")
    repository = ea.Repository
    flag = input("enter 0 to add or 1 to remove:")
    suffix_dialog(repository, flag)  # Pass flag value here

if __name__ == "__main__":
    main()
