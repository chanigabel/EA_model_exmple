'MasterDocumentClassifiersOnPackage
'The script, written by Chany Jacobs, 
'is designed to create a master document containing document models. 
'This allows users to generate specific documentation about a package by dragging it into one of the models.
'Tested and worked on 01-05-24
option Explicit
!INC Local Scripts.EAConstants-VBScript


' num - order of functions

' 7
Sub add_model_document_for_diagram(repository, master_document, diagram, name, treepos, template)
    ' Get the diagram ID
    Dim diagram_id
    diagram_id = diagram.DiagramID
    
    ' Create a new document object
    Dim document
    Set document = master_document.Elements.AddNew(name, "Model Document")
    
    ' Set properties of the document
    document.TreePos = treepos
    Dim tag
    For Each tag In document.TaggedValues
        If tag.Name = "RTFTemplate" Then
            tag.Value = template
            tag.Notes = template
            tag.Update
            Exit For
        End If
    Next
    
    ' Add the document to the diagram
    Dim diagramObject
    Set diagramObject = diagram.DiagramObjects.AddNew(name, "")
    diagramObject.ElementID = document.ElementID
    diagramObject.Update
    
    ' Refresh the diagram view
    repository.ReloadDiagram diagram_id
End Sub

' 6
Function add_master_document_with_details(repository, package_GUID, document_name, document_version, document_alias, diagram_name)
    Dim owner_package
    Set owner_package = repository.GetPackageByGuid(package_GUID)
    
    Dim master_document_package
    Set master_document_package = owner_package.Packages.AddNew(document_name, "Package")
    master_document_package.Update
    master_document_package.Element.Stereotype = "master document"
    master_document_package.Alias = document_alias
    master_document_package.Version = document_version
    master_document_package.Update

    ' Add a new tagged value for the diagram name
    Dim diagram_name_tag
    Set diagram_name_tag = master_document_package.Element.TaggedValues.AddNew("DiagramName", "")
    diagram_name_tag.Value = diagram_name
    diagram_name_tag.Update

    ' Link to the master template
    Dim template_tag
    For Each template_tag In master_document_package.Element.TaggedValues
        If template_tag.Name = "RTFTemplate" Then
            template_tag.Value = "Connector"
            template_tag.Notes = "Connector"
            template_tag.Update
            Exit For
        End If
    Next

    Set add_master_document_with_details = master_document_package
End Function

' 5
Function make_master_document(repository, package_GUID)
    Dim document_version
    document_version = InputBox("Please enter the version of this document (e.g., x.y.z): ")
    Dim document_alias
    document_alias = InputBox("Please enter the alias of this document: ")
    Dim document_diagram_name
    document_diagram_name = InputBox("Please enter the name of this document: ")

    If document_version <> "" Then
        Dim document_name
        document_name = "D - " & document_diagram_name & " v. " & document_version
        Set make_master_document = add_master_document_with_details(repository, package_GUID, document_name, document_version, document_alias, document_diagram_name)
    Else
        Set make_master_document = Nothing
    End If
End Function

' 4
Function create_diagram(repository, package_guid, diagram_name, diagram_type)
    Dim package
    Set package = repository.GetPackageByGuid(package_guid)
    If Not package Is Nothing Then
        Dim new_diagram
        Set new_diagram = package.Diagrams.AddNew(diagram_name, diagram_type)
        If Not new_diagram Is Nothing Then
            new_diagram.Update
            Set create_diagram = new_diagram
            Exit Function
        End If
    End If
    Set create_diagram = Nothing
End Function   

' 3
Sub create_document(repository, documents_package_GUID)
    Dim master_document
    Set master_document = make_master_document(repository, documents_package_GUID) 
    
    Dim documentation_diagram
    Set documentation_diagram = create_diagram(repository, master_document.PackageGUID, "Documentation Diagram", "Documentation")
    
    If Not master_document Is Nothing Then
        If Not documentation_diagram Is Nothing Then
            Dim i
            i = 0
            add_model_document_for_diagram repository, master_document, documentation_diagram, "Classifier Documentation", i, "ClassifierOnPackage_tm"
            i = i + 1
			
            repository.RefreshModelView master_document.PackageID
            repository.ShowInProjectView master_document
        End If
    End If
End Sub

' 2
Sub main()
	Repository.EnsureOutputVisible "Script"
    Dim documents_package
    Set documents_package = repository.GetTreeSelectedPackage()
    If Not documents_package Is Nothing Then
        Dim package_GUID
        package_GUID = documents_package.PackageGUID
        create_document repository, package_GUID
        MsgBox "Select the Master Document and press F8 to generate document"
    Else
        MsgBox "This script requires a package to be select"
    End If
End Sub

' 1
main
