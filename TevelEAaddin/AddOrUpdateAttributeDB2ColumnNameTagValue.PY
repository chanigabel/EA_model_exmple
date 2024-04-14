import win32com.client
from tkinter import messagebox

def create_uppercase_table_name(table_name):
    substr = ""
    for char in table_name:
        if char.isupper():
            if substr and substr[-1] != '_':
                substr += '_'
            substr += char
        else:
            substr += char.upper()
    return substr

def add_or_update_tagged_value(element, tag_name, tag_value):
    flag = False
    for tagged_value in element.TaggedValues:
        if tagged_value.Name == tag_name:
            tagged_value.Value = tag_value
            tagged_value.Update()
            flag = True
            break

    if not flag:
        new_tag = element.TaggedValues.AddNew(tag_name, 'String')
        new_tag.Value = tag_value
        new_tag.Update()

def add_or_update_attr_tag_value_db2_column_name(rep, db_name):
    diagram = rep.GetCurrentDiagram()
    if diagram is None:
        messagebox.showwarning("Diagram Not Found", "Please select a diagram.")
        return

    dialog_result = messagebox.askyesno(
        "Add or Update Attribute DB2ColumnName Tag Value",
        "This option adds or updates DB2ColumnName Tag Value of classes' attributes of the selected diagram. All diagram's classes have to be released prior and will be locked after.\n\nWould you like to proceed?"
    )

    if not dialog_result:
        return

    num_locked_elements = 0
    num_add_update_elements = 0

    for diagram_object in diagram.DiagramObjects:
        element = rep.GetElementByID(diagram_object.ElementID)
        if element is None:
            continue
        
        if element.Locked:
            num_locked_elements += 1
        else:
            num_add_update_elements += 1
            element.ApplyUserLock()
        
            for attribute in element.Attributes:
                new_tag_value = create_uppercase_table_name(attribute.Name)
                add_or_update_tagged_value(attribute, db_name, new_tag_value)

    if rep.IsSecurityEnabled:
        messagebox.showinfo(
            "General Information",
            f"{num_locked_elements} elements were locked before. {num_add_update_elements} elements were locked and affected by you."
        )
    else:
        messagebox.showinfo("Done", "All eligible elements have been processed.")

def main():
    ea = win32com.client.Dispatch("EA.App")
    rep = ea.Repository
    add_or_update_attr_tag_value_db2_column_name(rep, "DB2ColumnName")

if __name__ == "__main__":
    main()
