import win32com.client
import tkinter as tk
from tkinter import ttk, messagebox
import xml.etree.ElementTree as ET

def is_element_locked(element_guid, repository):
    squery = "SELECT UserID FROM t_seclocks WHERE EntityID='" + element_guid + "'"
    result = repository.SQLQuery(squery)
    xml_root = ET.fromstring(result)
    user = xml_root.find(".//UserID")
    return user is not None

def change_stereotype(rep, stereotype_name):
    sel_diagram = rep.GetCurrentDiagram()
    if sel_diagram is None:
        print("Please select a diagram.")
        return
    
    locked_classes_count = 0
    
    for diagram_object in sel_diagram.DiagramObjects:
        element = rep.GetElementByID(diagram_object.ElementID)
        if element.Type == "Class":
            if rep.IsSecurityEnabled and is_element_locked(element.ElementGUID, rep):
                locked_classes_count += 1
            else:
                element.StereotypeEx = stereotype_name
                element.Stereotype = stereotype_name
                element.Update()

    if locked_classes_count > 0:
        messagebox.showwarning("Tevel Addins: Change classes stereotype", f"{locked_classes_count} classes were locked and your changes did not affect them.")
    else:
        messagebox.showinfo("Tevel Addins: Change classes stereotype", "It's done!")

def on_selection_changed(rep, root, combo_stereotypes):
    selected_stereotype = combo_stereotypes.get()
    change_stereotype(rep, selected_stereotype)
    root.destroy()

def main():
    ea = win32com.client.Dispatch("EA.App")
    rep = ea.Repository

    # Ask user for confirmation using message box
    if rep.IsSecurityEnabled:
        dialog_result = messagebox.askyesno(
            "Tevel EA Addin: Change classes stereotype",
            "This option changes stereotype of all diagram's classes. All diagram's classes have to be released prior and will be locked after.\n\nWould you like to proceed?",
            icon="warning"
        )
    else:
        dialog_result = messagebox.askyesno(
            "Tevel EA Addin: Change classes stereotype",
            "This option changes stereotype of all diagram's classes.\n\nWould you like to proceed?",
            icon="warning"
        )
    
    if dialog_result:
        root = tk.Tk()
        root.title("Change Stereotype")

        ttk.Label(root, text="Select Stereotype:").pack()

        stereotype_options = ["", "Annotations", "XMLAnnotations"]
        selected_stereotype = tk.StringVar(root)
        selected_stereotype.set(stereotype_options[0])  # Default value
        combo_stereotypes = ttk.Combobox(root, textvariable=selected_stereotype, values=stereotype_options)
        combo_stereotypes.pack()

        combo_stereotypes.bind("<<ComboboxSelected>>", lambda event: on_selection_changed(rep, root, combo_stereotypes))

        root.mainloop()

        rep.Models.Refresh()
        rep.RefreshModelView(0)

if __name__ == "__main__":
    main()
