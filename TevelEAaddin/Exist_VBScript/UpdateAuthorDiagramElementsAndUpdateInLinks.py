#The script, written by Chany Jacobs, 
#This script updating the Author of Diagram Elements, and to the sub diagrams too. (links for diagrams)

import win32com.client
import tkinter as tk
from tkinter import messagebox
# Import module for parsing XML data
import xml.etree.ElementTree as ET

# Function to check if an element is locked by another user in the repository
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

# Function to create dialog box interface for updating author
def change_author(rep, selected_Diagram):

    root = tk.Tk()  # Create Tkinter root window
    root.title("Update author")  # Set title for the window

    # Create labels and entry fields for author information
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

# Function to retrieve linked diagrams for the currently selected diagram
def get_all_links_in_current_diagram(rep, selected_Diagram):
    # Construct the SQL query to retrieve linked diagrams (PDATA1) for the selected diagram
    squery = f"SELECT PDATA1 FROM t_object INNER JOIN t_diagramobjects ON t_object.Object_ID = t_diagramobjects.Object_ID WHERE t_diagramobjects.Diagram_ID = {int(selected_Diagram.DiagramID)} AND PDATA1 IS NOT NULL"
    # Execute the SQL query and retrieve the result
    #`result = ET.ElementTree(ET.fromstring(rep.SQLQuery(squery)))`-
    # creates an ElementTree object (`result`) from the XML data obtained by executing the SQL query 
    # against the Enterprise Architect repository. 
    # This ElementTree object can then be used to traverse and extract information from the XML document in a structured manner.
    result = ET.ElementTree(ET.fromstring(rep.SQLQuery(squery)))
    # Get the root element of the XML result
    root = result.getroot()
    # Extract the values of PDATA1 (linked diagram IDs) from the XML result
    pdata1_values = [element.text for element in root.findall(".//PDATA1")]
    # Return the pdata1_values as a list
    return [pdata1_values]

def on_update_click_author(rep, selected_Diagram, txt_to_author, txt_from_author, root,level=0):
    pdata1_values=[]
    if level==0:# If top level (in the select diagram and not in sub diagram), get linked diagrams
        pdata1_values = get_all_links_in_current_diagram(rep, selected_Diagram)
    update_author(rep, selected_Diagram, txt_to_author, txt_from_author, root, pdata1_values,level)

def update_author(rep, selected_Diagram, txt_to_author, txt_from_author, root, pdata1_values,level):
    for cur_object in selected_Diagram.DiagramObjects:
        if str(cur_object.ElementID) not in pdata1_values:
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
    if level == 0:  # If top level, update linked diagrams
        for cur_PDATA1 in pdata1_values[0]:
            if int(cur_PDATA1) > 0:
                # Recursively update author for linked diagrams
                on_update_click_author(rep, rep.GetDiagramByID(int(cur_PDATA1)), txt_to_author, txt_from_author, root,1)
                messagebox.showinfo("Info", f"{rep.GetDiagramByID(int(cur_PDATA1)).Name} Diagram elements updated successfully!")
    if level == 0:  # If top level, destroy root window after all updates
        root.destroy()

def main():
    ea = win32com.client.Dispatch("EA.App")
    rep = ea.Repository
    update_author_dialog(rep)

if __name__ == "__main__":
    main()
