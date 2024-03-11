import win32com.client

def create_master_document(package):
    # Create a new master document package
    master_document_package = package.Packages.AddNew("Master Document", "Package")
    master_document_package.Update()
    
    # Add a stereotype to indicate that it's a master document
    master_document_package.Element.Stereotype = "Master Document"
    
    # Update the package
    master_document_package.Update()
    print(master_document_package.packageID)
    return master_document_package.packageID

def create_sample_fragments(package):
    # Add example fragments of different types to the package
    add_fragment(package, "Text Fragment", "This is a text fragment.","Text")
    print(len(package.Elements))
    add_fragment(package, "Table Fragment", "<Table Content>","Table")
    print(len(package.Elements))
    add_fragment(package, "Image Fragment", "<Image Path>","Image")    
    print(len(package.Elements))


    
def add_fragment(package, name, content,type):
    fragment = package.Elements.AddNew(name, type)
    print(len(package.Elements),"kkkkkk")
    fragment.Notes = content
    fragment.Update()


def create_diagram_in_package(package, diagram_name):
    # Create a new diagram within the package
    diagram = package.Diagrams.AddNew(diagram_name, "Diagram")
    diagram.Update()
    
    return diagram

def add_fragment_to_diagram(diagram, fragment_name, fragment_type,fragment_ID):
    # Add a fragment to the diagram at the specified position
    diagram_object = diagram.DiagramObjects.AddNew(fragment_name, fragment_type)
    diagram_object.ElementID = fragment_ID
    diagram_object.Update()
    # diagram_object.left = position[0]
    # diagram_object.right = position[0] + 100  # Adjust the width as needed
    # diagram_object.top = position[1]
    # diagram_object.bottom = position[1] + 50  # Adjust the height as needed
    # diagram_object.Update()


def main():
    # Connect to Enterprise Architect
    ea = win32com.client.Dispatch("EA.App")
    repository = ea.Repository
    
    # Get the selected package
    selected_package = repository.GetTreeSelectedPackage()
    
    if selected_package is not None:
        # Create a new master document package
        master_document_package_ID = create_master_document(selected_package)
        master_document_package=repository.GetPackageByID(master_document_package_ID)
        # Create a new diagram within the master document package
        diagram = create_diagram_in_package(master_document_package, "Fragments Diagram")
        print(len(master_document_package.Elements),"ppp")
        # Create sample fragments within the master document package
        create_sample_fragments(master_document_package)
        selected_package.Update()

        # Add all fragments within the master document package to the diagram
        fragment_positions = [(100, 100), (200, 200), (300, 300)]  # Example positions
        print(len(master_document_package.Elements),"ddddddddddd")
        for fragment in master_document_package.Elements:
            print(type(fragment))
            if "Fragment" in fragment.Name:
                add_fragment_to_diagram(diagram, fragment.Name, fragment.Type,fragment.elementID)
    
        
        # Refresh the package view
        selected_package.Update()
        
        # Save changes
        repository.SaveAllDiagrams()
        

if __name__ == "__main__":
    main()
