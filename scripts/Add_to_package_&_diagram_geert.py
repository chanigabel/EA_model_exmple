import win32com.client
# num - order of functions

# 5
def add_master_document_with_details(
    repository,
    package_GUID,
    document_name,
    document_version,
    document_alias,
    diagram_name,
):
    owner_package = repository.GetPackageByGuid(package_GUID)
    master_document_package = owner_package.Packages.AddNew(document_name, "Package")
    master_document_package.Update()
    master_document_package.Element.Stereotype = "master document"
    master_document_package.Alias = document_alias
    master_document_package.Version = document_version
    master_document_package.Update()

    # Add a new tagged value for the diagram name
    diagram_name_tag = master_document_package.Element.TaggedValues.AddNew(
        "DiagramName", ""
    )
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

# 7
def add_model_document_for_package(
   master_document, package, name, treepos, template
):
    model_doc_element = master_document.Elements.AddNew(name, "Class")
    model_doc_element.TreePos = treepos
    model_doc_element.StereotypeEx = "model document"
    model_doc_element.Update()

    for template_tag in model_doc_element.TaggedValues:
        if template_tag.Name == "RTFTemplate":
            template_tag.Value = template
            template_tag.Notes = "Default: Model Report"
            template_tag.Update()
            break

    attribute = model_doc_element.Attributes.AddNew(package.Name, "Package")
    attribute.ClassifierID = package.Element.ElementID
    attribute.Update()

    return model_doc_element

# 6
def add_model_document_for_diagram(repository,master_document, diagram, name, treepos, template):
    # Get the diagram ID
    diagram_id = diagram.DiagramID
    # Create a new document object
    document = master_document.Elements.AddNew(name, "Document")
    # Set properties of the document
    # document.TreeNode = treepos//what the problem
    document.StyleEx = template
    # Add the document to the diagram
    diagramObject = diagram.DiagramObjects.AddNew(name, "")
    diagramObject.ElementID = document.ElementID
    diagramObject.Update()
    # Refresh the diagram view
    repository.ReloadDiagram(diagram_id)

#4
def make_use_case_master_document(repository, current_diagram, package_GUID):
    document_version = input(
        "Please enter the version of this document (e.g., x.y.z): "
    )
    document_alias = input("Please enter the alias of this document: ")

    if document_version:
        diagram_name = current_diagram.Name
        document_name = f"UCD - {diagram_name} v. {document_version}"
        master_document = add_master_document_with_details(
            repository,
            package_GUID,
            document_name,
            document_version,
            document_alias,
            diagram_name,
        )
        return master_document

    return None

# 11
def sort_elements_by_name(elements):
    go_again = True

    while go_again:
        go_again = False

        for i in range(len(elements) - 1):
            this_element = elements[i]
            next_element = elements[i + 1]

            if this_element.Name.lower() > next_element.Name.lower():
                elements[i], elements[i + 1] = elements[i + 1], elements[i]
                go_again = True

    return elements

# 8
def get_diagram_objects(repository, diagram, object_type):
    diagram_objects = diagram.DiagramObjects
    filtered_objects = []

    for diagram_object in diagram_objects:
        elementID = diagram_object.ElementID
        element = repository.GetElementByID(elementID)

        if element is not None and element.Type == object_type:
            filtered_objects.append(diagram_object)

    return filtered_objects

# 9
def get_elements_from_diagram_in_boundary(repository, diagram, element_type, boundary):
    diagram_elements = diagram.DiagramObjects
    filtered_elements = []

    for diagram_element in diagram_elements:
        element = diagram_element.Element

        if (
            element is not None
            and element.Type == element_type
            and diagram_element.IsWithinBoundary(boundary)
        ):
            filtered_elements.append(element)

    return filtered_elements

# 10
def get_elements_from_diagram(repository, diagram, element_type):
    diagram_objects = diagram.DiagramObjects
    filtered_elements = []

    for diagram_object in diagram_objects:
        elementID = diagram_object.ElementID
        element = repository.GetElementByID(elementID)

        if element is not None and element.Type == element_type:
            filtered_elements.append(element)

    return filtered_elements

# 12
def add_use_cases(master_document, usecases, starting_index):
    for usecase in usecases:
        new_element = master_document.Elements.AddNew(usecase.Name, "UseCase")
        new_element.TreePos = str(starting_index)
        starting_index += 1
        new_element.Update()

    return starting_index

#3
def create_use_case_document(repository, diagram, documents_package_GUID):
    master_document = make_use_case_master_document(
        repository, diagram, documents_package_GUID
    )

    if master_document is not None:
        i = 0
        add_model_document_for_diagram(
            repository,
            master_document,
            diagram,
            diagram.Name,
            i,
            "Use Case Details",
        )
        i += 1

        diagram_package = repository.GetPackageByID(diagram.PackageID)
        add_model_document_for_package(
            master_document,
            diagram_package,
            diagram.Name + " Actors",
            i,
            "UCD_Actors",
        )
        i += 1

        boundaries = get_diagram_objects(repository, diagram, "Boundary")
        usecases = []

        if len(boundaries) > 0:
            usecases = get_elements_from_diagram_in_boundary(
                repository, diagram, "UseCase", boundaries[0]
            )
            print("boundary found")
        else:
            usecases = get_elements_from_diagram(repository, diagram, "UseCase")

        usecases = sort_elements_by_name(usecases)
        i = add_use_cases(master_document, usecases, i)

        repository.RefreshModelView(master_document.PackageID)
        repository.ShowInProjectView(master_document)

#2
def on_diagram_script():
    ea = win32com.client.Dispatch("EA.App")
    repository = ea.Repository

    documents_package = repository.GetTreeSelectedPackage()
    if documents_package is not None:
        package_GUID = documents_package.PackageGUID
        current_diagram = repository.GetCurrentDiagram()
        if current_diagram is not None:
            create_use_case_document(repository, current_diagram, package_GUID)
            print("Select the Master Document and press F8 to generate document")
        else:
            print("This script requires a diagram to be visible")

#1
on_diagram_script()
