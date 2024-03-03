import win32com.client

def create_sample_fragments(package):
    # Add example fragments of different types to the package
    add_fragment(package, "Text Fragment", "This is a text fragment.","Text")
    add_fragment(package, "Table Fragment", "<Table Content>","Table")
    add_fragment(package, "Image Fragment", "<Image Path>","Image")

def add_fragment(package, name, content,type):
    fragment = package.Elements.AddNew(name, type)
    fragment.Notes = content
    fragment.Update()

def create_diagram_in_package(package, diagram_name):
    # Create a new diagram within the package
    diagram = package.Diagrams.AddNew(diagram_name, "Diagram")
    diagram.Update()
    
    return diagram

def add_element_to_diagram(diagram, element):
    # Add an element to the diagram
    diagram_object = diagram.DiagramObjects.AddNew(element.Name, element.Type)
    diagram_object.ElementID = element.ElementID
    diagram_object.Update()


def add_fragment_to_diagram(diagram, fragment_name, fragment_type, position):
    # Add a fragment to the diagram at the specified position
    diagram_object = diagram.DiagramObjects.AddNew(fragment_name, fragment_type)
    diagram_object.Update()
    diagram_object.left = position[0]
    diagram_object.right = position[0] + 100  # Adjust the width as needed
    diagram_object.top = position[1]
    diagram_object.bottom = position[1] + 50  # Adjust the height as needed
    diagram_object.Update()
    
def main():
    # Connect to Enterprise Architect
    ea = win32com.client.Dispatch("EA.App")
    repository = ea.Repository
    
    # Get the selected package
    selected_package = repository.GetTreeSelectedPackage()
    print(type(selected_package))
    if selected_package is not None:
        # Create a new diagram within the selected package
        diagram = create_diagram_in_package(selected_package, "Fragments Diagram")
        
        # Create sample fragments within the selected package
        create_sample_fragments(selected_package)
        selected_package.Update()

        # Add all elements (fragments) within the package to the diagram
        print(selected_package.Elements)
        for element in selected_package.Elements:
            if "Fragment" in element.Name:
                 print(element.Name)
                 add_element_to_diagram(diagram, element)

        # Refresh the package view
        selected_package.Update()
        diagram.Update()
        
        # Save changes
        repository.SaveAllDiagrams()


if __name__ == "__main__":
    main()
