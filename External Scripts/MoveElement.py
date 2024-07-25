#The script, written by Chany Jacobs, last modified - 04/07/24, 
#The script move selected element to selected package

import tkinter as tk
from tkinter import messagebox, ttk
import win32com.client

def move_element(repository, element_id, target_package_id):
    """Move the element to the target package."""
    try:
        repository.Execute(f"UPDATE t_object SET Package_ID = {target_package_id} WHERE Object_ID = {element_id}")
        repository.RefreshModelView(0)
        messagebox.showinfo("Success", "Element moved successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to move element: {str(e)}")

def get_packages(repository):
    """Get the list of packages from the repository."""
    packages = []
    for package in repository.Models:
        packages.append((package.PackageID, package.Name, None))  # Root packages have no parent
        packages.extend(get_sub_packages(package, package.PackageID))
    return packages

def get_sub_packages(parent_package, parent_id):
    """Recursively get sub-packages."""
    sub_packages = []
    for sub_package in parent_package.Packages:
        sub_packages.append((sub_package.PackageID, sub_package.Name, parent_id))
        sub_packages.extend(get_sub_packages(sub_package, sub_package.PackageID))
    return sub_packages

def select_package(packages):
    """Show a window to select a package."""
    def on_select():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No package selected.")
            return
        selected_package_id = tree.set(selected_item, 'id')
        root.destroy()
        root.quit()
        on_selection(selected_package_id)

    root = tk.Tk()
    root.title("Select Target Package")

    tree = ttk.Treeview(root)
    tree["columns"] = ("id",)
    tree.heading("#0", text="Package Name")
    tree.heading("id", text="Package ID")

    # Insert root packages
    for package_id, package_name, parent_id in packages:
        if parent_id is None:
            tree.insert("", "end", text=package_name, values=(package_id,), iid=package_id)
    
    # Insert sub-packages
    for package_id, package_name, parent_id in packages:
        if parent_id is not None:
            tree.insert(parent_id, "end", text=package_name, values=(package_id,), iid=package_id)

    tree.pack()

    button = tk.Button(root, text="Select", command=on_select)
    button.pack()

    root.mainloop()

def on_selection(selected_package_id):
    global target_package_id
    target_package_id = selected_package_id

def main():
    try:
        ea = win32com.client.Dispatch("EA.App")
        repository = ea.Repository
    except Exception as e:
        messagebox.showerror("Error", f"Could not connect to EA: {str(e)}")
        return

    selected_element = repository.GetTreeSelectedObject()
    if not selected_element:
        messagebox.showerror("Error", "No element selected.")
        return

    element_id = selected_element.ElementID

    packages = get_packages(repository)
    select_package(packages)

    if not target_package_id:
        messagebox.showerror("Error", "Target package ID not provided.")
        return

    move_element(repository, element_id, target_package_id)

if __name__ == "__main__":
    target_package_id = None
    main()
