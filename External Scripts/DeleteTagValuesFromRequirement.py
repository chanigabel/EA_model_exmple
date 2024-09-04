import tkinter as tk
from tkinter import messagebox
import win32com.client
import traceback

def delete_tag_values(repository, element, tags_to_delete):
    """Delete selected tag values from the element."""
    try:
        # Collect all PropertyIDs that need to be deleted
        property_ids_to_delete = [tagged_value.PropertyID for tagged_value in element.TaggedValues if f"{tagged_value.Name}: {tagged_value.Value}" in tags_to_delete]
        
        if property_ids_to_delete:
            # Create a SQL command to delete all selected tagged values in one go
            ids = ', '.join(map(str, property_ids_to_delete))
            sql = f"DELETE FROM t_objectproperties WHERE PropertyID IN ({ids})"
            repository.Execute(sql)
            element.Update()
            repository.RefreshModelView(0)
    except Exception as e:
        error_details = traceback.format_exc()
        messagebox.showerror("Error", f"Failed to delete tag values: {str(e)}\n\nDetails:\n{error_details}")

def show_checklist(tag_info, element_name, package_name):
    """Show a checklist to select tag names to delete, with an option to cancel."""
    selected_tags = []
    canceled = False

    def on_ok():
        for i, var in enumerate(vars):
            if var.get():
                selected_tags.append(tag_info[i])
        root.quit()

    def on_cancel():
        nonlocal canceled
        canceled = True
        root.quit()

    root = tk.Tk()
    root.title(f"Select Tag Values to Delete from '{element_name}'")

    vars = []
    label = tk.Label(root, text=f"Which tag values from '{element_name}' in package '{package_name}' do you want to delete?")
    label.pack()

    for tag in tag_info:
        var = tk.BooleanVar()
        chk = tk.Checkbutton(root, text=tag, variable=var)
        chk.pack(anchor=tk.W)
        vars.append(var)

    button_ok = tk.Button(root, text="OK", command=on_ok)
    button_ok.pack(side=tk.LEFT, padx=5, pady=5)

    button_cancel = tk.Button(root, text="Cancel", command=on_cancel)
    button_cancel.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()
    if root:
        root.destroy()

    if canceled:
        return None  # Return None if the operation was canceled
    return selected_tags

def process_package(repository, package):
    """Process all elements in the package and its sub-packages."""
    for element in package.Elements:
        if element.Type == "Requirement" and element.TaggedValues.Count > 0:
            tag_info = [f"{tagged_value.Name}: {tagged_value.Value}" for tagged_value in element.TaggedValues]
            if tag_info:  # Only show checklist if there are tag values
                selected_tags = show_checklist(tag_info, element.Name, package.Name)
                if selected_tags is None:  # If the user canceled the operation
                    messagebox.showinfo("Cancelled", "Operation has been canceled.")
                    exit()  # Exit the script
                delete_tag_values(repository, element, selected_tags)
    
    for sub_package in package.Packages:
        process_package(repository, sub_package)

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

    # End of process message
    messagebox.showinfo("Completed", "Tag values deletion process completed.")

if __name__ == "__main__":
    main()
