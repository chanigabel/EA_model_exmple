import tkinter as tk
from tkinter import messagebox
import win32com.client
import traceback

def delete_tag_values(repository, element, tags_to_delete):
    """Delete selected tag values from the element."""
    try:
        property_ids_to_delete = [tagged_value.PropertyID for tagged_value in element.TaggedValues if f"{tagged_value.Name}: {tagged_value.Value}" in tags_to_delete]
        
        if property_ids_to_delete:
            ids = ', '.join(map(str, property_ids_to_delete))
            sql = f"DELETE FROM t_objectproperties WHERE PropertyID IN ({ids})"
            repository.Execute(sql)
            element.Update()
            repository.RefreshModelView(0)
    except Exception as e:
        error_details = traceback.format_exc()
        messagebox.showerror("Error", f"Failed to delete tag values: {str(e)}\n\nDetails:\n{error_details}")

def ask_to_delete_tag(tag_info, element_name, package_name):
    """Ask the user if they want to delete each tag, one by one."""
    selected_tags = []

    for tag in tag_info:
        if messagebox.askyesno("Delete Tag?", f"Do you want to delete the tag '{tag}' from '{element_name}' in package '{package_name}'?"):
            selected_tags.append(tag)

    return selected_tags

def process_package(repository, package):
    """Process all elements in the package and its sub-packages."""
    all_selected_tags = {}

    for element in package.Elements:
        if element.Type == "Requirement" and element.TaggedValues.Count > 0:
            tag_info = [f"{tagged_value.Name}: {tagged_value.Value}" for tagged_value in element.TaggedValues]
            if tag_info:
                selected_tags = ask_to_delete_tag(tag_info, element.Name, package.Name)
                if selected_tags:
                    all_selected_tags[element.Name] = selected_tags
    
    for sub_package in package.Packages:
        process_package(repository, sub_package)
    
    if all_selected_tags:
        confirm_and_delete(repository, all_selected_tags)

def confirm_and_delete(repository, all_selected_tags):
    """Confirm with the user and delete selected tags if confirmed."""
    confirm_message = "You have selected the following tags to delete:\n\n"
    for element_name, tags in all_selected_tags.items():
        confirm_message += f"From element '{element_name}':\n"
        confirm_message += '\n'.join(f"  - {tag}" for tag in tags)
        confirm_message += "\n"
    
    confirm_message += "\nAre you sure you want to delete these tags?"

    if messagebox.askyesno("Confirm Deletion", confirm_message):
        for element_name, tags in all_selected_tags.items():
            element = repository.GetElementByGuid(repository.SQLQuery(f"SELECT ea_guid FROM t_object WHERE name='{element_name}'").split("<ea_guid>")[1].split("</ea_guid>")[0])
            delete_tag_values(repository, element, tags)
        messagebox.showinfo("Completed", "Tag values deletion process completed.")
    else:
        messagebox.showinfo("Cancelled", "Tag deletion operation cancelled.")

def main():
    try:
        ea = win32com.client.Dispatch("EA.App")
        repository = ea.Repository
    except Exception as e:
        messagebox.showerror("Error", f"Could not connect to EA: {str(e)}")
        return

    selected_package = repository.GetTreeSelectedPackage()
    if not selected_package:
        messagebox.showerror("Error", "No package selected.")
        return

    process_package(repository, selected_package)

if __name__ == "__main__":
    main()
