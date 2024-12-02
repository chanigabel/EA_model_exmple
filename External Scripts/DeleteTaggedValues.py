import win32com.client
from tkinter import messagebox

def print_attribute_tagged_values(repository, package):
    """Recursively print all tagged values of attributes in elements within the package."""
    for element in package.Elements:
        for oprations in element.oprations:
            if oprations.TaggedValues.Count > 0:
                print(f"Element: {element.Name}, Attribute: {oprations.Name}")
                for tagged_value in oprations.TaggedValues:
                    print(f"  Tagged Value: {tagged_value.Name} = {tagged_value.Value}")
                    print(tagged_value.TagGUID)

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

    print(f"Printing tagged values of attributes in elements under package '{selected_package.Name}':\n")
    print_attribute_tagged_values(repository, selected_package)
    print("\nCompleted printing tagged values.")

if __name__ == "__main__":
    main()
