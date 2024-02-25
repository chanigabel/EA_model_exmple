import win32com.client
ea = win32com.client.Dispatch("EA.App")

def add_master_document(package_guid, document_name, document_version, document_alias):
    owner_package = ea.Repository.GetPackageByGuid(package_guid)
    master_document_package = owner_package.Packages.create(documentName=document_name, package="package")
    master_document_package.update()
    master_document_package.Element.Stereotype = "master document"
    master_document_package.Alias = document_alias
    master_document_package.Version = document_version
    master_document_package.update()
    
    # link to the master template
    for template_tag in master_document_package.Element.TaggedValues:
        if template_tag.Name == "RTFTemplate":
            template_tag.Value = "(model document: master template)"
            template_tag.Notes = "Default: (model document: master template)"
            template_tag.update()
            break
    
    return master_document_package

def add_model_document_for_package(master_document, package, name, tree_pos, template):
    model_doc_element = master_document.Elements.create(name=name, metaClass="Class")
    # set the position
    model_doc_element.TreePos = tree_pos
    model_doc_element.StereotypeEx = "model document"
    model_doc_element.update()
    
    # add tagged values
    for template_tag in model_doc_element.TaggedValues:
        if template_tag.Name == "RTFTemplate":
            template_tag.Value = template
            template_tag.Notes = "Default: Model Report"
            template_tag.update()
            break
    
    # add attribute
    attribute = model_doc_element.Attributes.create(name=package.Name, metaClass="Package")
    attribute.ClassifierID = package.ElementID
    attribute.update()

def add_model_document_with_search(master_document, template, element_name, element_guid, tree_pos, search_name):
    model_doc_element = master_document.Elements.create(name=element_name, metaClass="Class")
    # set the position
    model_doc_element.TreePos = tree_pos
    model_doc_element.StereotypeEx = "model document"
    model_doc_element.update()
    
    if len(element_guid) > 0:
        for template_tag in model_doc_element.TaggedValues:
            if template_tag.Name == "RTFTemplate":
                template_tag.Value = template
                template_tag.Notes = "Default: Model Report"
                template_tag.update()
            elif template_tag.Name == "SearchName":
                template_tag.Value = search_name
                template_tag.update()
            elif template_tag.Name == "SearchValue":
                template_tag.Value = element_guid
                template_tag.update()
    else:
        # add tagged values
        for template_tag in model_doc_element.TaggedValues:
            if template_tag.Name == "RTFTemplate":
                template_tag.Value = template
                template_tag.Notes = "Default: Model Report"
                template_tag.update()
                break
        # no GUID provided. Set master document package ID as dummy attribute to make the template work
        attribute = model_doc_element.Attributes.create(name=master_document.Name, metaClass="Package")
        attribute.ClassifierID = master_document.Element.ElementID
        attribute.update()

def make_use_case_master_document(current_diagram):
    # we should ask the user for a version
    document_title = ""
    document_version = ""
    document_name = ""
    diagram_name = current_diagram.Name
    make_use_case_master_document = None

    # to make sure document version is filled in
    document_version = input("Please enter the version of this document: ")

    if document_version != "":
        # OK, we have a version, continue
        document_name = "UCD - " + diagram_name + " v. " + document_version
        master_document = add_master_document_with_details(use_case_documents_package_guid, document_name, document_version, diagram_name)
        make_use_case_master_document = master_document

    return make_use_case_master_document

def select_package():
    # Implement package selection logic here
    return ea.Repository.GetTreeSelectedPackage()

def create_use_case_document(diagram, documents_package_guid):
    use_case_documents_package_guid = documents_package_guid
    # first create a master document
    master_document = make_use_case_master_document(diagram)
    if master_document is not None:
        i = 0
        # use case diagram part 1
        add_model_document_for_diagram(use_case_documents_package_guidmaster_document, diagram, i, "UCD_Use Case Diagram")
        i += 1
        # add Actors
        diagram_package = ea.Repository.GetPackageByID(diagram.PackageID)
        add_model_document_for_package(master_document, diagram_package, diagram.Name + " Actors", i, "UCD_Actors")
        i += 1
        # We only want to report the use cases that are shown within the scope boundary on this diagram
        # get the boundary diagram object in the diagram
        boundaries = get_diagram_objects(diagram, "Boundary")
        print(boundaries.Count)
        # get the use cases
        if boundaries.Count > 0:
            use_cases = get_elements_from_diagram_in_boundary(diagram, "UseCase", boundaries[0])
            print("boundary found")
        else:
            use_cases = get_elements_from_diagram(diagram, "UseCase")

        # sort use cases alphabetically
        use_cases = sort_elements_by_name(use_cases)

        # add the use cases
        i = add_use_cases(master_document, use_cases, i)

        ea.Repository.RefreshModelView(master_document.PackageID)
        # select the created master document in the project browser
        ea.Repository.ShowInProjectView(master_document)

def on_diagram_script():
 # Select the package to generate the virtual document in
    documents_package = select_package()
    print(documents_package.Name)
    print(documents_package.packageGuid)
    if documents_package is not None:
        # Get a reference to the current diagram
        current_diagram = ea.Repository.GetCurrentDiagram()
        
        if current_diagram is not None:
            create_use_case_document(current_diagram, documents_package.PackageGUID)
            win32com.client.Dispatch("WScript.Shell").Popup("Select the Master Document and press F8 to generate document", 0, "Finished!", 0x40)
        else:
            win32com.client.Dispatch("WScript.Shell").Popup("This script requires a diagram to be visible", 0, "Error", 0x10)
    else:
        win32com.client.Dispatch("WScript.Shell").Popup("Please select the package to generate the virtual document in", 0, "Document Package", 0x20)

if __name__ == "__main__":
    on_diagram_script()
