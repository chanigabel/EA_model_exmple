import win32com.client
import tkinter as tk
from tkinter import messagebox
import xml.etree.ElementTree as ET

def is_element_locked(element_guid, repository):
    squery = "SELECT UserID FROM t_seclocks WHERE EntityID='" + element_guid + "'"
    result = repository.SQLQuery(squery)
    xml_root = ET.fromstring(result)
    user = xml_root.find(".//UserID")
    return user is not None

def update_author_dialog(rep):
    if rep.IsSecurityEnabled:
        dialog_result = messagebox.askyesno(
            "Tevel EA Addin: Update author of Diagram Elements",
            "This option opens the Update author dialog box which enables updating a author of the selected Diagram's elements which are not locked.\n\nWould you like to proceed?",
            icon="warning"
        )
    else:
        dialog_result = messagebox.askyesno(
            "Tevel EA Addin: Update author of Diagram Elements",
            "This option opens the Update author dialog box which enables updating a author of the selected Diagram's elements.\n\nWould you like to proceed?",
            icon="warning"
        )
    
    if dialog_result:
        sel_Diagram = get_selected_Diagram(rep)
        if sel_Diagram:
            change_author(rep, sel_Diagram)

def get_selected_Diagram(ea_repos):
    selected_Diagram = ea_repos.GetCurrentDiagram()
    if selected_Diagram is None:
        messagebox.showwarning("Warning", "Please select a Diagram")
    return selected_Diagram

def change_author(rep, selected_Diagram):

    root = tk.Tk()
    root.title("Update author")

    label = tk.Label(root, text="Update the Author from:")
    label.grid(row=0, column=0)

    label = tk.Label(root, text="Update the Author to:")
    label.grid(row=1, column=0)

    txt_to_author = tk.Entry(root)
    txt_to_author.grid(row=1, column=1)

    txt_from_author = tk.Entry(root)
    txt_from_author.grid(row=0, column=1)

    btn_update = tk.Button(root, text="Update", command=lambda: on_update_click_author(rep, selected_Diagram, txt_to_author.get(), txt_from_author.get(), root))
    btn_update.grid(row=3, column=1)

    root.mainloop()

def get_all_links_in_current_diagram(rep, selected_Diagram):
    squery = f"SELECT PDATA1 FROM t_object INNER JOIN t_diagramobjects ON t_object.Object_ID = t_diagramobjects.Object_ID WHERE t_diagramobjects.Diagram_ID = {int(selected_Diagram.DiagramID)} AND PDATA1 IS NOT NULL"
    result = ET.ElementTree(ET.fromstring(rep.SQLQuery(squery)))
    root = result.getroot()
    pdata1_values = [element.text for element in root.findall(".//PDATA1")]
    return [pdata1_values]

def on_update_click_author(rep, selected_Diagram, txt_to_author, txt_from_author, root):
    pdata1_values = get_all_links_in_current_diagram(rep, selected_Diagram)
    update_author(rep, selected_Diagram, txt_to_author, txt_from_author, root, pdata1_values)

def update_author(rep, selected_Diagram, txt_to_author, txt_from_author, root, pdata1_values):
 
    for cur_object in selected_Diagram.DiagramObjects:
        cur_element = rep.GetElementByID(cur_object.ElementID)
        if cur_element.Author == txt_from_author:
            if rep.IsSecurityEnabled:
                if not is_element_locked(cur_element.ElementGUID, rep):
                    cur_element.ApplyUserLock()
                    cur_element.Author = txt_to_author
                    cur_element.Update()
            else:
                cur_element.Author = txt_to_author
                cur_element.Update()

    for cur_PDATA1 in pdata1_values[0]:
        if int(cur_PDATA1) > 0:
            linked_diagram = rep.GetDiagramByID(int(cur_PDATA1))
            linked_diagram.Author = txt_to_author
            linked_diagram.Update()
            messagebox.showinfo("Info", f"{linked_diagram.Name} Diagram author updated successfully!")

    
    root.destroy()

def main():
    ea = win32com.client.Dispatch("EA.App")
    rep = ea.Repository
    update_author_dialog(rep)

if __name__ == "__main__":
    main()
