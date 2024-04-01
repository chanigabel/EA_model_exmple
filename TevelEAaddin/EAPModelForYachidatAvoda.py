#The script, written by Chany Jacobs, 
#This script create new EA project model from the selected diagram packages with all it's hierarchy, 
#apart from the selected diagram.

import win32com.client
import os

def create_eap_hierarchy(sel_package, rep, list_package_guids, list_package_names):
    if sel_package.ParentID == 0:
        return

    parent_package = rep.GetPackageByID(sel_package.ParentID)
    list_package_guids.append(parent_package.PackageGUID)
    list_package_names.append(parent_package.Name)

    create_eap_hierarchy(parent_package, rep, list_package_guids, list_package_names)

def if_package_exist(rep, package_name, list_package_guids):
    for cur_guid in list_package_guids:
        cur_package = rep.GetPackageByGuid(cur_guid)
        if cur_package.Name == package_name:
            return True, cur_package  # Return True and the found package
    return False, None  # Return False and None if package not found

def create_diagram_eap():
    try:
        # Connect to Enterprise Architect
        ea = win32com.client.Dispatch("EA.App")
        rep = ea.Repository

        # Get selected diagram
        cur_diagram = rep.GetCurrentDiagram()

        if cur_diagram is not None:
            sel_package = rep.GetTreeSelectedPackage()

            # Check if any package is selected
            if sel_package is None:
                print("Please select a package.")
                return

            flag_if_package_exist = False
            list_package_guids = []
            list_package_names = []
            list_xmi_package = []

            # Loop through diagram objects
            for cur_object in cur_diagram.DiagramObjects:
                sel_element = rep.GetElementByID(cur_object.ElementID)
                if sel_element.Type == "Package":
                    flag_if_package_exist = True

                    xmi_name = sel_package.Name + "_" + sel_element.Name
                    file_name = "C:\\Temp\\" + xmi_name + ".xmi"

                    first_package_id = sel_element.PackageID
                    sel_package = rep.GetPackageByID(first_package_id)
                    list_package_guids.append(sel_package.PackageGUID)
                    list_package_names.append(sel_package.Name)

                    # Create the list of its parent packages GUIDs
                    create_eap_hierarchy(sel_package, rep, list_package_guids, list_package_names)

                    # Create current XMI package
                    if not os.path.exists(file_name):  # Check if file exists
                        # Obtain the Project object
                        my_project = rep.GetProjectInterface()
                        # Call ExportPackageXMI from the Project object
                        my_project.ExportPackageXMI(sel_element.ElementGUID, 2, 1, -1, 0, 0, file_name)

                    # Store information for further processing
                    list_xmi_package.append((file_name, list(list_package_guids), list(list_package_names)))

            list_package_guids.clear()
            list_package_names.clear()
            print(flag_if_package_exist)
            if flag_if_package_exist:
                rep.CreateModel(0, "C:/Temp/" + cur_diagram.Name + ".eap", 1)
                print("EAP model created successfully.")
                    # Further process the EAP model
                create_eap_model("C:/Temp/" + cur_diagram.Name + ".eap", list_xmi_package, rep,my_project)
            else:
                print("No packages are found in the selected diagram.")

        else:
            print("Please select a diagram.")

    except Exception as e:
        print("An error occurred:", e)

def create_eap_model(project_path, list_xmi_package, rep,my_project):
    try:
        rep.OpenFile(project_path)

        # Delete existing models
        models = rep.Models
        models.DeleteAt(0, True)

        # Create root package
        root_package_name = list_xmi_package[0][2][-1]  # Last item in the list of package names
        root = models.AddNew(root_package_name, "")
        root.Update()

        cur_package = root
        list_package_guids = [cur_package.PackageGUID]

        # Iterate over XMI packages and import them
        for xmi_package in list_xmi_package:
            for package_name in reversed(xmi_package[2]):  # Reverse to start from the topmost package
                if package_name == root_package_name:
                    continue

                is_exist, tmp_package = if_package_exist(rep, package_name, list_package_guids)

                if not is_exist:
                    cur_package = cur_package.Packages.AddNew(package_name, "")
                    cur_package.Update()
                    cur_package.Packages.Refresh()
                    list_package_guids.append(cur_package.PackageGUID)
                else:
                    cur_package = tmp_package

            # Import XMI file to current package
            my_project.ImportPackageXMI(cur_package.PackageGUID, xmi_package[0], 1, 1)

        rep.RefreshModelView(0)
        models.Refresh()

        print("EAP model created and XMI files imported successfully.")

    except Exception as e:
        print("An error occurred:", e)

# Usage example
def main():
    create_diagram_eap()

if __name__ == "__main__":
    main()
