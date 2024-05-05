Option Explicit
'New script
!INC Local Scripts.EAConstants-VBScript

Sub LockElements(repository, diagram_id, listbox_locked_elements, locked_elements, action)
    locked_elements.RemoveAll

    Dim diagram
    Set diagram = repository.GetDiagramByID(diagram_id)

    If diagram Is Nothing Then
        MsgBox "Diagram Not Found", vbCritical, "Error"
        Exit Sub
    End If

    Dim diagram_object, element
    For Each diagram_object In diagram.DiagramObjects
        Set element = repository.GetElementByID(diagram_object.ElementID)
        If Not element Is Nothing Then
            If action = "Lock" Then
                If element.Locked Then
                    locked_elements.Add element.Name
                Else
                    element.Locked = True
                    If repository.IsSecurityEnabled Then
                        element.ApplyUserLock
                    End If
                End If
            ElseIf action = "Unlock" Then
                If Not element.Locked Then
                    locked_elements.Add element.Name
                Else
                    element.Locked = False
                    If repository.IsSecurityEnabled Then
                        element.ApplyUserLock
                    End If
                End If
            End If
        End If
    Next

    listbox_locked_elements.Clear
    Dim element_name
    For Each element_name In locked_elements
        listbox_locked_elements.AddItem element_name
    Next

    If locked_elements.Count > 0 Then
        If action = "Lock" Then
            MsgBox locked_elements.Count & " elements are already locked.", vbInformation, "Locked Elements"
        ElseIf action = "Unlock" Then
            MsgBox locked_elements.Count & " elements are already unlocked.", vbInformation, "Unlocked Elements"
        End If
    Else
        If action = "Lock" Then
            MsgBox "All eligible elements have been locked.", vbInformation, "Done"
        ElseIf action = "Unlock" Then
            MsgBox "All eligible elements have been unlocked.", vbInformation, "Done"
        End If
    End If
End Sub

Sub Main()
    Repository.EnsureOutputVisible "Script"
    
    Dim selected_package, root, listbox_diagrams, listbox_locked_elements, action_var, action_menu, action

    Set selected_package = Repository.GetTreeSelectedPackage()

    action = InputBox("Enter 'Lock' or 'Unlock' to perform the action:", "Enter Action", "Lock")
    If action = "" Then
        MsgBox "Operation cancelled.", vbInformation, "Cancelled"
        Exit Sub
    ElseIf action <> "Lock" And action <> "Unlock" Then
        MsgBox "Invalid action! Please enter 'Lock' or 'Unlock'.", vbCritical, "Error"
        Exit Sub
    End If

    MsgBox "Apply User Lock", vbOKCancel + vbInformation, "Apply User Lock"
    MsgBox "Select Diagram", vbOKCancel + vbInformation, "Select Diagram"

    Dim wshell, selected_index
    Set wshell = CreateObject("WScript.Shell")

    action_var = "Lock|Unlock"
    selected_index = wshell.Popup("Choose an action:", 0, "Choose Action", vbOKCancel + vbExclamation)

    If selected_index = -1 Then
        MsgBox "Operation cancelled.", vbInformation, "Cancelled"
        Exit Sub
    End If

    action = Split(action_var, "|")(selected_index)
    Set root = CreateObject("WScript.Shell")
    root.Popup "Select Diagram", 0, "Select Diagram", vbOKCancel + vbInformation

    Dim element, diagram_id
    For Each diagram_id In selected_package.Diagrams
        LockElements Repository, diagram_id, Nothing, Nothing, action
    Next
End Sub

Main
