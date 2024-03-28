#The script, written by Chany Jacobs, 
#This script update Version of Diagram Elements.


import xml.etree.ElementTree as ET
import win32com.client
import tkinter as tk
from tkinter import messagebox

def is_element_locked(element_guid, repository):
    squery = "SELECT UserID FROM t_seclocks WHERE EntityID='" + element_guid + "'"
    result = repository.SQLQuery(squery)
    xml_root = ET.fromstring(result)
    user = xml_root.find(".//UserID")
    return user is not None

def update_phase_version_dialog(rep):
    if rep.IsSecurityEnabled:
        dialog_result = messagebox.askyesno(
            "Tevel EA Addin: Update Phase and Version of Diagram Elements",
            "This option opens the Update Phase and Version dialog box which enables update a phase and a version of the selected diagram's elements which are not locked.\n\nWould you like to proceed?",
            icon="warning"
        )
    else:
        dialog_result = messagebox.askyesno(
            "Tevel EA Addin: Update Phase and Version of Diagram Elements",
            "This option opens the Update Phase and Version dialog box which enables update a phase and a version of the selected diagram's elements.\n\nWould you like to proceed?",
            icon="warning"
        )
    
    if dialog_result:
        sel_diagram = get_selected_diagram(rep)
        if sel_diagram:
            change_phase_version(rep, sel_diagram)

def get_selected_diagram(ea_repos):
    selected_diagram = ea_repos.GetCurrentDiagram()
    if selected_diagram is None:
        messagebox.showwarning("Warning", "Please select a diagram")
    return selected_diagram

def change_phase_version(rep, selected_diagram):
    root = tk.Tk()
    root.title("Update Version")

    label = tk.Label(root, text="Update the Version to:")
    label.grid(row=0, column=0)

    txt_phase_version = tk.Entry(root)
    txt_phase_version.grid(row=0, column=1)

    btn_update = tk.Button(root, text="Update", command=lambda: on_update_click(rep, selected_diagram, txt_phase_version, root))
    btn_update.grid(row=1, column=1)

    root.mainloop()

def on_update_click(rep, selected_diagram, txt_phase_version, root):
    for cur_object in selected_diagram.DiagramObjects:
        cur_element = rep.GetElementByID(cur_object.ElementID)
        if rep.IsSecurityEnabled:
            if not is_element_locked(cur_element.ElementGUID, rep):
                cur_element.ApplyUserLock()
                cur_element.Version = txt_phase_version.get()
                cur_element.Update()
        else:
            cur_element.Version = txt_phase_version.get()
            cur_element.Update()

    rep.RefreshModelView(selected_diagram.DiagramID)
    messagebox.showinfo("Info", "Diagram elements updated successfully!")
    root.destroy()

def main():
    ea = win32com.client.Dispatch("EA.App")
    rep = ea.Repository
    update_phase_version_dialog(rep)

if __name__ == "__main__":
    main()
