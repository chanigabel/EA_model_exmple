#The script, written by Chany Jacobs, 
#is designed to create a master document containing document models. 
#This allows users to generate specific documentation about a package by dragging it into one of the models.

import win32com.client
# num - order of functions

#7
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

#6
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

#5
def make_master_document(repository, package_GUID):
    document_version = input(
        "Please enter the version of this document (e.g., x.y.z): "
    )
    document_alias = input("Please enter the alias of this document: ")
    document_diagram_name = input("Please enter the name of this document: ")

    if document_version:
        document_name = f"D - {document_diagram_name} v. {document_version}"
        master_document = add_master_document_with_details(
            repository,
            package_GUID,
            document_name,
            document_version,
            document_alias,
            document_diagram_name,
        )
        return master_document

    return None

#4
def create_diagram(repository, package_guid, diagram_name, diagram_type):
    package = repository.GetPackageByGuid(package_guid)
    if package:
        new_diagram = package.Diagrams.AddNew(diagram_name, diagram_type)
        if new_diagram:
            new_diagram.Update()
            return new_diagram
    return None   

#3
def create_document(repository, documents_package_GUID):
    master_document = make_master_document(
        repository, documents_package_GUID
    ) 
    
    documentation_diagram = create_diagram(
            repository,
            master_document.PackageGUID,
            "Documentation Diagram",
            "Documentation"
        )
    
    if master_document is not None:
        if documentation_diagram is not None:
            i = 0
            add_model_document_for_diagram(
                repository,
                master_document,
                documentation_diagram,
                "Connectors Documentation",
                i,
                "Connector_tm",
            )
            i += 1
            add_model_document_for_diagram(
                repository,
                master_document,
                documentation_diagram,
               "Operations Documentation",
                i,
                "Operation_tm",
            )
            i += 1
            
            repository.RefreshModelView(master_document.PackageID)
            repository.ShowInProjectView(master_document)

#2
def main():
    ea = win32com.client.Dispatch("EA.App")
    repository = ea.Repository
    documents_package = repository.GetTreeSelectedPackage()
    if documents_package is not None:
        package_GUID = documents_package.PackageGUID
        create_document(repository, package_GUID)
        print("Select the Master Document and press F8 to generate document")
    else:
        print("This script requires a package to be select")

#1
main()
