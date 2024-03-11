import win32com.client
# num - order of functions

# 6 
def add_model_document_for_diagram(repository,master_document, diagram, name, treepos, template):
    # Get the diagram ID
    diagram_id = diagram.DiagramID
    # Create a new document object
    document = master_document.Elements.AddNew(name, "Model Document")
    # Set properties of the document
    document.TreePos = treepos
    for tag in document.TaggedValues:
        if tag.Name == "RTFTemplate":
            tag.Value = template
            tag.Notes =template
            tag.Update()
            break
    # Add the document to the diagram
    diagramObject = diagram.DiagramObjects.AddNew(name, "")
    diagramObject.ElementID = document.ElementID
    diagramObject.Update()
    # Refresh the diagram view
    repository.ReloadDiagram(diagram_id)

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
            template_tag.Value = "Connector"
            template_tag.Notes = "Connector"
            template_tag.Update()
            break

        
    return master_document_package

# 4 
def make_master_document(repository, current_diagram, package_GUID):
    document_version = input(
        "Please enter the version of this document (e.g., x.y.z): "
    )
    document_alias = input("Please enter the alias of this document: ")

    if document_version:
        diagram_name = current_diagram.Name
        document_name = f"D - {diagram_name} v. {document_version}"
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

#3 
def create_document(repository, diagram, documents_package_GUID):
    master_document = make_master_document(
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
            "Connector",
        )
        i += 1
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
            create_document(repository, current_diagram, package_GUID)
            print("Select the Master Document and press F8 to generate document")
        else:
            print("This script requires a diagram to be visible")

#1 
on_diagram_script()
