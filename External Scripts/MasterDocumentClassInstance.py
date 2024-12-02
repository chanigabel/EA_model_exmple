import win32com.client

# Step 7 - Add model document for a selected instance and classifier
def add_model_document_for_instance(repository, master_document, instance, classifier_name, treepos, template):
    # Create a new document object for the instance
    document = master_document.Elements.AddNew(instance.Name, "Model Document")
    document.TreePos = treepos
    
    # Set the template for the document
    for tag in document.TaggedValues:
        if tag.Name == "RTFTemplate":
            tag.Value = template
            tag.Notes = template
            tag.Update()
            break
    
    # Link instance to classifier in the document
    instance_tag = document.TaggedValues.AddNew("Classifier", "")
    instance_tag.Value = classifier_name
    instance_tag.Update()
    
    document.Update()
    repository.ReloadDiagram(instance.DiagramID)  # Refresh view if needed

# Step 6 - Create master document package with additional tagged values
def add_master_document_with_details(repository, diagram, document_name, document_version, document_alias):
    owner_package = repository.GetPackageByGuid(diagram.PackageGUID)
    master_document_package = owner_package.Packages.AddNew(document_name, "Package")
    master_document_package.Element.Stereotype = "master document"
    master_document_package.Alias = document_alias
    master_document_package.Version = document_version
    master_document_package.Update()
    
    # Add diagram description as a tagged value
    description_tag = master_document_package.Element.TaggedValues.AddNew("DiagramDescription", "")
    description_tag.Value = diagram.Notes
    description_tag.Update()
    
    return master_document_package

# Step 5 - Main function to create the document with instances and classifiers
def create_master_document(repository, diagram):
    document_version = input("Enter document version (e.g., x.y.z): ")
    document_alias = input("Enter document alias: ")
    document_name = f"D - {diagram.Name} v. {document_version}"
    
    master_document = add_master_document_with_details(
        repository, diagram, document_name, document_version, document_alias
    )
    
    if master_document:
        # Retrieve instances and their classifiers
        for i, instance in enumerate(diagram.DiagramObjects):
            classifier_name = instance.Classifier.Name  # Assuming Classifier is accessible
            add_model_document_for_instance(
                repository, master_document, instance, classifier_name, i, "InstanceTemplate"
            )
        
        repository.RefreshModelView(master_document.PackageID)
        repository.ShowInProjectView(master_document)

# Step 2 - Main entry point
def main():
    ea = win32com.client.Dispatch("EA.App")
    repository = ea.Repository
    selected_diagram = repository.GetTreeSelectedObject()
    print(selected_diagram.Type)
    if selected_diagram and selected_diagram.Type == "Diagram":
        create_master_document(repository, selected_diagram)
        print("Master document created for the selected diagram.")
    else:
        print("Please select a diagram.")

# Run the main function
main()
