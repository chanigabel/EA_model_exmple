import win32com.client
import tkinter as tk
from tkinter import messagebox

def lock_elements(rep, diagram_id, listbox_locked_elements, locked_elements):
    locked_elements.clear()

    diagram = rep.GetDiagramByID(diagram_id)
    if diagram is None:
        messagebox.showwarning("Diagram Not Found", f"No diagram with the ID '{diagram_id}' was found.")
        return

    for diagram_object in diagram.DiagramObjects:
        element = rep.GetElementByID(diagram_object.ElementID)
        if element is None:
            continue

        # Check if the element is already locked
        if element.Locked:
            locked_elements.append(element.Name)
            # Skip updating the locked element
        else:
            # Apply user lock to the selected element
            element.Locked = True
            if rep.IsSecurityEnabled:
                element.ApplyUserLock()

    # Display all locked elements in the listbox
    listbox_locked_elements.delete(0, tk.END)
    for element_name in locked_elements:
        listbox_locked_elements.insert(tk.END, element_name)

    if locked_elements:
        messagebox.showinfo("Locked Elements", f"{len(locked_elements)} elements are already locked.")
    else:
        messagebox.showinfo("Done", "All eligible elements have been locked.")

def main():
    ea = win32com.client.Dispatch("EA.App")
    rep = ea.Repository
    selected_package = rep.GetTreeSelectedPackage()

    root = tk.Tk()
    root.title("Apply User Lock")

    # Function to retrieve and display diagrams in the selected package
    def display_diagrams():
        selected_package = rep.GetTreeSelectedPackage()
        if selected_package is not None:
            listbox_diagrams.delete(0, tk.END)
            for diagram in selected_package.Diagrams:
                listbox_diagrams.insert(tk.END, diagram.Name)

    tk.Label(root, text="Select Diagram", font=("Arial", 12)).grid(row=0, column=0)
    listbox_diagrams = tk.Listbox(root, selectmode=tk.SINGLE)
    listbox_diagrams.grid(row=1, column=0)

    tk.Label(root, text="Locked Elements", font=("Arial", 12)).grid(row=0, column=1)
    listbox_locked_elements = tk.Listbox(root)
    listbox_locked_elements.grid(row=1, column=1)

    locked_elements = []

    def btnLock_Click():
        selected_index = listbox_diagrams.curselection()
        if not selected_index:
            messagebox.showwarning("No Diagram Selected", "Please select a diagram.")
            return

        diagram_id = selected_package.Diagrams[selected_index[0]].DiagramID
        lock_elements(rep, diagram_id, listbox_locked_elements, locked_elements)

    # Button to lock elements for the selected diagram
    tk.Button(root, text="Lock Elements", 
              command=btnLock_Click).grid(row=2, column=0, columnspan=2)

    # Button to refresh the list of diagrams
    tk.Button(root, text="Refresh Diagrams", 
              command=display_diagrams).grid(row=3, column=0, columnspan=2)
    
    display_diagrams()  # Initial display of diagrams
    
    root.mainloop()

if __name__ == "__main__":
    main()
