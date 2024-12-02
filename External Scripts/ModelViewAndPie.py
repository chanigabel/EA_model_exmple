import win32com.client
import tkinter as tk
from tkinter import messagebox
import re

def get_package_by_name(package, package_name):
    """Recursively search for a package by name within a given package and its sub-packages."""
    if package.Name == package_name:
        return package

    for sub_package in package.Packages:
        found_package = get_package_by_name(sub_package, package_name)
        if found_package:
            return found_package

    return None

def find_package_in_repository(repository, package_name):
    """Start the search for the package by name in all top-level models in the repository."""
    for model in repository.Models:
        found_package = get_package_by_name(model, package_name)
        if found_package:
            return found_package
    return None

def get_elements_from_package(package):
    """Retrieve all elements within a package."""
    elements = []
    for element in package.Elements:
        elements.append(element)
    return elements

def prompt_user_to_select_elements(elements):
    """Display a checklist for the user to select one or more elements."""
    root = tk.Tk()
    root.title("Select Elements from ModelView-Chart")
    selected_elements = []

    # Frame to hold the checklist of elements
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    # Function to handle checkbox selection
    def on_select():
        selected_elements.clear()
        for var, element in zip(variables, elements):
            if var.get():
                selected_elements.append(element)
        root.quit()  # Close the window

    # Create a checkbox for each element
    variables = []
    for element in elements:
        var = tk.BooleanVar()
        chk = tk.Checkbutton(frame, text=element.Name, variable=var)
        chk.pack(anchor="w")
        variables.append(var)

    # Confirm button to finalize the selection
    confirm_button = tk.Button(root, text="Confirm Selection", command=on_select)
    confirm_button.pack(pady=(0, 10))

    root.mainloop()
    root.destroy()

    return selected_elements

def fetch_and_update_tagged_values(element, package_id):
    """Fetch and update specific tagged values for the selected element."""
    try:
        tagged_values = element.TaggedValues
        for tag in tagged_values:
            if tag.Notes:
                # Regular expression to match either "Package_ID = #Package#" or "Package_ID = (some number)"
                pattern = r"Package_ID = (#Package#|\(\d+\))"
                
                # Replace with the new package ID
                if re.search(pattern, tag.Notes):
                    tag.Notes = re.sub(pattern, f"Package_ID = ({package_id})", tag.Notes)
                    tag.Update()
    except Exception as e:
        print(f"Error fetching or updating tagged values: {e}")

def main():
    try:
        ea = win32com.client.Dispatch("EA.App")
        repository = ea.Repository
        print("EA is accessible.")
    except Exception as e:
        print("Error: Could not connect to EA:", str(e))
        return

    try:
        # Find the "ModelView-Chart" package
        package = find_package_in_repository(repository, "ModelView-Chart")
        if not package:
            print("Package 'ModelView-Chart' not found.")
            return

        # Get elements from the package
        elements = get_elements_from_package(package)
        if not elements:
            print("No elements found in 'ModelView-Chart'.")
            return

        # Prompt user to select elements
        selected_elements = prompt_user_to_select_elements(elements)
        if not selected_elements:
            print("No elements selected.")
            return

        # Get the selected package from the EA Project Browser
        selected_package = repository.GetTreeSelectedObject()
        if selected_package is None or selected_package.ObjectType != 5:
            print("No package is selected in the EA Project Browser.")
            return

        package_id = selected_package.PackageID

        # Update tagged values for each selected element
        for element in selected_elements:
            fetch_and_update_tagged_values(element, package_id)
            print(f"Updated tagged values for '{element.Name}' with Package_ID {package_id}.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
