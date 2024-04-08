import win32com.client
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog

def search_for_duplicates(repository):
    selected_package = repository.GetTreeSelectedPackage()
    if not selected_package:
        messagebox.showwarning("Package Not Found", "Please select a package for the duplicates search.")
        return

    duplicates_list = []
    list_subpackages = [selected_package]
    find_subpackages(selected_package, list_subpackages)

    for cur_package in list_subpackages:
        for cur_element in cur_package.Elements:
            if cur_element.Type in ["Class", "Interface", "Enumeration"]:
                list_duplicates = [p for p in cur_package.Elements if p.Name == cur_element.Name and p.Type == cur_element.Type]
                if len(list_duplicates) > 1:
                    package_name = repository.GetPackageByID(cur_element.PackageID).Name
                    duplicates_list.append((cur_element.Name, cur_element.Type, package_name, cur_element.ElementID))

    duplicates_search_window = tk.Tk()
    duplicates_search_window.title("Search for Duplicates")
    duplicates_search_window.geometry("800x600")

    tk.Label(duplicates_search_window, text="Element Name - Type - Package - ID").pack(padx=10, pady=5)

    duplicates_listbox = tk.Listbox(duplicates_search_window)
    duplicates_listbox.pack(expand=True, fill='both', padx=10, pady=10)

    for name, element_type, package_name, element_id in duplicates_list:
        item_text = f"{name} - {element_type} - {package_name} - {element_id}"
        duplicates_listbox.insert(tk.END, item_text)

    btn_open = ttk.Button(duplicates_search_window, text="Open", command=lambda: open_selected(repository, duplicates_listbox))
    btn_open.pack(side=tk.RIGHT, padx=10, pady=5)

    btn_close = ttk.Button(duplicates_search_window, text="Close", command=duplicates_search_window.destroy)
    btn_close.pack(side=tk.RIGHT, padx=10, pady=5)

    btn_save = ttk.Button(duplicates_search_window, text="Save to File", command=lambda: save_to_file(duplicates_list))
    btn_save.pack(side=tk.RIGHT, padx=10, pady=5)

    duplicates_search_window.mainloop()

def find_subpackages(cur_package, list_subpackages):
    for sub_package in cur_package.Packages:
        if sub_package not in list_subpackages:
            list_subpackages.append(sub_package)
            find_subpackages(sub_package, list_subpackages)

def open_selected(repository, listbox):
    selected_index = listbox.curselection()
    if selected_index:
        selected_item = listbox.get(selected_index[0])
        element_id = selected_item.split(" - ")[3]
        element_com = repository.GetElementByID(int(element_id))  # Convert to COM object
        repository.ShowInProjectView(element_com)  # Pass the COM object to ShowInProjectView

def save_to_file(duplicates_list):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, 'w') as file:
            for name, element_type, package_name, _ in duplicates_list:
                file.write(f"{name}, {element_type}, {package_name}\n")

def main():
    ea = win32com.client.Dispatch("EA.App")
    repository = ea.Repository
    search_for_duplicates(repository)

if __name__ == "__main__":
    main()
