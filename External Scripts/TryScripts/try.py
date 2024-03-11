import win32com.client

ea = win32com.client.Dispatch("EA.App")
repository = ea.Repository

def add_element_to_diagram( diagram, element):
    # Get the element's ID
    element_id = element.ElementID
    # Create a new diagram object for the given element
    diagram_object = diagram.DiagramObjects.AddNew("", "")
    # Set the element ID for the diagram object
    diagram_object.ElementID = element_id
    # Update the diagram object
    diagram_object.Update()
    # Refresh the diagram view in Enterprise Architect
    repository.ReloadDiagram(diagram.DiagramID)

# documents_package = repository.GetTreeSelectedPackage()
# if documents_package is not None:
#     package_GUID = documents_package.PackageGUID
#     current_diagram = repository.GetCurrentDiagram()
#     print(repository.GetPackageByGuid(package_GUID).name)
#     print(repository.GetCurrentDiagram().name)
d=repository.GetDiagramByID(21)
e=repository.GetElementByID(121)
e1=repository.GetElementByID(119)
e2=repository.GetElementByID(116)
e3=repository.GetElementByID(120)
e4=repository.GetElementByID(145)
add_element_to_diagram(d,e)
add_element_to_diagram(d,e1)
add_element_to_diagram(d,e2)
add_element_to_diagram(d,e3)
add_element_to_diagram(d,e4)
    # if current_diagram is not None:
    #     print("Select the Master Document and press F8 to generate document")
    # else:
    #     print("This script requires a diagram to be visible")
