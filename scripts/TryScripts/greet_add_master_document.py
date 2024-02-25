import win32com.client
ea = win32com.client.Dispatch("EA.App")
repository = ea.Repository
def add_master_document(package_GUID, document_name, document_version, document_alias):
   
    
    owner_package = repository.GetPackageByGuid(package_GUID)
    master_document_package = owner_package.Packages.AddNew(document_name, "Package")
    master_document_package.Update()
    master_document_package.Element.Stereotype = "master document"
    master_document_package.Alias = document_alias
    master_document_package.Version = document_version
    master_document_package.Update()
    
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

def add_model_document_with_search(master_document, template, element_name, element_GUID, treepos, search_name):
    ea = win32com.client.Dispatch("EA.App")
    repository = ea.Repository
    
    # Add a new element (model document) to the master document
    model_doc_element = master_document.Elements.AddNew(element_name, "Class")
    
    # Set the position of the model document in the tree
    model_doc_element.TreePos = treepos
    
    # Set the stereotype of the model document
    model_doc_element.StereotypeEx = "model document"
    model_doc_element.Update()
    
    # Add tagged values to the model document
    if len(element_GUID) > 0:
        for template_tag in model_doc_element.TaggedValues:
            if template_tag.Name == "RTFTemplate":
                template_tag.Value = template
                template_tag.Notes = "Default: Model Report"
                template_tag.Update()
            elif template_tag.Name == "SearchName":
                template_tag.Value = search_name
                template_tag.Update()
            elif template_tag.Name == "SearchValue":
                template_tag.Value = element_GUID
                template_tag.Update()
    else:
        # Add tagged values when no GUID is provided
        for template_tag in model_doc_element.TaggedValues:
            if template_tag.Name == "RTFTemplate":
                template_tag.Value = template
                template_tag.Notes = "Default: Model Report"
                template_tag.Update()
                break
        
        # Set master document package ID as a dummy attribute to make the template work
        attribute = model_doc_element.Attributes.AddNew(master_document.Name, "Package")
        attribute.ClassifierID = master_document.Element.ElementID
        attribute.Update()

def connect(package_GUID, document_name, document_version, document_alias):
    
    owner_package = repository.GetPackageByGuid(package_GUID)
    master_document_package = add_master_document(package_GUID, document_name, document_version, document_alias)
    
    # Example usage of add_model_document_for_package
    example_package = owner_package.Packages[0]  # Example: Assume the first package in owner_package
    model_doc_element = add_model_document_for_package(master_document_package, example_package, "ModelDocument", 0, "Template")
    
    print("Model document added to master document:", model_doc_element.Name)
    # Example usage:
    master_document = master_document_package
    template = "Template"
    element_name = "Element Name"
    element_GUID = "Element GUID"
    treepos = 0
    search_name = "Search Name"
    add_model_document_with_search(master_document, template, element_name, element_GUID, treepos, search_name)


# Example usage of connect function
package_GUID = "{38579E13-7386-40f7-A7DF-FD478DE8667D}"
document_name = "Use Case Details"
document_version = "v1"
document_alias = "1"

connect(package_GUID, document_name, document_version, document_alias)
