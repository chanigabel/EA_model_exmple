import win32com.client
ea = win32com.client.Dispatch("EA.App")
repository = ea.Repository
global package_GUID

def add_master_document_with_details(package_GUID, document_name, document_version, document_alias, diagram_name):
    
    owner_package = repository.GetPackageByGuid(package_GUID)
    master_document_package = owner_package.Packages.AddNew(document_name, "Package")
    master_document_package.Update()
    master_document_package.Element.Stereotype = "master document"
    master_document_package.Alias = document_alias
    master_document_package.Version = document_version
    master_document_package.Update()
    
    # Add a new tagged value for the diagram name
    diagram_name_tag = master_document_package.Element.TaggedValues.AddNew("DiagramName", "")
    diagram_name_tag.Value = diagram_name
    diagram_name_tag.Update()
    
    # Link to the master template
    for template_tag in master_document_package.Element.TaggedValues:
        if template_tag.Name == "RTFTemplate":
            template_tag.Value = "(model document: master template)"
            template_tag.Notes = "Default: (model document: master template)"
            template_tag.Update()
            break
    
    return master_document_package

def add_model_document_for_package(master_document, package, name, treepos, template):
    
    # Add a new element (model document) to the master document
    model_doc_element = master_document.Elements.AddNew(name, "Class")
    
    # Set the position of the model document in the tree
    model_doc_element.TreePos = treepos
    
    # Set the stereotype of the model document
    model_doc_element.StereotypeEx = "model document"
    model_doc_element.Update()
    
    # Add tagged values to the model document
    for template_tag in model_doc_element.TaggedValues:
        if template_tag.Name == "RTFTemplate":
            template_tag.Value = template
            template_tag.Notes = "Default: Model Report"
            template_tag.Update()
            break
    
    # Add an attribute to represent the package
    attribute = model_doc_element.Attributes.AddNew(package.Name, "Package")
    attribute.ClassifierID = package.Element.ElementID
    attribute.Update()
    
    return model_doc_element

def add_model_document_for_diagram(master_document, diagram, name, treepos, template):
    
    # Add a new element (model document) to the master document
    model_doc_element = master_document.Elements.AddNew(name, "Class")
    
    # Set the position of the model document in the tree
    model_doc_element.TreePos = treepos
    
    # Set the stereotype of the model document
    model_doc_element.StereotypeEx = "model document"
    model_doc_element.Update()
    
    # Add tagged values to the model document
    for template_tag in model_doc_element.TaggedValues:
        if template_tag.Name == "RTFTemplate":
            template_tag.Value = template
            template_tag.Notes = "Default: Model Report"
            template_tag.Update()
            break
    
    # Add an attribute to represent the diagram
    attribute = model_doc_element.Attributes.AddNew(diagram.Name, "Diagram")
    attribute.ClassifierID = diagram.DiagramID
    attribute.Update()
    
    return model_doc_element

def make_use_case_master_document(current_diagram):
    # We should ask the user for a version
    document_version = input("Please enter the version of this document (e.g., x.y.z): ")
    document_alias = input("Please enter the alias of this document: ")
    if document_version:
        # OK, we have a version, continue
        diagram_name = current_diagram.Name
        document_name = f"UCD - {diagram_name} v. {document_version}"
        master_document = add_master_document_with_details(package_GUID, document_name, document_version, document_alias, diagram_name)
        return master_document
    return None

def get_activity_for_use_case(use_case):
    return get_nested_diagram_owner_for_element(use_case, "Activity")

def get_interaction_for_use_case(use_case):
    return get_nested_diagram_owner_for_element(use_case, "Interaction")

def get_nested_diagram_owner_for_element(element, element_type):
    diagram_owner = None
    for nested_element in element.Elements:
        if nested_element.Type == element_type and nested_element.Diagrams.Count > 0:
            diagram_owner = nested_element
            break
    return diagram_owner

