'UpdateAuthorDiagramElementsAndUpdateInLinks
'The script, written by Chany Jacobs, 
'This script updating the Author of Diagram Elements, 
'and to the sub diagrams too. (links for diagrams)
'Tested and worked on 04-30-2024
' Declare global variables
Dim rep, selected_Diagram

' Function to check if an element is locked by another user in the repository
Function IsElementLocked(element_guid, repository)
    Dim squery, result, xmlDoc, user
    squery = "SELECT UserID FROM t_seclocks WHERE EntityID='" & element_guid & "'"
    result = repository.SQLQuery(squery)
    Set xmlDoc = CreateObject("MSXML2.DOMDocument")	'This code snippet creates an XML document 
    xmlDoc.LoadXml result                         	'object, loads XML data into it, retrieves 
    Set user = xmlDoc.SelectSingleNode("//UserID")	'the root element of the XML document, 
    If Not user Is Nothing Then                   	'and then retrieves all elements with the tag name 
        IsElementLocked = True						'"UserID" within the XML document.
    Else
        IsElementLocked = False
    End If
End Function

' Function to create dialog box interface for updating author
Sub UpdateAuthorDialog(rep)
    Dim dialog_result, txt_to_author, txt_from_author
    If rep.IsSecurityEnabled Then
        dialog_result = MsgBox("This option opens the Update author dialog box which enables updating the author of the selected Diagram's elements which are not locked." & vbCrLf & vbCrLf & "Would you like to proceed?", vbYesNo + vbQuestion, "Tevel EA Addin: Update author of Diagram Elements")
    Else
        dialog_result = MsgBox("This option opens the Update author dialog box which enables updating the author of the selected Diagram's elements." & vbCrLf & vbCrLf & "Would you like to proceed?", vbYesNo + vbQuestion, "Tevel EA Addin: Update author of Diagram Elements")
    End If
    If dialog_result = vbYes Then
        Set selected_Diagram = GetSelectedDiagram(rep)
        If Not selected_Diagram Is Nothing Then
            ChangeAuthor rep, selected_Diagram
        Else
            MsgBox "Please select a Diagram", vbExclamation, "Warning"
        End If
    End If
End Sub

' Function to retrieve the currently selected diagram
Function GetSelectedDiagram(ea_repos)
    Dim selected_Diagram
    Set selected_Diagram = ea_repos.GetCurrentDiagram()
    Set GetSelectedDiagram = selected_Diagram
End Function

' Function to create dialog box interface for updating author
Sub ChangeAuthor(rep, selected_Diagram)
    Dim txt_to_author, txt_from_author
    txt_to_author = InputBox("Enter the Author to update to:", "Update Author", "")
	If txt_to_author <> "" Then
		txt_from_author = InputBox("Enter the Author to update from:", "Update Author", "")
		If txt_from_author <> "" Then
			OnUpdateClickAuthor rep, selected_Diagram, txt_to_author, txt_from_author
		Else
        MsgBox "Process cancelled."
		End If
	Else
        MsgBox "Process cancelled."
    End If
End Sub

' Function to retrieve linked diagrams for the currently selected diagram
Function GetAllLinksInCurrentDiagram(rep, selected_Diagram)
    Dim squery, result, xmlDoc, root, pdata1_values, element
    squery = "SELECT PDATA1 FROM t_object INNER JOIN t_diagramobjects ON t_object.Object_ID = t_diagramobjects.Object_ID WHERE t_diagramobjects.Diagram_ID = " & CStr(selected_Diagram.DiagramID) & " AND PDATA1 IS NOT NULL"
    result = rep.SQLQuery(squery)
    Set xmlDoc = CreateObject("MSXML2.DOMDocument") 		'This code snippet creates an XML document 
    xmlDoc.LoadXml result 									'object, loads XML data into it, retrieves 
    Set root = xmlDoc.documentElement						'the root element of the XML document, 
    Set pdata1_values = root.getElementsByTagName("PDATA1") 'and then retrieves all elements with the tag name 
    Dim linksList()											'"PDATA1" within the XML document.	
    ReDim linksList(pdata1_values.length - 1)
    For Each element In pdata1_values
        linksList(index) = element.text
        index = index + 1
    Next
    GetAllLinksInCurrentDiagram = linksList
End Function

' Function to update the author
Sub UpdateAuthor(rep, selected_Diagram, txt_to_author, txt_from_author,pdata1_values)
    Dim cur_object, cur_element
    For Each cur_object In selected_Diagram.DiagramObjects
        If Not IsInArray(CStr(cur_object.ElementID), pdata1_values) Then
            Set cur_element = rep.GetElementByID(cur_object.ElementID)
            If cur_element.Author = txt_from_author Then
                If rep.IsSecurityEnabled Then
                    If Not IsElementLocked(cur_element.ElementGUID, rep) Then
                        cur_element.ApplyUserLock
                        cur_element.Author = txt_to_author
                        cur_element.Update
                    End If
                Else
                    cur_element.Author = txt_to_author
                    cur_element.Update
                End If
            End If
        End If
    Next
    
	Dim cur_PDATA1
	For Each cur_PDATA1 In pdata1_values
		If CInt(cur_PDATA1) > 0 Then
			Set linked_diagram=rep.GetDiagramByID(CInt(cur_PDATA1))
			linked_diagram.Author = txt_to_author
			linked_diagram.Update()
			
		End If
	Next
	MsgBox selected_Diagram.Name & " Diagram authors elements updated successfully!", vbInformation + vbOKOnly, "Info"

End Sub

' Function to recursively update author for linked diagrams
Sub OnUpdateClickAuthor(rep, selected_Diagram, txt_to_author, txt_from_author)
    Dim pdata1_values
    pdata1_values = GetAllLinksInCurrentDiagram(rep, selected_Diagram)
    UpdateAuthor rep, selected_Diagram, txt_to_author, txt_from_author, pdata1_values
End Sub

' Function to check if an element ID is in the array of linked diagrams
Function IsInArray(ID, arr)
    Dim i
    For i = LBound(arr) To UBound(arr)
        If arr(i) = ID Then
            IsInArray = True
            Exit Function
        End If
    Next
    IsInArray = False
End Function

' Main function
Sub Main()
    Repository.EnsureOutputVisible "Script"
    UpdateAuthorDialog repository
End Sub

' Call the main function
Main