def sort_elements_by_name(elements):
    go_again = False
    while True:
        for i in range(len(elements) - 1):
            this_element = elements[i]
            next_element = elements[i + 1]
            if element_is_after(this_element, next_element):
                elements[i], elements[i + 1] = elements[i + 1], elements[i]
                go_again = True
        if not go_again:
            break
        go_again = False
    return elements

def element_is_after(this_element, next_element):
    return this_element.Name.lower() > next_element.Name.lower()

def get_diagram_objects(diagram, object_type):
    # Get all diagram objects in the diagram
    diagram_objects = diagram.DiagramObjects
    
    # Filter diagram objects based on object type
    filtered_objects = []
    for diagram_object in diagram_objects:
        elementID = diagram_object.ElementID
        element=repository.GetElementByID(elementID)
        if element is not None and element.Type == object_type:
            filtered_objects.append(diagram_object)
    
    return filtered_objects

def get_elements_from_diagram_in_boundary(diagram, element_type, boundary):
    # Get all elements in the diagram
    diagram_elements = diagram.DiagramObjects
    
    # Filter elements based on element type and containment within the boundary
    filtered_elements = []
    for diagram_element in diagram_elements:
        element = diagram_element.Element
        if element is not None and element.Type == element_type:
            # Check if the element is contained within the boundary
            if diagram_element.IsWithinBoundary(boundary):
                filtered_elements.append(element)
    
    return filtered_elements

def get_elements_from_diagram(diagram, element_type):
    # Get all diagram objects in the diagram
    diagram_objects = diagram.DiagramObjects
    
    # Filter diagram objects based on element type
    filtered_elements = []
    for diagram_object in diagram_objects:
        elementID = diagram_object.ElementID
        element=repository.GetElementByID(elementID)
        if element is not None and element.Type == element_type:
            filtered_elements.append(element)
    
    return filtered_elements

def add_use_cases(master_document, usecases, starting_index):
    for usecase in usecases:
        # Create a new element (use case) under the master document
        new_element = master_document.Elements.AddNew(usecase.Name, "UseCase")
        
        # Set the position of the use case in the tree
        new_element.TreePos = str(starting_index)
        starting_index += 1
        
        # Update the use case element
        new_element.Update()
    
    return starting_index

def create_use_case_document(diagram, documents_package_GUID):
    
    # First, create a master document
    master_document = make_use_case_master_document(diagram)
    if master_document is not None:
        i = 0
        # Use case diagram part 1
        add_model_document_for_diagram(master_document, diagram,diagram.Name, i, "UCD_Use Case Diagram")
        i += 1
        
        # Add Actors
        diagram_package = repository.GetPackageByID(diagram.PackageID)
        add_model_document_for_package(master_document, diagram_package, diagram.Name + " Actors", i, "UCD_Actors")
        i += 1
        
        # Check if there are boundaries in the diagram
        boundaries = get_diagram_objects(diagram, "Boundary")
        
        # Get the use cases
        if len(boundaries)>0:
            usecases = get_elements_from_diagram_in_boundary(diagram, "UseCase", boundaries[0])
            print("boundary found")
        else:
            usecases = get_elements_from_diagram(diagram, "UseCase")
        
        # Sort use cases alphabetically
        usecases = sort_elements_by_name(usecases)
        
        # Add the use cases
        i = add_use_cases(master_document, usecases, i)
        
        repository.RefreshModelView(master_document.PackageID)
        # Select the created master document in the project browser
        repository.ShowInProjectView(master_document)

def on_diagram_script():
    global package_GUID
    documents_package = repository.GetTreeSelectedPackage()
    if documents_package is not None:
        package_GUID = documents_package.PackageGUID
        current_diagram = repository.GetCurrentDiagram()
        # current_diagram = repository.GetDiagramByID(10)
        print(current_diagram.name)
        if current_diagram is not None:
            create_use_case_document(current_diagram, package_GUID)
            print("Select the Master Document and press F8 to generate document")
        else:
            print("This script requires a diagram to be visible")

on_diagram_script()
